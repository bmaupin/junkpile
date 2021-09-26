package langpop



import static org.springframework.http.HttpStatus.*
import grails.converters.JSON
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

    def ajaxGetTopLangs = {
        def chartColors = [
            [63,81,181],
            [3,169,244],
            [0,150,136],
            [139,195,74],
            [255,235,59],
            [255,152,0],
            [233,30,99],
            [103,58,183],
            [33,150,243],
            [0,188,212],
            [76,175,80],
            [205,220,57],
            [255,193,7],
            [255,87,34],
            [244,67,54],
            [156,39,176],
            [121,85,72],
            [158,158,158],
            [96,125,139],
            [0,0,0]
        ]

        // Use 5 dates, 90 day increments, and 20 languages for interesting results

        def chartData = [:]
        def labelsKey = 'labels'
        chartData[labelsKey] = []
        def langCounts = [:]
        // TESTING
        
        def queryDates = [
            '2016-07-18',
            '2015-07-18',
            '2014-07-18',
            '2013-07-18',
            '2012-07-18'
        ]
        
        /*
        def queryDates = [
            '2016-07-20',
            '2014-07-20',
            '2012-07-20',
            '2010-07-20',
            '2008-07-20'
        ]
        */

        (0..4).each{ dateIndex ->
            //def queryDate = new Date().clearTime() - (dateIndex * 80)
            // TESTING
            def queryDate = Date.parse('yyyy-MM-dd', queryDates[dateIndex])
            def formattedDate = queryDate.format('yyyy-MM-dd')
            // Add date to front of list since we want to show oldest first
            chartData[labelsKey].add(0, formattedDate)

            if (dateIndex == 0) {
                countService.getTopLangCounts(10, queryDate).each{
                    def langName = Lang.findById(it[countService.langId]).name
                    if (!(langName in langCounts)) {
                        langCounts[langName] = []
                    }
                    // Add language count in reverse order to show oldest first
                    langCounts[langName].add(0, it[countService.sumCount])
                }

            } else {
                langCounts.keySet().each{ langName ->
                    // Add language count in reverse order to show oldest first
                    langCounts[langName].add(0, countService.getLangCount(langName, queryDate))
                }
            }
        }



/*
        render dateLabels.reverse()
        render "<br>"

        langCounts.each{ langName, counts ->
            render langName
            render "<br>"
            render counts.reverse()
            render "<br>"
        }
        //render langCounts
*/

//        render "'" + dateLabels.join("', '") + "'"

/*
        render(
            view: "testtop5",
            model: [
                dataLabels: ("'" + dateLabels.reverse().join("', '") + "'"),
                dataSetLabels: langs,
                data1: langCounts[langs[0]].reverse(),
                data2: langCounts[langs[1]].reverse(),
                data3: langCounts[langs[2]].reverse(),
                data4: langCounts[langs[3]].reverse(),
                data5: langCounts[langs[4]].reverse()
            ])
*/

/*
        render(contentType: "application/json") {
            model: [
                dateLabels,
                langCounts
            ]
        }
*/



        def datasetsKey = 'datasets'
        chartData[datasetsKey] = []
        def colorIndex = 0

        langCounts.each{ langName, counts ->
            def dataset = [:]
            dataset['label'] = langName
            dataset['fill'] = false
            dataset['lineTension'] = 0.1
            dataset['backgroundColor'] = "rgba(${chartColors[colorIndex].join(',')},0.4)"
            dataset['borderColor'] = "rgba(${chartColors[colorIndex].join(',')},1)"
            dataset['data'] = counts

            chartData[datasetsKey].add(dataset)

            colorIndex ++
        }

        render chartData as JSON


/*
            labels: ["January", "February", "March", "April", "May", "June", "July"],
            datasets: [
                {
                    label: "One",
                    fill: false,
                    lineTension: 0.1,
                    backgroundColor: "rgba(63,81,181,0.4)",
                    borderColor: "rgba(63,81,181,1)",
                    data: [40, 55, 56, 59, 65, 80, 81],
                },
                {
                    label: "Two",
                    fill: false,
                    lineTension: 0.1,
                    backgroundColor: "rgba(3,169,244,0.4)",
                    borderColor: "rgba(3,169,244,1)",
                    data: [41, 49, 57, 70, 72, 79, 79],
                },
                {
                    label: "Three",
                    fill: false,
                    lineTension: 0.1,
                    backgroundColor: "rgba(0,150,136,0.4)",
                    borderColor: "rgba(0,150,136,1)",
                    data: [36, 45, 50, 71, 88, 93, 97],
                },
                {
                    label: "Four",
                    fill: false,
                    lineTension: 0.1,
                    backgroundColor: "rgba(139,195,74,0.4)",
                    borderColor: "rgba(139,195,74,1)",
                    data: [35, 51, 71, 72, 80, 96, 99],
                },
                {
                    label: "Five",
                    fill: false,
                    lineTension: 0.1,
                    backgroundColor: "rgba(255,235,59,0.4)",
                    borderColor: "rgba(255,235,59,1)",
                    data: [25, 35, 41, 47, 51, 54, 60],
                }
            ]
        }
*/

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
            def queryDate = new Date().clearTime() - (dateIndex * 90)
            def formattedDate = queryDate.format('yyyy-MM-dd')
            dateLabels.add(formattedDate)

            countService.getTopLangCounts(5, queryDate).each{
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

/*
        render dateLabels.reverse()
        render "<br>"

        langCounts.each{ langName, counts ->
            render langName
            render "<br>"
            render counts.reverse()
            render "<br>"
        }
        //render langCounts
*/

//        render "'" + dateLabels.join("', '") + "'"


        render(
            view: "testtop5",
            model: [
                dataLabels: ("'" + dateLabels.reverse().join("', '") + "'"),
                dataSetLabels: langs,
                data1: langCounts[langs[0]].reverse(),
                data2: langCounts[langs[1]].reverse(),
                data3: langCounts[langs[2]].reverse(),
                data4: langCounts[langs[3]].reverse(),
                data5: langCounts[langs[4]].reverse()
            ])



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

    def test3() {
        def queryDate = new Date().clearTime()

        //render countService.getLangCount("JavaScript", queryDate)

        render countService.getTopLangCounts(5, queryDate)
        /*.each{
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
