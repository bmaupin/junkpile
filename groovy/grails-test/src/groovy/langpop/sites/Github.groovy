package langpop.sites

class Github extends CodingSite {
    // TODO: handle API limitations in instance
    // Maximum number of requests that can be made within the API_TIME_LIMIT
    private static final int API_REQ_LIMIT = 10
    // Time limit in milliseconds
    private static final int API_TIME_LIMIT = 60000
    private static final String API_URL = 'https://api.github.com/search/repositories?q=language:%s+created:<=%s'
    // Try this many times on API failures before giving up
    private static final int MAX_API_TRIES = 20
    // This is the date of the oldest data in github
    private static final String OLDEST_DATE = '2007-10-29'

    @Override
    Date getOldestDate() {
        return Date.parse('yyyy-MM-dd', OLDEST_DATE)
    }

    @Override
    Integer getScore(String langName, Date date) {
        if (!isDateValid(date)) {
            return null
        }

        def searchURL = String.format(API_URL, encodeLangName(langName), encodeDate(date))

        // TODO: have the api token as part of the instance?
        def githubAuthToken = System.getenv('GITHUB_AUTH_TOKEN')
        if (githubAuthToken != null) {
            searchURL += '&access_token=' + githubAuthToken
        }

        int apiCount = 0
        URLConnection conn
        int score

        while (true) {
            try {
                conn = new URL(searchURL).openConnection()
                score = new groovy.json.JsonSlurper().parseText(conn.getURL().getText())['total_count']
                break

            } catch (java.io.IOException e) {
                try {
                    if (conn.getResponseCode() == 403) {
                        log.warn 'Exceeded Github API request limit'
                        log.debug "Max requests per minute: ${conn.getHeaderField('X-RateLimit-Limit')}"
                        log.debug "Requests remaining: ${conn.getHeaderField('X-RateLimit-Remaining')}"
                        log.debug "Rate reset time: ${new Date(Long.parseLong(conn.getHeaderField('X-RateLimit-Reset')) * 1000)}"

                        sleep(API_TIME_LIMIT)

                    // TODO: this never actually occurs for the way we're presently using the API
                    } else if (conn.getResponseCode() == 422) {
                        log.warn "Github API request empty for lang: ${langName} (The language may have been renamed or removed)"

                        return 0
                    }

                } catch (java.net.ConnectException | java.net.UnknownHostException e2) {
                    if (++apiCount == MAX_API_TRIES) {
                        throw e2
                    }
                    log.warn e2
                    sleep(API_TIME_LIMIT)
                }
            }
        }

        return score
    }

    private static String encodeDate(Date date) {
        return date.format('yyyy-MM-dd')
    }

    private static String encodeLangName(String langName) {
        // Spaces must be replaced with dashes for github language names
        return java.net.URLEncoder.encode(langName.replaceAll(' ', '-'))
    }
}
