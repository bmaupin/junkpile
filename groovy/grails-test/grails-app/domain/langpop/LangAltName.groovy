package langpop

class LangAltName {
    String altName

    static belongsTo = [lang: Lang,
                        site: Site]

    static constraints = {
    }
}
