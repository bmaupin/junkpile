package langpop.sites

class Stackoverflow extends CodingSite {
    // TODO: handle API limitations in instance
    private static final int API_SLEEP_TIME = 60000
    // Uses a custom filter that only returns quota_remaining and total
    // (https://api.stackexchange.com/docs/create-filter#unsafe=false&filter=!GeF-5sUcKK53)&run=true)
    private static final String API_URL = 'https://api.stackexchange.com/2.2/search?todate=%s&site=stackoverflow&tagged=%s&filter=!GeF-5sUcKK53)'
    // Try this many times on API failures before giving up
    private static final int MAX_API_TRIES = 20
    private static final String OLDEST_DATE = '2008-07-31'

    private String apiKey

    @Override
    Date getOldestDate() {
        return Date.parse('yyyy-MM-dd', OLDEST_DATE)
    }

    @Override
    Integer getScore(String langName, Date date) {
        if (!isDateValid(date)) {
            return null
        }

        def url = String.format(API_URL, encodeDate(date), encodeLangName(langName))
        def result = getResult(url)

        log.debug "StackOverflow API daily quota remaining: ${result.quota_remaining}"

        return result.total
    }

    @Override
    void setApiKey(String apiKey) {
        this.apiKey = apiKey
    }

    private static String encodeDate(Date date) {
        // All dates in the API are in unix epoch time, which is the number of seconds since midnight UTC January 1st,
        // 1970. (https://api.stackexchange.com/docs/dates)
        return date.getTime() / 1000
    }

    private static String encodeLangName(String langName) {
        return java.net.URLEncoder.encode(langName.toLowerCase().replaceAll(' ', '-'))
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
}
