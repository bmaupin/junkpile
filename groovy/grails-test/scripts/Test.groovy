import langpop.*


Date prevDate

def currentDate = Date.parse('yyyy-MM-dd', '2015-07-15')
println currentDate > prevDate


/*
// Replace imported Stackoverflow data with totals
def FIRST_DATE = ImportUtil.STACKOVERFLOW_OLDEST_DATE
// This is the last date of data that isn't in the DB already
def LAST_DATE = '2015-07-15'

def firstDate = Date.parse('yyyy-MM-dd', FIRST_DATE)
def searchDate = firstDate
def lastDate = Date.parse('yyyy-MM-dd', LAST_DATE)

def soSite = Site.findByName(ImportUtil.STACKOVERFLOW_SITE_NAME)

// This will hold the running total count for each language
def totalCounts = [:]

while (searchDate <= lastDate) {
    Lang.list().each { lang ->
        // Be verbose in case we have to abort the script
        println "${searchDate}\t${lang.name}"

        // Get today's count
        def query = Count.where {
            date == searchDate && lang.id == lang.id && site.id == soSite.id
        }
        def count = query.find()

        if (count == null) {
            if (lang.name in totalCounts && totalCounts[lang.name] != 0) {
                new Count(
                    // Remove the time component of the date just to be safe
                    date: date.clearTime(),
                    count: totalCounts[lang.name],
                    lang: lang,
                    site: site
                // TODO: this save doesn't get persisted without flush: true...
                ).save(flush: true)
            }

        } else {
            if (!(lang.name in totalCounts)) {
                totalCounts[lang.name] = count.count

            } else {
                totalCounts[lang.name] += count.count
                count.count = totalCounts[lang.name]
                // TODO: this save doesn't get persisted without flush: true...
                count.save(flush: true)
            }
        }
    }

    searchDate += 1
}
*/

/*
// Get an idea of how many times dates in stackoverflow dump are out of order
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
*/

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

