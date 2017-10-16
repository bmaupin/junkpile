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
        when:"A valid date is provided"
            def scores = github.getScores(['javascript', 'java', 'python'],
                Date.parse('yyyy-MM-dd', '2017-01-01'))

        then:"Valid scores are returned"
            scores.size() == 3
            scores.javascript > 1000000
            scores.java > 1000000
            scores.python > 500000

        when:"An invalid date is provided"
            scores = github.getScores(['javascript', 'java', 'python'],
                Date.parse('yyyy-MM-dd', '2007-01-01'))

        then:"Null scores are returned"
            scores.size() == 3
            scores.javascript == null
            scores.java == null
            scores.python == null
    }
}
