package langpop

public class ImportUtil {
    static final String STACKOVERFLOW_SITE_NAME = 'stackoverflow'

    static String getStackoverflowLangName(Lang l) {
        def a = LangAltName.find {
            lang.id == l.id && site.id == Site.findByName(STACKOVERFLOW_SITE_NAME).id
        }

        if (a == null) {
            return l.name.toLowerCase().replaceAll(' ', '-')
        }

        return a.altName
    }

    static List<String> getStackoverflowLangNames() {
        return Lang.list().collect { getStackoverflowLangName(it) }
    }

    static String getGitHubLangName(String name) {
        def a = LangAltName.find {
            altName == name && site.id == Site.findByName(STACKOVERFLOW_SITE_NAME).id
        }

        if (a != null) {
            return Lang.findById(a.lang.id).name

        } else {
            def gitHubLangName = Lang.findByNameIlike(name)?.name
            if (gitHubLangName != null) {
                return gitHubLangName
            } else {
                return Lang.findByNameIlike(name.replaceAll('-', ' '))?.name
            }
        }
    }
}