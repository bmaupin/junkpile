package langpop

class Score {
    Date date
    Integer score

    static belongsTo = [lang: Lang,
                        site: Site]

    static constraints = {
        // Only allow one score per date, lang, site
        date(unique: ['lang', 'site'])
    }

    void setDate(Date date) {
        // Remove the time component since we only want the date
        this.date = date.clearTime()
    }
}
