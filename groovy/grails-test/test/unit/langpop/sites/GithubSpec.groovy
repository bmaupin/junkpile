package langpop.sites

import spock.lang.Specification

class GithubSpec extends Specification {
    def github = new langpop.sites.Github()

    void "Test getScore for valid date"() {
        given:
        def score = github.getScore('javascript', Date.parse('yyyy-MM-dd', '2017-01-01'))
        println score

        expect:
        score > 1000000
    }

    // TODO: implement this once we've defined behaviour for invalid dates
    // void "Test getScore for invalid date"() {
    //     given:
    //     def score = github.getScore('javascript', Date.parse('yyyy-MM-dd', '2007-01-01'))

    //     expect:
    //     score == 0
    // }

    // TODO: implement this once we've defined behaviour for invalid languages
    // void "Test getScore for invalid language"() {
    //     given:
    //     def score = github.getScore('notalanguage', Date.parse('yyyy-MM-dd', '2007-01-01'))

    //     expect:
    //     score == 0
    // }
}
