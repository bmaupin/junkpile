import langpop.*

import groovy.transform.Field
import javax.xml.parsers.SAXParser
import javax.xml.parsers.SAXParserFactory
import org.xml.sax.helpers.DefaultHandler
import org.xml.sax.*


def soDumpFile = '/home/bmaupin/Desktop/temp-so/Posts.xml'

class MyHandler extends DefaultHandler {
    // This is the last date of data that isn't in the DB already
    def lastDate = Date.parse('yyyy-MM-dd', '2015-07-15')

    def soSite = Site.findByName(ImportUtil.STACKOVERFLOW_SITE_NAME)
    def soLangNames = ImportUtil.getStackoverflowLangNames()

    void startElement(String ns, String localName, String qName, Attributes atts) {
        if (qName == 'row') {
            // Parse the date, dropping the time
            def creationDate = Date.parse('yyyy-MM-dd', atts.getValue('CreationDate'))

            if (creationDate <= lastDate) {
                println creationDate
                // Check for null as well as empty
                if (atts.getValue('Tags')) {
                    atts.getValue('Tags').replaceAll('<', ' ').replaceAll('>', ' ').split().each { tag ->
                        if (tag in soLangNames) {
                            println tag

                            incrementCount(creationDate, Lang.findByName(ImportUtil.getGitHubLangName(tag)), soSite)
                        }
                    }
                }
            }
        }
    }

    void incrementCount(Date date, Lang lang, Site site) {
        def query = Count.where {
            date == date && lang.id == lang.id && site.id == site.id
        }
        def count = query.find()

        if (count == null) {
            new Count(
                // Remove the time component of the date just to be safe
                date: date.clearTime(),
                count: 1,
                lang: lang,
                site: site
            // TODO: this save doesn't get persisted without flush: true...
            ).save(flush: true)

        } else {
            count.count ++
            // TODO: this save doesn't get persisted without flush: true...
            count.save(flush: true)
        }
    }
}

// XmlParser and XmlSlurper read the whole file into memory, so we have to use SAXParser instead
SAXParserFactory factory = SAXParserFactory.newInstance()
SAXParser parser = factory.newSAXParser()
File file = new File(soDumpFile)
DefaultHandler handler = new MyHandler()
parser.parse(file, handler)
