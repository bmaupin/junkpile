import langpop.*

import groovy.transform.Field
import javax.xml.parsers.SAXParser
import javax.xml.parsers.SAXParserFactory
import org.xml.sax.helpers.DefaultHandler
import org.xml.sax.*


def SO_DUMP_FILE = '/home/bmaupin/Desktop/temp-so/Posts.xml'

class MyHandler extends DefaultHandler {
    // This is the last date of data that isn't in the DB already
    def LAST_DATE = '2015-07-15'

    def lastDate = Date.parse('yyyy-MM-dd', LAST_DATE)

    def soSite = Site.findByName(ImportUtil.STACKOVERFLOW_SITE_NAME)
    def soLangNames = ImportUtil.getStackoverflowLangNames()

    // This will hold the running total count for each language
    def totalCounts = [:]
    Date currentDate

    void startElement(String ns, String localName, String qName, Attributes atts) {
        if (qName == 'row') {
            // Parse the date, dropping the time
            def creationDate = Date.parse('yyyy-MM-dd', atts.getValue('CreationDate'))

            // Write the previous day's data to the DB if the date changes
            if (creationDate > currentDate) {
                println creationDate

                // currentDate will be null the first time we get here
                if (currentDate != null) {
                    soLangNames.each { langName ->
                        ImportUtil.newCount(
                            currentDate.clearTime(),
                            totalCounts[langName],
                            Lang.findByName(ImportUtil.getGitHubLangName(langName)),
                            soSite
                        )
                    }
                }

                currentDate = creationDate
            }

            // Do this check after creationDate > currentDate to make sure the last date gets written to the DB
            if (creationDate > lastDate) {
                System.exit(0)
            }

            // Check for null as well as empty
            if (atts.getValue('Tags')) {
                atts.getValue('Tags').replaceAll('<', ' ').replaceAll('>', ' ').split().each { tag ->
                    if (tag in soLangNames) {
                        // Some of the dates aren't in order, so just retroactively increment them up to the current date
                        if (creationDate < currentDate) {
                            def dateToIncrement = creationDate
                            while (dateToIncrement < currentDate) {
                                incrementCount(dateToIncrement, Lang.findByName(ImportUtil.getGitHubLangName(tag)), soSite)
                                dateToIncrement ++
                            }
                        }

                        if (!(tag in totalCounts)) {
                            totalCounts[tag] = 0
                        }
                        totalCounts[tag] ++
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
File file = new File(SO_DUMP_FILE)
DefaultHandler handler = new MyHandler()
parser.parse(file, handler)
