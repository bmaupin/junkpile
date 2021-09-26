package langpop.sites

import grails.util.Metadata
import org.apache.log4j.Logger

abstract class CodingSite {
    protected static Logger log = Logger.getLogger(Metadata.current.getApplicationName())

    abstract Date getOldestDate()

    abstract Integer getScore(String langName, Date date)

    abstract Map<String, Integer> getScores(ArrayList<String> langNames, Date date)

    abstract void setApiKey(String apiKey)
}
