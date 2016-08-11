import langpop.*

def startDate = Date.parse('yyyy-MM-dd', '2008-10-29')

(0..10).each{
    println ImportUtil.getGithubRepoCount('ruby', startDate + it)
}


/*
ImportUtil.getStackoverflowLangNames().each {
    println it
    println ImportUtil.getGitHubLangName(it)
}

println ImportUtil.getStackoverflowLangNames().size()
*/

//println ImportUtil.STACKOVERFLOW_ALT_NAMES

//println ImportUtil.getGithubLangs()

//def conn = new URL('http://localhost:8999').getText()

/*
def countService = ctx.countService

countService.getTopLangCounts(20).each { lang, count ->
    println "${lang.name}: ${count}"
}
*/

/*
site = Site.findByName('stackoverflow')
lang = Lang.findByName('Go')
new Count(
    date: new Date().clearTime(),
    //date: new java.sql.Date(new java.util.Date().getTime()),
    count: 111,
    lang: lang,
    site: site
).save()
*/

/*
// Wipe the time portion of the timestamp and just leave the date
Count.list().each { c ->
    c.date = new Date(c.date.getTime()).clearTime()
    c.save()
}
*/

/*
def site = Site.findByName('stackoverflow')
def lang = Lang.findByName('Go')
def query = Count.where {
    lang.id == lang.id && site.id == site.id && date == new Date().clearTime()
}
if (query.count() == 1) {
    println query.get().count
}



def notLangs = [
    'AppleScript',
    'ASP',
    'Arduino',
    'Batchfile',
    'CMake',
    'CSS',
    'Cuda',
    'HTML',
    'HTTP',
    'JSON',
    'Makefile',
    'Max',
    'Nginx',
    'Processing',
    'Puppet',
    'QML',
    'SQL',
    'TeX',
    'VimL',
    'XML',
    'XSLT',
]

def langCounts = [:]
Lang.list().each { lang ->
    if (!(lang.name in notLangs)) {
        def langTotalCount = 0

        Site.list().each { site ->
            def query = Count.where {
                lang.id == lang.id && site.id == site.id && date == new Date().clearTime()
            }
            if (query.count() == 1) {
                langTotalCount += query.get().count
            }
        }

        langCounts[lang] = langTotalCount
    }
}

println "<h4>Top languages overall:</h4>"
langCounts.sort{ -it.value }.take(20).each{ lang, count ->
    println "${lang.name}: ${count}<br>"
}
*/

