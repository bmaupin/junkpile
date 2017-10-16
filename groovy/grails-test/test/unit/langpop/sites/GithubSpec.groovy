package langpop.sites

import spock.lang.Specification

class GithubSpec extends Specification {
    def github = new langpop.sites.Github()

    def setup() {
        def apiKey = System.getenv('GITHUB_API_KEY')
        if (apiKey != null) {
            github.setApiKey(apiKey)
        }
    }

    void "Test getScore"() {
        when:"A valid date is provided"
            def score = github.getScore('javascript', Date.parse('yyyy-MM-dd', '2017-01-01'))

        then:"A valid score is returned"
            score > 2000000

        when:"An invalid date is provided"
            score = github.getScore('javascript', Date.parse('yyyy-MM-dd', '2007-01-01'))

        then:"Null is returned"
            score == null
    }

    void "Test getScores"() {
        given:
            def scores = github.getScores(['javascript', 'java', 'python'],
                Date.parse('yyyy-MM-dd', '2017-01-01'))

        expect:
            scores.size() == 3
            scores.javascript > 2000000
            scores.java > 2000000
            scores.python > 1000000
    }
}
