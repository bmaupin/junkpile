package langpop

class Count {
    Date date
    Integer count

    static belongsTo = [lang: Lang,
                        site: Site]

    static constraints = {
    }
}
