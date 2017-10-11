package langpop.sites

import spock.lang.Specification

class GithubSpec extends Specification {
    def gh = new langpop.sites.Github()

    void "test getScore for valid date"() {
        given:
        def score = gh.getScore("javascript", Date.parse('yyyy-MM-dd', '2017-10-01'))

        expect:
        score > 1000000
    }

    // TODO: implement this once we've defined behaviour for invalid dates
    // void "test getScore for invalid date"() {
    //     given:
    //     def score = gh.getScore("javascript", Date.parse('yyyy-MM-dd', '2007-10-01'))

    //     expect:
    //     score > 1
    // }
}
