package langpop

class Lang {
    String name

    static hasMany = [altNames: LangAltName]

    static constraints = {
        name blank: false, unique: true
    }
}
