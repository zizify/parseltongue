from wordlist import content
from suffixes import verbs, nominals

def go_again(output):
    """Prompts user to enter another query or quit."""
    go = input('Type another word or phrase, or type Q or q to quit: ')

    if go == 'Q' or go == 'q':
        return
    else:
        split_string(go)

def send_output(output):
    """Prints output."""
    for each in output:
        print(each)

    go_again(output)

def find_suffix(word):
    """Takes part of speech and category to find appropriate suffix gloss from suffixes module."""
    content = word['content']
    suffix = word['suffix']
    
    if content['pos'] == 'verb':
        if content['category'] == 'ar':
            ending = verbs['ar'][suffix]
            return '-{}{}{}{}'.format(ending['tense'], (('.' + ending['mood'] + '.') if ending['mood'] != None else '.'), ending['person'], ending['number'])
        elif content['category'] == 'er':
            ending = verbs['er'][suffix]
            return '-{}.{}{}'.format(ending['tense'], ending['person'], ending['number'])
        elif content['category'] == 'ir':
            ending = verbs['ir'][suffix]
            return '-{}.{}{}'.format(ending['tense'], ending['person'], ending['number'])
    elif content['pos'] == 'noun':
        if suffix == None:
            return ''
        elif suffix in ['os', 'as', 'es', 's']:
            return '-{}.{}'.format(content['category'], nominals[suffix]['number'])
    elif content['pos'] == 'adjective':
        if suffix == None:
            return ''
        else:
            return '-{}.{}'.format(nominals[suffix]['gender'], nominals[suffix]['number'])
    else:
        return ''

def parse(words):
    """Looks up suffixes for each word in relevant module and creates a gloss string."""
    output = []

    for each in words:
        original = each['original']
        parsed = each['parsed'] if each['parsed'] != None else original
        gloss = each['content']['gloss']
        word_type = ''

        if each['content']['regular'] == 'unknown':
            ending = ''
        elif not each['content']['regular']:
            ending = each['content']['parse']
        else:
            ending = find_suffix(each)

        if each['content']['pos'] in ['verb', 'noun']:
            word_type = each['content']['pos'] + ' (' + each['content']['category'] + ')'
        else:
            word_type = each['content']['pos']

        output.append('{}: {} || {} || {}{}'.format(original, word_type, parsed, gloss, ending))

    send_output(output)

def create_virtual(word):
    if len(word) == 1:
        return {'pos': '?', 'gloss': 'unknown, unlikely to be true word', 'regular': 'unknown', 'no_suffix': True, 'unknown': True}
    elif word.endswith(('ción', 'sión', 'ad', 'ez')):
        return {'pos': 'noun', 'category': 'F', 'gloss': 'unknown', 'regular': True, 'no_suffix': True, 'unknown': True}
    elif word[-1] not in ['a', 'e', 'o', 'n', 's', 'r']:
        return {'pos': 'noun', 'category': 'M','gloss': 'unknown, potentially a noun, adjective, or name', 'regular': 'unknown', 'no_suffix': True, 'unknown': True}
    elif word.endswith(tuple(verbs['ar'].keys())):
        return {'pos': 'verb', 'category': 'ar', 'gloss': 'unknown', 'regular': True, 'no_suffix': False, 'unknown': True}
    elif word.endswith(tuple(verbs['er'].keys())):
        return {'pos': 'verb', 'category': 'er', 'gloss': 'unknown', 'regular': True, 'no_suffix': False, 'unknown': True}
    elif word.endswith(tuple(verbs['ir'].keys())):
        return {'pos': 'verb', 'category': 'ir', 'gloss': 'unknown', 'regular': True, 'no_suffix': False, 'unknown': True}
    else:
        return {'pos': 'noun', 'category': 'M', 'gloss': 'unknown', 'regular': True, 'no_suffix': False, 'unknown': True}

def lookup_suffix(word, content):
    if content['no_suffix'] == True:
        return None
    else:
        if content['pos'] == 'verb':
            cat = content['category']
            for index in range(0, len(word), 1):
                if word[index:] in verbs[cat].keys():
                    return word[index:]
                
        elif word.endswith(('os', 'as', 'es', 's')):
            return 's'


def create_pair(query):
    """Processes query array and words array of objects, each having content and suffix properties."""
    words = []

    for each in query:
        entry = find_stem(each)
        if entry[0] != None and entry[1] != None:
            stem = entry[0]
            content = entry[1]
            suffix = each[len(stem):]
        else:
            content = create_virtual(each)
            suffix = lookup_suffix(each, content)
            stem = each[:(len(each)-len(suffix))] if suffix != None else each

        if suffix:
            words.append({'original': each, 'content': content, 'suffix': suffix, 'parsed': (stem + '-' + suffix)})
        else:
            words.append({'original': each, 'content': content, 'suffix': None, 'parsed': None})

    parse(words)

def find_stem(word):
    """Looks up the content stem of each queried word and returns it to create_pair()."""
    entry = [None, None]

    for index in range(len(word), 0, -1):
        for key in list(content.keys()):
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
