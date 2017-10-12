package langpop.sites

class Github extends CodingSite {
    // This is the date of the oldest data in github
    private static final String OLDEST_DATE = '2007-10-29'

    private String apiKey

    @Override
    Date getOldestDate() {
        return Date.parse('yyyy-MM-dd', OLDEST_DATE)
    }

    @Override
    Integer getScore(String langName, Date date) {
        if (!isDateValid(date)) {
            return null
        }

        // API key can't be null for the GraphQL API (https://platform.github.community/t/anonymous-access/2093)
        if (apiKey == null) {
            throw new Exception('apiKey cannot be null')
        }

        def result = getResult(langName, date)

        return result.data.search.repositoryCount
    }

    @Override
    void setApiKey(String apiKey) {
        this.apiKey = apiKey
    }

    private Object getResult(String langName, Date date) {
        final String API_QUERY = '{"query": "{ search(query: \\"language:%s created:<%s\\", type: REPOSITORY) \
            { repositoryCount }}"}'
        final String API_URL = 'https://api.github.com/graphql'

        // Derived from https://stackoverflow.com/a/42664926/399105
        def conn = new URL(API_URL).openConnection()
        def postData = String.format(API_QUERY, encodeLangName(langName), encodeDate(date))

        conn.setRequestProperty ('Authorization', "bearer ${apiKey}");
        conn.setRequestMethod('POST')
        conn.setDoOutput(true)
        conn.getOutputStream().write(postData.getBytes('UTF-8'))

        def responseCode = conn.getResponseCode()
        if (responseCode.equals(200)) {
            def jsonResponse = conn.getInputStream().getText()
            return new groovy.json.JsonSlurper().parseText(jsonResponse)

        } else {
            log.error "Github API response code: ${responseCode}, language: ${langName}, date: ${date}"
        }
    }

    private static String encodeDate(Date date) {
        return date.format('yyyy-MM-dd')
    }

    private static String encodeLangName(String langName) {
        // Spaces must be replaced with dashes for github language names
        return java.net.URLEncoder.encode(langName.replaceAll(' ', '-'))
    }
}
