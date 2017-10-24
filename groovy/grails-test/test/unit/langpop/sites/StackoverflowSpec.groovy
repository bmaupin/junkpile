package langpop.sites

import spock.lang.Specification

class StackoverflowSpec extends Specification {
    def stackoverflow = new langpop.sites.Stackoverflow()

    def setup() {
        def apiKey = System.getenv('STACKOVERFLOW_API_KEY')
        if (apiKey != null) {
            stackoverflow.setApiKey(apiKey)
        }
    }

    void "Test getScore"() {
        given:
            def score = stackoverflow.getScore('javascript', Date.parse('yyyy-MM-dd', '2017-01-01'))

        expect:
            score > 1000000
    }

    void "Test getScores"() {
        given:
            def scores = stackoverflow.getScores(['javascript', 'java', 'python'],
                Date.parse('yyyy-MM-dd', '2017-01-01'))

        expect:
            scores.size() == 3
            scores.javascript > 1000000
            scores.java > 1000000
            scores.python > 500000
    }
}
