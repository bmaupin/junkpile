package langpop



import static org.springframework.http.HttpStatus.*
import grails.transaction.Transactional
import groovy.time.TimeCategory

@Transactional(readOnly = true)
class CountController {

    static allowedMethods = [save: "POST", update: "PUT", delete: "DELETE"]

    def countService

    def index(Integer max) {
        params.max = Math.min(max ?: 10, 100)
        respond Count.list(params), model:[countInstanceCount: Count.count()]
    }

    def test1() {
        respond Site.list()
    }

    def test2() {
        // Use 5 dates, 90 day increments, and 20 languages for interesting results

        def dateLabels = []
        def langCounts = [:]
        def langs = []
        // Keep track of how many dates we get data for
        def dateCount = 0

        (0..4).each{ dateIndex ->
            dateCount ++
            def queryDate = new Date().clearTime() - (dateIndex * 7)
            def formattedDate = queryDate.format('yyyy-MM-dd')
            dateLabels.add(formattedDate)

            countService.getTopLangCounts2(5, queryDate).each{
                def langName = Lang.findById(it[0]).name
                if (!(langName in langs)) {
                    langs.add(langName)
                }
                if (!(langName in langCounts)) {
                    langCounts[langName] = []
                }

                // Use the specific dateIndex so missing dates will be filled with nulls
                langCounts[langName][dateIndex] = it[1]
            }
        }

        langs.each{ langName ->
            // Replace all null elements with 0
            Collections.replaceAll(langCounts[langName], null, 0)

            // Fill missing language data with 0
            while (langCounts[langName].size() != dateCount) {
                langCounts[langName].add(0)
            }
        }

        render dateLabels
        render "<br>"
        render langCounts


        /*
        langCounts = {
            '2016-07-14': {
                'Javascript': 555,
                'somethineelse': 444,
    
        }
        */

        /*
        dates = ['2016-07-14', ...]
        langCoounts = {
            'Javascript': [555, 555, 555]
        }
        */


        /*
        render countService.getTopLangCounts2(5, new Date().clearTime())
        render "<br>"
        */

        /*
        countService.getTopLangCounts2(5, new Date().clearTime()).each{
            render "${Lang.findById(it[0]).name}: ${it[1]}<br>"
        }
        */

        /*
        1. Get counts
        2. Put in map
        */



        /*
        (0..4).each{
            def queryDate = new Date().clearTime() - (it * 7)

            def langCounts = [:]

            langCounts[queryDate.format('yyyy-MM-dd')] = countService.getTopLangCounts(5, queryDate)
            render langCounts

            render "<br>"
        }
        */

        /*
        def langCounts = [:]

        langCounts[queryDate.format('yyyy-MM-dd')] = countService.getTopLangCounts(5, queryDate)
        render langCounts
        */

        /*
        langCounts = {}
        langCounts[date] = {}
        langCounts[date][]
        */
    }

    def testtime() {
        def startTime = new Date()

        (0..4).each{
            countService.getTopLangCounts(5, new Date().clearTime())
            def endTime = new Date()
            def elapsedTime = TimeCategory.minus(endTime, startTime)
            startTime = endTime

            render "${elapsedTime}<br>"
        }
    }

    def testchart() {}

    def testtop5() {}

    def testtoday() {
        def queryDate = new Date().clearTime()
        render "<h3>${queryDate}</h3>"
        render "<ol>"
        countService.getTopLangCounts(20, queryDate).each { lang, count ->
            render "<li>${lang.name}: ${count}</li>"
        }
        render "</ol>"

//        render {

//        }

//        respond Count.getTopLangs(20)

        //respond Site.list()
        //[site: Site.get(params.id)]
//        render(text) {
            
/*
        println "<h4>Top languages overall:</h4>"
        langCounts.sort{ -it.value }.take(20).each{ lang, count ->
            println "${lang.name}: ${count}<br>"
        }
*/
//        }

/*
        render {
            "<h4>Top languages overall:</h4>"
            langCounts.sort{ -it.value }.take(20).each{ lang, count ->
                "${lang.name}: ${count}<br>"
            }
        }
*/


/*        
def site = Site.findByName('stackoverflow')
def lang = Lang.findByName('C')

render "${lang.name}: ${lang.altNames}"
/*
def query = Count.where {
    lang.id == lang.id && site.id == site.id && date == new Date().clearTime()
}
if (query.count() == 1) {
    respond query.get().count
}
*/

    }

    def show(Count countInstance) {
        respond countInstance
    }

    def create() {
        respond new Count(params)
    }

    @Transactional
    def save(Count countInstance) {
        if (countInstance == null) {
            notFound()
            return
        }

        if (countInstance.hasErrors()) {
            respond countInstance.errors, view:'create'
            return
        }

        countInstance.save flush:true

        request.withFormat {
            form multipartForm {
                flash.message = message(code: 'default.created.message', args: [message(code: 'count.label', default: 'Count'), countInstance.id])
                redirect countInstance
            }
            '*' { respond countInstance, [status: CREATED] }
        }
    }

    def edit(Count countInstance) {
        respond countInstance
    }

    @Transactional
    def update(Count countInstance) {
        if (countInstance == null) {
            notFound()
            return
        }

        if (countInstance.hasErrors()) {
            respond countInstance.errors, view:'edit'
            return
        }

        countInstance.save flush:true

        request.withFormat {
            form multipartForm {
                flash.message = message(code: 'default.updated.message', args: [message(code: 'Count.label', default: 'Count'), countInstance.id])
                redirect countInstance
            }
            '*'{ respond countInstance, [status: OK] }
        }
    }

    @Transactional
    def delete(Count countInstance) {

        if (countInstance == null) {
            notFound()
            return
        }

        countInstance.delete flush:true

        request.withFormat {
            form multipartForm {
                flash.message = message(code: 'default.deleted.message', args: [message(code: 'Count.label', default: 'Count'), countInstance.id])
                redirect action:"index", method:"GET"
            }
            '*'{ render status: NO_CONTENT }
        }
    }

    protected void notFound() {
        request.withFormat {
            form multipartForm {
                flash.message = message(code: 'default.not.found.message', args: [message(code: 'count.label', default: 'Count'), params.id])
                redirect action: "index", method: "GET"
            }
            '*'{ render status: NOT_FOUND }
        }
    }
}
