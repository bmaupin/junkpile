package langpop.sites

import grails.util.Metadata
import org.apache.log4j.Logger

class Stackoverflow implements CodingSite {
    private static final int API_SLEEP_TIME = 60000
    // Uses a custom filter that only returns quota_remaining and total
    // (https://api.stackexchange.com/docs/create-filter#unsafe=false&filter=!GeF-5sUcKK53)&run=true)
    private static final String API_URL = 'https://api.stackexchange.com/2.2/search?todate=%s&site=stackoverflow&tagged=%s&filter=!GeF-5sUcKK53)'
    // Try this many times on API failures before giving up
    private static final int MAX_API_TRIES = 20
    static final String OLDEST_DATE = '2008-07-31'

    private static Logger log = Logger.getLogger(Metadata.current.getApplicationName())

    Integer getScore(String langName, Date dateCreated) {
        // TODO: handle if the date is < OLDEST_DATE. throw an error? return null? return 0?

        def url = String.format(API_URL, encodeDate(dateCreated), encodeLangName(langName))
        def result = getResult(url)

        log.debug "StackOverflow API daily quota remaining: ${result.quota_remaining}"

        if (result.containsKey('total')) {
            return result.total

        } else {
            // TODO: handle unmatched language
            log.info "Unmatched StackOverflow language: ${lang.name}"
        }
    }

    private static Object getResult(String url) {
        def conn = url.toURL().openConnection()

        BufferedReader reader
        int apiCount = 0
        while (true) {
            try {
                reader = new BufferedReader(new InputStreamReader(new java.util.zip.GZIPInputStream(conn.getInputStream())))
                break
            } catch (java.net.ConnectException | java.net.UnknownHostException e) {
                if (++apiCount == MAX_API_TRIES) {
                    throw e
                }
                log.warn e
                sleep(API_SLEEP_TIME)
            }
        }

        def line = ''
        def sb = new StringBuilder()
        while (line = reader.readLine()) {
            sb.append(line)
        }

        return new groovy.json.JsonSlurper().parseText(sb.toString())
    }

    private static String encodeDate(Date date) {
        // All dates in the API are in unix epoch time, which is the number of seconds since midnight UTC January 1st,
        // 1970. (https://api.stackexchange.com/docs/dates)
        return date.getTime() / 1000
    }

    private static String encodeLangName(String langName) {
        return java.net.URLEncoder.encode(langName.toLowerCase().replaceAll(' ', '-'))
    }
}
