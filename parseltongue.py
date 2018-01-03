from content import content
from suffixes import verbs, nominals

output = {}

def create_output(query):
    """INC--Generates user-readable output."""
    for n in range(0, len(query)):
        output[query[n]] = 'none'

def find_suffix(word):
    """Takes part of speech and category to find appropriate suffix gloss from suffixes module."""
    content = word['content']
    suffix = word['suffix']
    
    if word['content']['pos'] == 'verb':
        if word['content']['category'] == 'ar':
            for suf in verbs['ar'].keys():
                if word['suffix'] == suf:
                    ending = verbs['ar'][suf]
                    return '{}.{}{}'.format(ending['tense'], ending['person'], ending['number'])
        elif word['content']['category'] == 'er':
            for suf in verbs['er'].keys():
                if word['suffix'] == suf:
                    ending = verbs['er'][suf]
                    return '{}.{}{}'.format(ending['tense'], ending['person'], ending['number'])
        elif word['content']['category'] == 'ir':
            for suf in verbs['ir'].keys():
                if word['suffix'] == suf:
                    ending = verbs['ir'][suf]
                    return '{}.{}{}'.format(ending['tense'], ending['person'], ending['number'])
    
    return '???'

def parse(words):
    """INC--Looks up suffixes for each word in relevant module and creates a gloss string."""
    parses = []

    for each in words:
        original = each['original']
        ending = ''
        gloss = each['content']['gloss']

        if not each['content']['regular']:
            ending = each['content']['parse']
        else:
            ending = find_suffix(each)

        parses.append('{}: {}-{}'.format(original, gloss, ending))
    
    for each in parses:
        print(each)

def create_pair(query):
    """Processes query array and words array of objects, each having content and suffix properties."""
    words = []

    for each in query:
        entry = find_stem(each)
        stem = entry[0]
        content = entry[1]
        suffix = each.replace(stem, '')

        if suffix:
            words.append({'original': each, 'content': content, 'suffix': suffix})
        else:
            words.append({'original': each, 'content': content, 'suffix': None})

    parse(words)

def find_stem(word):
    """Looks up the content stem of each queried word and returns it to create_pair()."""
    entry = [None, None]

    for index in range(len(word), 0, -1):
        for key in content.keys():
            stem = word[:index]
            if key == stem:
                entry[0] = stem
                entry[1] = content[stem]
    
    return entry

def retrieve():
    """Requests query string from user and formats input correctly as array of words."""
    query_string = input('Enter a Spanish phrase here: ')
    query = query_string.split(' ')

    create_pair(query)

if __name__ == '__main__':
    retrieve()
