import langpop.*

import groovy.transform.Field
import javax.xml.parsers.SAXParser
import javax.xml.parsers.SAXParserFactory
import org.xml.sax.helpers.DefaultHandler
import org.xml.sax.*

class MyHandler extends DefaultHandler {
    def lastDate = Date.parse('yyyy-MM-dd', '2015-07-15')

    void startElement(String ns, String localName, String qName, Attributes atts) {
        switch (qName) {
            case 'row':
                // Parse the date, dropping the time
                def creationDate = Date.parse('yyyy-MM-dd', atts.getValue('CreationDate'))

                if (creationDate <= lastDate) {
                    println creationDate
                }

                break
        }
    }
}

// XmlParser and XmlSlurper read the whole file into memory, so we have to use SAXParser instead
SAXParserFactory factory = SAXParserFactory.newInstance()
SAXParser parser = factory.newSAXParser()
File file = new File('/home/bmaupin/Desktop/temp-so/Posts-head.xml')
DefaultHandler handler = new MyHandler()
parser.parse(file, handler)
