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
     * - Esoteric programming languages (Brainfuck, Dogescript, LOLCODE, etc)
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
        'Befunge',
        'Bison',
        'BitBake',
        'Blade',
        'Bluespec',
        'Brainfuck',
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
        'ECL', // https://github.com/hpcc-systems/ecl-ml ??
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
        'Gradle',
        'Grammatical Framework',
        'Graph Modeling Language',
        'GraphQL',
        'Graphviz (DOT)',
        'Groovy Server Pages',
        'Haml',
        'Handlebars',
        'HCL', // https://github.com/hashicorp/hcl
        'HLSL', // https://en.wikipedia.org/wiki/High-Level_Shading_Language
        'HTML',
        'HTML+Django',
        'HTML+ECR',
        'HTML+EEX',
        'HTML+ERB',
        'HTML+PHP',
        'HTTP', // httpspec??
        'HyPhy', // https://en.wikipedia.org/wiki/HYPHY_(software)
        'IGOR Pro',
        'Inform 7',
        'INI',
        'Inno Setup',
        'IRC log',
        'Isabelle', // https://en.wikipedia.org/wiki/Isabelle_(proof_assistant)
        'Isabelle ROOT', // Isabelle Session ROOT specification file (https://isabelle.in.tum.de/doc/system.pdf)
        'Jasmin', // https://en.wikipedia.org/wiki/Jasmin_(software)
        'Java Server Pages',
        'JFlex',
        'Jison',
        'Jison Lex',
        'JSON',
        'JSON5',
        'JSONiq',
        'JSONLD',
        'JSX',
        'Jupyter Notebook',
        'KiCad Layout',
        'KiCad Legacy Layout',
        'KiCad Schematic',
        'Kit', // https://codekitapp.com/help/kit/
        'KRL', // https://en.wikipedia.org/wiki/KUKA_Robot_Language
        'LabVIEW',
        'Latte', // https://latte.nette.org/en/ ??
        'Lean', // https://leanprover.github.io/
        'Less',
        'Lex',
        'LilyPond',
        'Linker Script',
        'Linux Kernel Module',
        'Liquid', // https://shopify.github.io/liquid/
        'Literate Agda',
        'Literate CoffeeScript',
        'Literate Haskell',
        'LLVM',
        'Logos', // http://iphonedevwiki.net/index.php/Logos
        'LOLCODE',
        'LookML',
        'LoomScript',
        'LSL', // https://en.wikipedia.org/wiki/Linden_Scripting_Language
        'M4',
        'M4Sugar',
        'Mako', // http://www.makotemplates.org/
        'Makefile',
        'Markdown',
        'Marko', // https://markojs.com/
        'Mask', // https://github.com/atmajs/MaskJS
        'Maven POM',
        'Max', // https://en.wikipedia.org/wiki/Max_(software)
        'MAXScript', // MAXScript is the built-in scripting language for Autodesk ® 3ds Max ® and Autodesk ® 3ds Max ® Design. (http://docs.autodesk.com/3DSMAX/14/ENU/MAXScript%20Help%202012/)
        'MediaWiki',
        'Meson', // http://mesonbuild.com
        'Metal', // This is just C with the Metal API (https://developer.apple.com/metal/)
        'Modelica', // Modeling language, not programming language
        'Module Management System', // HPE Module Management System for OpenVMS
        'Monkey', // For video games
        'Moocode', // https://en.wikipedia.org/wiki/MOO
        'MQL4',
        'MQL5',
        'MTML', // Movable Type Markup Language
        'MUF', // Multi-User Forth (https://en.wikipedia.org/wiki/MUF_(programming_language))
        'mupad', // https://en.wikipedia.org/wiki/MuPAD
        'Myghty', // https://pythonhosted.org/Myghty/
        'NCL', // https://www.ncl.ucar.edu/overview.shtml
        'Nearley', // https://nearley.js.org/
        'nesC',
        'NetLinx',
        'NetLinx+ERB',
        'NetLogo',
        'Nginx',
        'Ninja', // https://ninja-build.org/
        'Nix', // https://nixos.org/
        'NL', // https://en.wikipedia.org/wiki/Nl_(format)
        'NSIS', // https://en.wikipedia.org/wiki/Nullsoft_Scriptable_Install_System
        'Nu',
        'NumPy',
        'ObjDump',
        'Objective-J', // Pretty much exclusive to Cappucino (http://www.cappuccino-project.org/learn/objective-j.html)
        'Omgrofl',
        'OpenCL',
        'OpenEdge ABL',
        'OpenRC runscript',
        'OpenSCAD',
        'OpenType Feature File',
        'Org', // https://en.wikipedia.org/wiki/Org-mode
        'Ox',
        'P4',
        'Pan',
        'Papyrus', // https://www.creationkit.com/fallout4/index.php?title=Papyrus_Introduction
        'Parrot',
        'Parrot Assembly',
        'Parrot Internal Representation',
        'PAWN', // https://www.compuphase.com/pawn/
        'Pep8', // Pep/8 assembly language
        'Perl 6',
        'Pic', // https://en.wikipedia.org/wiki/Pic_language
        'Pickle', // Python Pickle data dump
        'PigLatin', // https://en.wikipedia.org/wiki/Pig_(programming_tool)
        'PLpgSQL',
        'PLSQL',
        'Pod', // https://en.wikipedia.org/wiki/Plain_Old_Documentation
        'PostScript',
        'POV-Ray SDL',
        'PowerBuilder', // AKA PowerScript (https://en.wikipedia.org/wiki/PowerBuilder)
        'Processing',
        'Propeller Spin', // https://en.wikipedia.org/wiki/Parallax_Propeller
        'Protocol Buffer',
        'Public Key',
        'Pug', // https://github.com/pugjs/pug
        'Puppet',
        'Pure Data', // https://en.wikipedia.org/wiki/Pure_Data
        'Python console',
        'Python traceback',
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