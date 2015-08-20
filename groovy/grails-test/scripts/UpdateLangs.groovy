import langpop.*
import grails.util.Metadata
import groovy.transform.Field
import org.apache.log4j.Logger


final int GITHUB_API_REQ_LIMIT = 5
@Field final int GITHUB_API_TIME_LIMIT = 60000
@Field final String GITHUB_BASE_URL = 'https://api.github.com/search/repositories?q=language:'
final String GITHUB_SITE_NAME = 'github'

@Field final String STACKOVERFLOW_BASE_URL = 'https://api.stackexchange.com/2.2/tags/%s/info?order=desc&sort=popular&site=stackoverflow'
final int STACKOVERFLOW_BATCH_API_LIMIT = 20
@Field final String STACKOVERFLOW_SITE_NAME = 'stackoverflow'
final String[] SITES = [
    GITHUB_SITE_NAME,
    STACKOVERFLOW_SITE_NAME,
]

final Map STACKOVERFLOW_ALT_NAMES = [
    'Ant Build System': 'ant',
    'API Blueprint': 'apiblueprint',
    'Arc': 'arc-lisp',
    'ASP': 'asp.net',
    'Batchfile': 'batch-file',
    'C2hs Haskell': 'c2hs',
    'Clean': 'clean-language',
    'ColdFusion CFC': 'cfc',
    'Darcs Patch': 'darcs',
    'DIGITAL Command Language': 'dcl',
    'Emacs Lisp': 'elisp',
    'Factor': 'factor-lang',
    'GAMS': 'gams-math',
    'GAP': 'gap-system',
    'Game Maker Language': 'game-maker',
    'Gettext Catalog': 'gettext',
    'Grammatical Framework': 'gf',
    'Graph Modeling Language': 'graph-modelling-language',
    'Graphviz (DOT)': 'graphviz',
    'Groovy Server Pages': 'gsp',
    'Hack': 'hacklang',
    'IGOR Pro': 'igor',
    'Inform 7': 'inform7',
    'Java Server Pages': 'jsp',
    'JSONLD': 'json-ld',
    'Julia': 'julia-lang',
    'LSL': 'linden-scripting-language',
    'Mathematica': 'wolfram-mathematica',
    'OpenEdge ABL': 'openedge',
    'PigLatin': 'apache-pig',
    'Protocol Buffer': 'protocol-buffers',
    'SaltStack': 'salt-stack',
    'SQLPL': 'db2',
    'Standard ML': 'sml',
    'SystemVerilog': 'system-verilog',
    'VimL': 'vim',
    'Visual Basic': 'vb.net',
    'Web Ontology Language': 'owl',
]


@Field Logger log = Logger.getLogger(Metadata.current.getApplicationName())


List<String> getGithubLangs() {
    githubLanguagesUrl = "https://github.com/search/advanced"

    // Use a TagSoup parser because of malformed XML
    def parser = new XmlSlurper(new org.ccil.cowan.tagsoup.Parser())
    def doc = parser.parse(githubLanguagesUrl)
    // Get the select element with id search_language
    def select = doc.depthFirst().find { it.name() == 'select' && it.@id == 'search_language' }

    // Return the text of each option sub-element in a list
    return select.optgroup.option.collect { it.text() }
}


String getStackoverflowLangName(Lang l) {
    def a = LangAltName.find {
        lang.id == l.id && site.id == Site.findByName(STACKOVERFLOW_SITE_NAME).id
    }

    if (a == null) {
        return l.name.toLowerCase().replaceAll(' ', '-')
    }

    return a.altName
}

Map<Lang, Integer> getStackoverflowTagCount(ArrayList<Lang> langs) {
    def conn =  String.format(STACKOVERFLOW_BASE_URL, java.net.URLEncoder.encode((langs.collect{ return getStackoverflowLangName(it) }.join(';')), 'UTF-8')).toURL().openConnection()
    def reader = new BufferedReader(new InputStreamReader(new java.util.zip.GZIPInputStream(conn.getInputStream())))

    def sb = new StringBuilder()
    while (line = reader.readLine()) {
        sb.append(line)
    }

    def jsonResult = new groovy.json.JsonSlurper().parseText(sb.toString())

    // For now stay under the limit rather than worrying about handling paged results 
    if (jsonResult['has_more'] == true) {
        log.error 'Exceeded number of results per single StackExchange API call'
    }

    log.debug "StackOverflow API daily quota remaining: ${jsonResult['quota_remaining']}"

    def soTagCount = [:]
    langs.each { lang ->
        // Use find{} since we can't break fom each{}
        jsonResult['items'].find { item ->
            if (getStackoverflowLangName(lang) == item['name']) {
                soTagCount[lang] = item['count']
                // Break
                return true
            }
        }

        if (!soTagCount.containsKey(lang)) {
            log.info "Unmatched StackOverflow language: ${lang.name}"
        }
    }

    return soTagCount
}

Integer getGithubRepoCount(String langName) {
    // Spaces must be replaced with dashes for github language names
    def conn = new URL(GITHUB_BASE_URL + java.net.URLEncoder.encode(langName.replaceAll(' ', '-'))).openConnection()
    if (conn.getResponseCode() == 403) {
        log.warn 'Exceeded Github API request limit'
        sleep(GITHUB_API_TIME_LIMIT)
        return getGithubRepoCount(langName)
    } else if (conn.getResponseCode() == 422) {
        log.warn "Github API request empty for lang: ${langName}"
        return 0
    } else {
        return new groovy.json.JsonSlurper().parseText(conn.getURL().getText())['total_count']
    }
}


// Populate the sites table
SITES.each {
    if (!Site.findByName(it)) {
        new Site(name: it).save()
    }
}


// Populate the lang table
getGithubLangs().each {
    if (!Lang.findByName(it)) {
        new Lang(name: it).save()
    }
}


// Populate the LangAltName table
def soSite = Site.findByName(STACKOVERFLOW_SITE_NAME)

STACKOVERFLOW_ALT_NAMES.each { langName, langAltName ->
    def lang = Lang.findByName(langName)

    def query = LangAltName.where {
        altName == langAltName && lang.id == lang.id && site.id == soSite.id
    }
    // If the LangAltName doesn't exist
    if (query.count() == 0) {
        // Create it
        new LangAltName(
            altName: langAltName,
            lang: lang,
            site: soSite
        ).save()
    }
}


// Add counts for stackoverflow
//
def debugCount = 0

Lang.list().collate(STACKOVERFLOW_BATCH_API_LIMIT).each {
    def soTagCount = getStackoverflowTagCount(it.each{})

    soTagCount.each{ lang, tagCount ->
        new Count(
            // We only want the date, not the time
            date: new Date().clearTime(),
            count: tagCount,
            lang: lang,
            site: soSite
        ).save()
    }

//    debugCount ++
//    if (debugCount == 1) {
//        System.exit(0)
//    }
}


// Add counts for github
def ghSite = Site.findByName(GITHUB_SITE_NAME)

Lang.list().eachWithIndex { lang, ghApiReqCount ->
    def ghRepoCount = getGithubRepoCount(lang.name)

    new Count(
        // We only want the date, not the time
        date: new Date().clearTime(),
        count: ghRepoCount,
        lang: lang,
        site: ghSite
    ).save()

    if ((ghApiReqCount + 1) % GITHUB_API_REQ_LIMIT == 0) {
        sleep(GITHUB_API_TIME_LIMIT)
    }

/*
    // DEBUG
    if (ghApiReqCount >= 15) {
        System.exit(0)
    }
*/
}
