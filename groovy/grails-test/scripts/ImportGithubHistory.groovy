import langpop.*


def FIRST_DATE = ImportUtil.GITHUB_OLDEST_DATE
// This is the last date of data that isn't in the DB already
def LAST_DATE = '2015-07-15'

def firstDate = Date.parse('yyyy-MM-dd', FIRST_DATE)
def searchDate = firstDate
def lastDate = Date.parse('yyyy-MM-dd', LAST_DATE)

def ghSite = Site.findByName(ImportUtil.GITHUB_SITE_NAME)

// Build the list of languages, sorted alphabetically
def langNames = ImportUtil.getGithubLangNames()
Collections.sort(langNames, String.CASE_INSENSITIVE_ORDER)
def langs = []
langNames.each{ langName ->
    langs.add(Lang.findByName(langName))
}

// This will hold the running total count for each language
def totalCounts = [:]

while (searchDate <= lastDate) {
    langs.each{ lang ->
        // Be verbose in case we have to abort the script
        println "${searchDate}\t${lang.name}"

        // Populate the total counts from the DB if this is the first date
        if (searchDate == firstDate) {
            def query = Count.where {
                date == searchDate - 1 && lang.id == lang.id && site.id == ghSite.id
            }
            def count = query.find()

            if (count == null) {
                totalCounts[lang.name] = 0
            } else {
                totalCounts[lang.name] = count.count
            }
        }

        totalCounts[lang.name] += ImportUtil.getGithubRepoCount(lang.name, searchDate)

        if (totalCounts[lang.name] != 0) {
            new Count(
                // Remove the time component of the date just to be safe
                date: searchDate.clearTime(),
                count: totalCounts[lang.name],
                lang: lang,
                site: ghSite
            // TODO: this save doesn't get persisted without flush: true...
            ).save(flush: true)
        }
    }

    searchDate += 1
}
