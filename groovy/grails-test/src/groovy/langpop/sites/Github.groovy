package langpop.sites

class Github extends CodingSite {
    // This is the date of the oldest data in github
    static final String OLDEST_DATE = '2007-10-29'
    static final String SITE_NAME = 'github'

    private String apiKey

    static List<String> getLangNames() {
        final String GITHUB_LANGUAGES_URL = 'https://github.com/search/advanced'

        // Use a TagSoup parser because of malformed XML
        def parser = new XmlSlurper(new org.ccil.cowan.tagsoup.Parser())
        def doc = parser.parse(GITHUB_LANGUAGES_URL)
        // Get the select element with id search_language
        def select = doc.depthFirst().find { it.name() == 'select' && it.@id == 'search_language' }

        // Return the text of each option sub-element in a list
        return select.optgroup.option.collect { it.text() }
    }

    @Override
    Date getOldestDate() {
        return Date.parse('yyyy-MM-dd', OLDEST_DATE)
    }

    @Override
    Integer getScore(String langName, Date date) {
        return getScores([langName], date)[langName]
    }

    @Override
    Map<String, Integer> getScores(ArrayList<String> langNames, Date date) {
        // API key can't be null for the GraphQL API (https://platform.github.community/t/anonymous-access/2093)
        if (apiKey == null) {
            throw new Exception('apiKey cannot be null')
        }

        def result = getResult(langNames, date)

        return langNames.collectEntries { langName ->
            [(langName): result.data[encodeLangName(langName)].repositoryCount]
        }
    }

    @Override
    void setApiKey(String apiKey) {
        this.apiKey = apiKey
    }

    private Object getResult(ArrayList<String> langNames, Date date) {
        def postData = encodePostData(langNames, date)
        return callApi(postData)
    }

    private String encodePostData(ArrayList<String> langNames, Date date) {
        final String API_QUERY = '{"query": "{ %s }"}'
        final String LANG_QUERY = '%s: search(query: \\"language:%s created:<%s\\", type: REPOSITORY) { repositoryCount }'

        def langQueries = langNames.collect { langName ->
            String.format(LANG_QUERY, encodeLangName(langName), encodeLangName(langName), encodeDate(date))
        }

        return String.format(API_QUERY, langQueries.join(' '))
    }

    private static String encodeLangName(String langName) {
        // Spaces must be replaced with dashes for github language names
        return java.net.URLEncoder.encode(langName.replaceAll(' ', '-'))
    }

    private static String encodeDate(Date date) {
        return date.format('yyyy-MM-dd')
    }

    private Object callApi(postData) {
        final String API_URL = 'https://api.github.com/graphql'

        // Derived from https://stackoverflow.com/a/42664926/399105
        def conn = new URL(API_URL).openConnection()

        conn.setRequestProperty ('Authorization', "bearer ${apiKey}");
        conn.setRequestMethod('POST')
        conn.setDoOutput(true)
        conn.getOutputStream().write(postData.getBytes('UTF-8'))

        def responseCode = conn.getResponseCode()
        if (responseCode.equals(200)) {
            def jsonResponse = conn.getInputStream().getText()
            return new groovy.json.JsonSlurper().parseText(jsonResponse)

        } else {
            log.error("Github API response code: ${responseCode}, language: ${langName}, date: ${date}")
        }
    }
}
