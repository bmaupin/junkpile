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
        given:
            def score = github.getScore('javascript', Date.parse('yyyy-MM-dd', '2017-01-01'))

        expect:
            score > 2000000
    }

    void "Test getScores"() {
        given:
            def scores = github.getScores(['javascript', 'java', 'python'],
                Date.parse('yyyy-MM-dd', '2017-01-01'))

        expect:
            scores.size() == 3
            scores.javascript > 1000000
            scores.java > 1000000
            scores.python > 500000
    }
}
