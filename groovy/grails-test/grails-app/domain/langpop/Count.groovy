package langpop

class Count {
    Date date
    Integer count

    static belongsTo = [lang: Lang,
                        site: Site]

    static constraints = {
    }

    /*
    def notLangs = [
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

    def fwoof(Integer number) {
        def langCounts = [:]
        Lang.list().each { lang ->
            if (!(lang.name in notLangs)) {
                def langTotalCount = 0

                Site.list().each { site ->
                    def query = Count.where {
                        lang.id == lang.id && site.id == site.id && date == new Date().clearTime()
                    }
                    if (query.count() == 1) {
                        langTotalCount += query.get().count
                    }
                }

                langCounts[lang] = langTotalCount
            }
        }

        return langCounts.sort{ -it.value }.take(number)
    }
    */
}
