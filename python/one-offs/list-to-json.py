''' One-off junk code to convert a list of programming languages with some extra information in the comments to JSON
'''

from collections import OrderedDict

languages = []

for line in t.split('\n'):
    language = OrderedDict()
    slashes = line.find('//')
    if slashes != -1:
        language_name, language_etc = line.split('//', 1)
    else:
        language_name = line
    language_name = language_name.strip()
    language_name = language_name[1:-2]
    language['name'] = language_name
    if slashes != -1:
        language_etc = language_etc.strip()
        if language_etc.startswith('http'):
            language['include'] = False
            language['url'] = language_etc
        elif language_etc.find('http') != -1:
            language_description, language_url = language_etc.split('http')
            if language_description.endswith('('):
                language_description = language_description[:-1]
            language['description'] = language_description.strip()
            language['include'] = False
            if language_url.endswith(')'):
                language_url = language_url[:-1]
            language['url'] = 'http' + language_url.strip()
    else:
        language['include'] = False
    languages.append(language)


language_names = []
for language in languages:
    language_names.append(language['name'])


all_languages = []

for name in names:
    if name in language_names:
        for language in languages:
            if language['name'] == name:
                all_languages.append(language)
                continue
    else:
        language = OrderedDict()
        language['name'] = name
        language['include'] = True
        all_languages.append(language)


outfile = open('languages.json', 'w')
outfile.write(json.dumps(all_languages, indent=4))
outfile.close()
