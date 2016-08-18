import langpop.*

import grails.util.Metadata
import groovy.transform.Field
import org.apache.log4j.Logger


@Field final String STACKOVERFLOW_BASE_URL = 'https://api.stackexchange.com/2.2/tags/%s/info?site=stackoverflow'
final int STACKOVERFLOW_BATCH_API_LIMIT = 20
final String[] SITES = [
    ImportUtil.GITHUB_SITE_NAME,
    ImportUtil.STACKOVERFLOW_SITE_NAME,
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
    'ECLiPSe': 'eclipse-clp',
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
    'POV-Ray SDL': 'povray',
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


Map<Lang, Integer> getStackoverflowTagCount(ArrayList<Lang> langs) {
    def conn =  String.format(STACKOVERFLOW_BASE_URL, java.net.URLEncoder.encode((langs.collect{ return ImportUtil.getStackoverflowLangName(it) }.join(';')), 'UTF-8')).toURL().openConnection()
    BufferedReader reader
    int apiCount = 0
    while (true) {
        try {
            reader = new BufferedReader(new InputStreamReader(new java.util.zip.GZIPInputStream(conn.getInputStream())))
            break
        } catch (java.net.ConnectException | java.net.UnknownHostException e) {
            if (++apiCount == ImportUtil.MAX_API_TRIES) {
                throw e
            }
            log.warn e
            sleep(ImportUtil.STACKOVERFLOW_API_SLEEP_TIME)
        }
    }

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
            if (ImportUtil.getStackoverflowLangName(lang) == item['name']) {
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

// Populate the sites table
SITES.each {
    if (!Site.findByName(it)) {
        new Site(name: it).save()
    }
}


// Populate the lang table
ImportUtil.getGithubLangNames().each {
    if (!Lang.findByName(it)) {
        new Lang(name: it).save()
    }
}


// Populate the LangAltName table
def soSite = Site.findByName(ImportUtil.STACKOVERFLOW_SITE_NAME)

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
def ghSite = Site.findByName(ImportUtil.GITHUB_SITE_NAME)

Lang.list().eachWithIndex { lang, ghApiReqCount ->
    def ghRepoCount = ImportUtil.getGithubRepoCount(lang.name)

    new Count(
        // We only want the date, not the time
        date: new Date().clearTime(),
        count: ghRepoCount,
        lang: lang,
        site: ghSite
    ).save()

    if ((ghApiReqCount + 1) % ImportUtil.GITHUB_API_REQ_LIMIT == 0) {
        sleep(ImportUtil.GITHUB_API_TIME_LIMIT)
    }

/*
    // DEBUG
    if (ghApiReqCount >= 15) {
        System.exit(0)
    }
*/
}
