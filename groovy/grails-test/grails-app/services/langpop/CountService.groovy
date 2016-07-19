package langpop

class CountService {
    static transactional = false

    // My arbitrary list of non-languages
    def nonLangs = [
        'AppleScript',
        'ASP',
        'Arduino',
        'Batchfile',
        'CMake',
        'CSS',
        'Cuda',
        'HTML',
        'HTTP',
        'JSON',
        'Makefile',
        'Max',
        'Nginx',
        'Processing',
        'Puppet',
        'QML',
        'SQL',
        'TeX',
        'VimL',
        'XML',
        'XSLT',
    ]

    Map<Lang, Integer> getTopLangCounts(int numLangs, Date queryDate) {
        def langCounts = [:]
        Lang.list().each { lang ->
            // Don't include non-languages
            if (!(lang.name in nonLangs)) {
                def langTotalCount = 0

                // Add up the counts for each site for each language
                Site.list().each { site ->
                    def query = Count.where {
                        lang.id == lang.id && site.id == site.id && date == queryDate
                    }
                    if (query.count() == 1) {
                        langTotalCount += query.get().count
                    }
                }

                langCounts[lang] = langTotalCount
            }
        }

        // Do a reverse (descending) sort and return the top n results
        return langCounts.sort{ -it.value }.take(numLangs)
    }

    def getTopLangCounts2(int numLangs, Date queryDate) {
        def results = Count.createCriteria().list {
            eq("date", queryDate)
            projections{
                // SQL: group by lang_id
                lang {
                    groupProperty("id")
                }
                // Calculate the sum of the count column and alias it as sumCount
                // SQL: select sum(count) as sumCount
                sum("count", "sumCount")
            }
            order("sumCount", "desc")
            maxResults(numLangs)
        }

        return results
    }

    def getLangCount(String langName, Date queryDate) {
        def results = Count.createCriteria().list {
            eq("date", queryDate)
            projections{
                lang {
                    // SQL: where lang_id = (select id from lang where name = 'JavaScript')
                    eq("name", langName)
                    // SQL: group by lang_id
                    groupProperty("id")
                }
                // Calculate the sum of the count column
                // SQL: select sum(count)
                sum("count")
            }
        }

        // Return just the count ([1]). There should only be one result (results[0])
        return results[0][1]
    }
}

/*
def countService = ctx.countService
countService.getTopLangCounts(20).each { lang, count ->
    println "${lang.name}: ${count}"
}
*/