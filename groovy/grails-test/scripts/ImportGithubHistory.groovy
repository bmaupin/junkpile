import langpop.*


def OLDEST_GITHUB_DATE = '2007-10-29'

def searchDate = Date.parse('yyyy-MM-dd', OLDEST_GITHUB_DATE)
// This is the last date of data that isn't in the DB already
def lastDate = Date.parse('yyyy-MM-dd', '2015-07-15')

def ghSite = Site.findByName(ImportUtil.GITHUB_SITE_NAME)

// Build the list of languages, sorted alphabetically
def langNames = ImportUtil.getGithubLangNames()
Collections.sort(langNames, String.CASE_INSENSITIVE_ORDER)
def langs = []
langNames.each{ langName ->
    langs.add(Lang.findByName(langName))
}

while (searchDate <= lastDate) {
    langs.each{ lang ->
        // Be verbose in case we have to abort the script
        println "${searchDate}\t${lang.name}"

        def count = ImportUtil.getGithubRepoCount(lang.name, searchDate)

        if (count != 0) {
            new Count(
                // Remove the time component of the date just to be safe
                date: searchDate.clearTime(),
                count: count,
                lang: lang,
                site: ghSite
            // TODO: this save doesn't get persisted without flush: true...
            ).save(flush: true)
        }
    }

    searchDate += 1
}
