package langpop

class Site {
    String name

    static constraints = {
        name blank: false, unique: true
    }
}
