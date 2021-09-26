import langpop.Lang
import langpop.Site

class BootStrap {
    def init = { servletContext ->
        populateDatabase()
    }

    def destroy = {
    }

    private static void populateDatabase() {
        populateSite()
        populateLang()
    }

    private static void populateSite() {
        final String[] SITE_NAMES = [
            langpop.sites.Github.SITE_NAME,
            langpop.sites.Stackoverflow.SITE_NAME,
        ]

        if (Site.count() == 0) {
            SITE_NAMES.each { siteName ->
                new Site(name: siteName).save()
            }
        }
    }

    private static void populateLang() {
        final List<String> GITHUB_LANG_NAMES = langpop.sites.Github.getLangNames()

        if (Lang.count() == 0) {
            GITHUB_LANG_NAMES.each { langName ->
                new Lang(name: langName).save()
            }
        }
    }
}
