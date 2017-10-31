package langpop

class CountService {
    static transactional = false

    static final langId = 'langId'
    static final sumCount = 'sumCount'

    // TODO: put this into a data file?
    /* My arbitrary list of non-languages
     * - Markup/data formats (HTML, JSON, XML, YAML, etc)
     * - Languages for build tools (Ant, CMake, etc)
     * - Languages that aren't general purpose (Bluespec, ChucK, Clarion, etc)
     * - Metalanguages (ABNF, EBNF, etc)
     * - File types (Adobe Font Metrics, C-ObjDump, etc)
     * - Templating formats (Closure Templates, EJS, Java Server Pages, etc)
     */
    def nonLangs = [
        'ABNF',
        'Adobe Font Metrics',
        'Alloy',
        'Alpine Abuild',
        'Ant Build System',
        'ANTLR',
        'ApacheConf',
        'API Blueprint',
        'AppleScript',
        'Apollo Guidance Computer',
        'Arduino',
        'AsciiDoc',
        'ASN.1',
        'ASP',
        'Augeas',
        'AutoHotkey',
        'AutoIt',
        'Batchfile',
        'Bison',
        'BitBake',
        'Blade',
        'Bluespec',
        'Brightscript',
        'Bro',
        'C-ObjDump',
        'C2hs Haskell',
        'Cap\'n Proto',
        'CartoCSS',
        'ChucK',
        'Cirru',
        'Clarion',
        'Click',
        'CLIPS',
        'Closure Templates',
        'CMake',
        'ColdFusion CFC',
        'COLLADA',
        'Coq',
        'Cpp-ObjDump',
        'Creole',
        'CSON',
        'Csound',
        'Csound Document',
        'Csound Score',
        'CSS',
        'CSV',
        'Cuda',
        'Cycript',
        'Cython',
        'D-ObjDump',
        'Darcs Patch',
        'DataWeave',
        'desktop',
        'Diff',
        'DIGITAL Command Language',
        'DM',
        'DNS Zone',
        'Dockerfile',
        'Dogescript',
        'DTrace',
        'Eagle',
        'Easybuild',
        'EBNF',
        'Ecere Projects',
        // 'ECL', // ??
        'ECLiPSe', // http://eclipseclp.org/
        'edn',
        'EJS',
        'Emacs Lisp',
        'Filebench WML',
        'Filterscript', // https://en.wikipedia.org/wiki/RenderScript, .fs
        'fish', // https://esolangs.org/wiki/Fish
        'FLUX', // Reshade .fx file?
        'Formatted', // https://github.com/github/linguist/tree/master/samples/Formatted
        'FreeMarker',
        'G-code',
        'Game Maker Language',
        'GAMS', // https://en.wikipedia.org/wiki/General_Algebraic_Modeling_System
        'GAP', // https://en.wikipedia.org/wiki/GAP_(computer_algebra_system)
        'GCC Machine Description',
        'GDB', // https://en.wikipedia.org/wiki/GNU_Debugger
        'GDScript', // https://en.wikipedia.org/wiki/Godot_(game_engine)
        'Genshi', // https://en.wikipedia.org/wiki/Genshi_(templating_language)
        'Gentoo Ebuild',
        'Gentoo Eclass',
        'Gerber Image', // https://en.wikipedia.org/wiki/Gerber_format
        'Gettext Catalog',
        'Gherkin', // https://en.wikipedia.org/wiki/Cucumber_(software)
        'GLSL', // https://en.wikipedia.org/wiki/OpenGL_Shading_Language
        'Glyph', // Pointwise's scripting language, .glf
        'GN', // Generate Ninja, https://chromium.googlesource.com/chromium/src/tools/gn/+/HEAD/docs/language.md, .gn
        'Gnuplot',
        'HTML',
        'HTTP',
        'Java Server Pages',
        'JSON',
        'Makefile',
        'Markdown',
        'Max',
        'Nginx',
        'ObjDump',
        'Processing',
        'Puppet',
        'QML',
        'RenderScript',
        'SQL',
        'TeX',
        'Vim script',
        'VimL',
        'XML',
        'XSLT',
        'YAML',
    ]

    Map<Lang, Integer> getTopLangCountsOld(int numLangs, Date queryDate) {
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

    def getTopLangCounts(int numLangs, Date queryDate) {
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
        // Map the results for easier reference
        }.collect {
            [
                (langId): it[0],
                (sumCount): it[1]
            ]
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

        if (results.size() == 0) {
            return null

        } else {
            if (results.size() > 1) {
                log.warn "getLangCount found more than one result"
            }

            // Return just the count ([1]). There should only be one result (results[0])
            return results[0][1]
        }
    }
}

/*
def countService = ctx.countService
countService.getTopLangCounts(20).each { lang, count ->
    println "${lang.name}: ${count}"
}
*/