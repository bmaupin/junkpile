package langpop

class Score {
    Date date
    Integer score

    static belongsTo = [lang: Lang,
                        site: Site]

    static constraints = {
    }
}
