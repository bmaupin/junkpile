package langpop.sites

class Stackoverflow extends CodingSite {
    // This is the date of the oldest data in stackoverflow
    static final String OLDEST_DATE = '2008-07-31'
    static final String SITE_NAME = 'stackoverflow'

    /* TODO: handle API limitations in instance (https://stackapps.com/a/3057/41977)
     *  - Don't make more than 30 requests/second
     *  - Handle backoff field
     */
    private static final int API_SLEEP_TIME = 60000
    // Uses a custom filter that only returns backoff, quota_remaining, and total
    // (https://api.stackexchange.com/docs/create-filter#unsafe=false&filter=!.UE8F0bVg4M-_Ii4&run=true)
    private static final String API_URL = 'https://api.stackexchange.com/2.2/search?todate=%s&site=stackoverflow&tagged=%s&filter=!.UE8F0bVg4M-_Ii4'
    // Try this many times on API failures before giving up
    private static final int MAX_API_TRIES = 20

    private String apiKey

    @Override
    Date getOldestDate() {
        return Date.parse('yyyy-MM-dd', OLDEST_DATE)
    }

    @Override
    Integer getScore(String langName, Date date) {
        def url = String.format(API_URL, encodeDate(date), encodeLangName(langName))
        def result = getResult(url)

        log.debug("StackOverflow API daily quota remaining: ${result.quota_remaining}")

        return result.total
    }

    @Override
    Map<String, Integer> getScores(ArrayList<String> langNames, Date date) {
        return langNames.collectEntries { langName ->
            [(langName): getScore(langName, date)]
        }
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

    private Object getResult(String url) {
        url = addApiKey(url)
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
                log.warn(e)
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

    private String addApiKey(String url) {
        final String KEY_PARAMETER = '&key='
        if (apiKey != null) {
            url = "${url}${KEY_PARAMETER}${apiKey}"
        }

        return url
    }
}
