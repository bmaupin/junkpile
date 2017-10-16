package langpop.sites

import spock.lang.Specification

class StackoverflowSpec extends Specification {
    def stackoverflow = new langpop.sites.Stackoverflow()

    void "Test getScore"() {
        when:"A valid date is provided"
            def score = stackoverflow.getScore('javascript', Date.parse('yyyy-MM-dd', '2017-01-01'))

        then:"A valid score is returned"
            score > 1000000

        when:"An invalid date is provided"
            score = stackoverflow.getScore('javascript', Date.parse('yyyy-MM-dd', '2007-01-01'))

        then:"Null is returned"
            score == null
    }

    void "Test getScores"() {
        when:"A valid date is provided"
            def scores = stackoverflow.getScores(['javascript', 'java', 'python'],
                Date.parse('yyyy-MM-dd', '2017-01-01'))

        then:"Valid scores are returned"
            scores.size() == 3
            scores.javascript > 1000000
            scores.java > 1000000
            scores.python > 500000

        when:"An invalid date is provided"
            scores = stackoverflow.getScores(['javascript', 'java', 'python'],
                Date.parse('yyyy-MM-dd', '2007-01-01'))

        then:"Null scores are returned"
            scores.size() == 3
            scores.javascript == null
            scores.java == null
            scores.python == null
    }
}
