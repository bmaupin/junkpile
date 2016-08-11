package langpop

import grails.util.Metadata
import org.apache.log4j.Logger


public class ImportUtil {
    static final int GITHUB_API_REQ_LIMIT = 10
    static final int GITHUB_API_TIME_LIMIT = 60000
    static final String GITHUB_REPO_URL = 'https://api.github.com/search/repositories?q=language:'
    static final String GITHUB_SITE_NAME = 'github'

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

        def conn = new URL(searchURL).openConnection()
        int totalCount

        try {
            totalCount = new groovy.json.JsonSlurper().parseText(conn.getURL().getText())['total_count']

        } catch (java.io.IOException e) {
            try {
                if (conn.getResponseCode() == 403) {
                    log.warn 'Exceeded Github API request limit'
                    sleep(GITHUB_API_TIME_LIMIT)
                    return getGithubRepoCount(langName, dateCreated)
                } else if (conn.getResponseCode() == 422) {
                    log.warn "Github API request empty for lang: ${langName}"
                    return 0
                }

            } catch (java.net.ConnectException | java.net.UnknownHostException e2) {
                log.warn e2
                sleep(GITHUB_API_TIME_LIMIT)
                return getGithubRepoCount(langName, dateCreated)
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
}