import langpop.*

import javax.xml.parsers.SAXParser
import javax.xml.parsers.SAXParserFactory
import org.xml.sax.helpers.DefaultHandler
import org.xml.sax.*


class MyHandler extends DefaultHandler {
    Date lastDate

    void startElement(String ns, String localName, String qName, Attributes atts) {
        if (qName == 'row') {
            // Parse the date, dropping the time
            def creationDate = Date.parse('yyyy-MM-dd', atts.getValue('CreationDate'))

            if (creationDate > lastDate) {
                lastDate = creationDate

            } else if (creationDate < lastDate) {
                println "ERROR: CreationDate ${creationDate} is older than previous date ${lastDate}"
            }
        }
    }
}

// XmlParser and XmlSlurper read the whole file into memory, so we have to use SAXParser instead
SAXParserFactory factory = SAXParserFactory.newInstance()
SAXParser parser = factory.newSAXParser()
File file = new File('/home/bmaupin/Desktop/temp-so/Posts.xml')
DefaultHandler handler = new MyHandler()
parser.parse(file, handler)


/*
println ImportUtil.getGithubLangNames().size()
*/

/*
def githubAuthToken = System.getenv("GITHUB_AUTH_TOKEN")
println githubAuthToken
*/

/*
def startDate = Date.parse('yyyy-MM-dd', '2008-10-29')

(0..10).each{
    println ImportUtil.getGithubRepoCount('ruby', startDate + it)
}
*/

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

