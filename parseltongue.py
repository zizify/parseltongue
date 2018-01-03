from content import content
from suffixes import verbs, nominals

def go_again():
    go = input('Type another word or phrase, or type Q or q to quit: ')

    if go == 'Q' or go == 'q':
        return
    else:
        split_string(go)
        

def find_suffix(word):
    """Takes part of speech and category to find appropriate suffix gloss from suffixes module."""
    content = word['content']
    suffix = word['suffix']
    
    if content['pos'] == 'verb':
        if content['category'] == 'ar':
            for suf in verbs['ar'].keys():
                if suffix == suf:
                    ending = verbs['ar'][suf]
                    return '{}{}{}{}'.format(ending['tense'], (('.' + ending['mood'] + '.') if ending['mood'] != None else '.'), ending['person'], ending['number'])
        elif content['category'] == 'er':
            for suf in verbs['er'].keys():
                if suffix == suf:
                    ending = verbs['er'][suf]
                    return '{}.{}{}'.format(ending['tense'], ending['person'], ending['number'])
        elif content['category'] == 'ir':
            for suf in verbs['ir'].keys():
                if suffix == suf:
                    ending = verbs['ir'][suf]
                    return '{}.{}{}'.format(ending['tense'], ending['person'], ending['number'])
    elif content['pos'] == 'noun':
        for suf in nominals.keys():
            if suffix == None:
                return 'SG'
            elif suffix in ['os', 'as', 'es', 's']:
                return '{}.{}'.format(content['category'], nominals[suffix]['number'])
    elif content['pos'] == 'adjective':
        for suf in nominals.keys():
            if suffix == None:
                return 'E.SG'
            elif suffix in ['os', 'as', 'es', 's']:
                return '{}.{}'.format(nominals[suffix]['gender'], nominals[suffix]['number'])

    return '???'

def parse(words):
    """Looks up suffixes for each word in relevant module and creates a gloss string."""
    parses = []

    for each in words:
        original = each['original']
        parsed = each['parsed']
        ending = ''
        gloss = each['content']['gloss']

        if not each['content']['regular']:
            ending = each['content']['parse']
        else:
            ending = find_suffix(each)

        parses.append('{}: {} || {}-{}'.format(original, parsed if parsed else '', gloss, ending))
    
    for each in parses:
        print(each)

    go_again()

def create_pair(query):
    """Processes query array and words array of objects, each having content and suffix properties."""
    words = []

    for each in query:
        entry = find_stem(each)
        stem = entry[0]
        content = entry[1]
        suffix = each.replace(stem, '')

        if suffix:
            words.append({'original': each, 'content': content, 'suffix': suffix, 'parsed': (stem + '-' + suffix)})
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

def split_string(string):
    query = string.split(' ')

    create_pair(query)

def retrieve():
    """Requests query string from user and formats input correctly as array of words."""
    query_string = input('Enter a Spanish phrase here: ')

    split_string(query_string)

if __name__ == '__main__':
    retrieve()
