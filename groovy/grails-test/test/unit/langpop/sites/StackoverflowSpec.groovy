package langpop.sites

import spock.lang.Specification

class StackoverflowSpec extends Specification {
    def stackoverflow = new langpop.sites.Stackoverflow()

    void "test getScore for valid date"() {
        given:
        def score = stackoverflow.getScore("javascript", Date.parse('yyyy-MM-dd', '2017-01-01'))

        expect:
        score > 1000000
    }

    // TODO: implement this once we've defined behaviour for invalid dates
    // void "test getScore for invalid date"() {
    //     given:
    //     def score = stackoverflow.getScore("javascript", Date.parse('yyyy-MM-dd', '2007-01-01'))

    //     expect:
    //     score == 0
    // }
}
