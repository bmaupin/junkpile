package langpop

import grails.util.Metadata
import org.apache.log4j.Logger


public class ImportUtil {
    // Try this many times on API failures before giving up
    static final int MAX_API_TRIES = 20

    static final int GITHUB_API_REQ_LIMIT = 10
    static final int GITHUB_API_TIME_LIMIT = 60000
    // This is the date of the oldest data in github
    static final String GITHUB_OLDEST_DATE = '2007-10-29'
    static final String GITHUB_REPO_URL = 'https://api.github.com/search/repositories?q=language:'
    static final String GITHUB_SITE_NAME = 'github'

    // The amount of time to wait in between failed requests
    static final String STACKOVERFLOW_API_SLEEP_TIME = 60000
    static final String STACKOVERFLOW_OLDEST_DATE = '2008-07-31'
    static final String STACKOVERFLOW_SITE_NAME = 'stackoverflow'

    static Logger log = Logger.getLogger(Metadata.current.getApplicationName())

    static String getGitHubLangName(String name) {
        def a = LangAltName.find {
            altName == name && site.id == Site.findByName(STACKOVERFLOW_SITE_NAME).id
        }

        if (a != null) {
            return Lang.findById(a.lang.id).name

        } else {
            def gitHubLangName = Lang.findByNameIlike(name)?.name
            if (gitHubLangName != null) {
                return gitHubLangName
            } else {
                return Lang.findByNameIlike(name.replaceAll('-', ' '))?.name
            }
        }
    }

    static List<String> getGithubLangNames() {
        def githubLanguagesUrl = "https://github.com/search/advanced"

        // Use a TagSoup parser because of malformed XML
        def parser = new XmlSlurper(new org.ccil.cowan.tagsoup.Parser())
        def doc = parser.parse(githubLanguagesUrl)
        // Get the select element with id search_language
        def select = doc.depthFirst().find { it.name() == 'select' && it.@id == 'search_language' }

        // Return the text of each option sub-element in a list
        return select.optgroup.option.collect { it.text() }
    }

    static Integer getGithubRepoCount(String langName) {
        return getGithubRepoCount(langName, null)
    }

    static Integer getGithubRepoCount(String langName, Date dateCreated) {
        // Spaces must be replaced with dashes for github language names
        def searchURL = GITHUB_REPO_URL + java.net.URLEncoder.encode(langName.replaceAll(' ', '-'))

        if (dateCreated != null) {
            searchURL += '+created:' + dateCreated.format('yyyy-MM-dd')
        }

        def githubAuthToken = System.getenv("GITHUB_AUTH_TOKEN")
        if (githubAuthToken != null) {
            searchURL += '&access_token=' + githubAuthToken
        }

        int apiCount = 0
        URLConnection conn
        int totalCount

        while (true) {
            try {
                conn = new URL(searchURL).openConnection()
                totalCount = new groovy.json.JsonSlurper().parseText(conn.getURL().getText())['total_count']
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

        return totalCount
    }

    static String getStackoverflowLangName(Lang l) {
        def a = LangAltName.find {
            lang.id == l.id && site.id == Site.findByName(STACKOVERFLOW_SITE_NAME).id
        }

        if (a == null) {
            return l.name.toLowerCase().replaceAll(' ', '-')
        }

        return a.altName
    }

    static List<String> getStackoverflowLangNames() {
        return Lang.list().collect { getStackoverflowLangName(it) }
    }

    // TODO: this should probably be moved to the domain
    // Adds a new count to the database
    static void newCount(Date date, int count, Lang lang, Site site) {
        // Don't waste DB space by adding a count of 0
        if (count == 0) {
            return
        }

        // Don't add duplicate counts
        def query = Count.where {
            date == date && lang.id == lang.id && site.id == site.id
        }
        if (query.find() != null) {
            log.warn "Count already exists for date: ${date} lang: ${lang.name} site: ${site.name}"
            return
        }

        new Count(
            // Remove the time component of the date just to be safe
            date: date.clearTime(),
            count: count,
            lang: lang,
            site: site
        // TODO: this save doesn't get persisted without flush: true...
        ).save(flush: true)
    }
}
