import langpop.Site

class BootStrap {
    def init = { servletContext ->
        populateDatabase()
    }

    def destroy = {
    }

    private static void populateDatabase() {
        populateSite()
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
}
