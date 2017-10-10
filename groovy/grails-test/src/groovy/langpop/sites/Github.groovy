package langpop.sites

import grails.util.Metadata
import org.apache.log4j.Logger

class Github implements CodingSite {
    // Try this many times on API failures before giving up
    private static final int MAX_API_TRIES = 20
    // Maximum number of requests that can be made within the GITHUB_API_TIME_LIMIT
    private static final int GITHUB_API_REQ_LIMIT = 10
    // Time limit in milliseconds
    private static final int GITHUB_API_TIME_LIMIT = 60000
    // This is the date of the oldest data in github
    static final String GITHUB_OLDEST_DATE = '2007-10-29'
    private static final String GITHUB_REPO_URL = 'https://api.github.com/search/repositories?q=language:'

    private static Logger log = Logger.getLogger(Metadata.current.getApplicationName())

    Integer getScore(String langName, Date dateCreated) {
        // TODO: handle if the date is < GITHUB_OLDEST_DATE. throw an error? return null? return 0?

        def searchURL = GITHUB_REPO_URL + encodeLangName(langName)

        searchURL += '+created:<=' + dateCreated.format('yyyy-MM-dd')

        // TODO: have the api token as part of the instance?
        def githubAuthToken = System.getenv("GITHUB_AUTH_TOKEN")
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

                        sleep(GITHUB_API_TIME_LIMIT)

                    } else if (conn.getResponseCode() == 422) {
                        log.warn "Github API request empty for lang: ${langName} (The language may have been renamed or removed)"

                        return 0
                    }

                } catch (java.net.ConnectException | java.net.UnknownHostException e2) {
                    if (++apiCount == MAX_API_TRIES) {
                        throw e2
                    }
                    log.warn e2
                    sleep(GITHUB_API_TIME_LIMIT)
                }
            }
        }

        return score
    }

    private static String encodeLangName(String langName) {
        // Spaces must be replaced with dashes for github language names
        return java.net.URLEncoder.encode(langName.replaceAll(' ', '-'))
    }
}
