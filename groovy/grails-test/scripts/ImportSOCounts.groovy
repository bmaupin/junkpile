import langpop.*

/* Out of memory
def posts = new XmlSlurper().parse('/home/bmaupin/Desktop/temp-so/Posts.xml')
def posts = new XmlParser().parse('/home/bmaupin/Desktop/temp-so/Posts.xml')

posts.row.each{
    println it.@CreationDate
}
*/

/*
import javax.xml.parsers.SAXParserFactory
import org.xml.sax.helpers.DefaultHandler
import org.xml.sax.*

def handler = new DefaultHandler()
def reader = SAXParserFactory.newInstance().newSAXParser().XMLReader
reader.setContentHandler(handler)
def inputStream = new ByteArrayInputStream(XmlExamples.CAR_RECORDS.getBytes("UTF-8"))
reader.parse(new InputSource(inputStream))
*/

import javax.xml.parsers.SAXParser
import javax.xml.parsers.SAXParserFactory
import org.xml.sax.helpers.DefaultHandler
import org.xml.sax.*

class MyHandler extends DefaultHandler {
    void startElement(String ns, String localName, String qName, Attributes atts) {
        switch (qName) {
           case 'row':
               println atts.getValue('CreationDate'); break
        }
    }
    /*
    void characters(char[] chars, int offset, int length) {
       if (countryFlag) {
           currentMessage += new String(chars, offset, length)
       }
    }
    void endElement(String ns, String localName, String qName) {
        switch (qName) {
           case 'car':
               messages << currentMessage; break
           case 'country':
               currentMessage += ' has a '; countryFlag = false; break
        }
    }
    */
}

SAXParserFactory factory = SAXParserFactory.newInstance()
SAXParser parser = factory.newSAXParser()
File file = new File('/home/bmaupin/Desktop/temp-so/Posts.xml')
DefaultHandler handler = new MyHandler()
parser.parse(file, handler)
