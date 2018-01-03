from content import content
from suffixes import verbs, nominals

output = {}

def create_output(query):
    """INC--Generates user-readable output."""
    for n in range(0, len(query)):
        output[query[n]] = 'none'

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
            ending = '???'

        parses.append('{}: {}-{}'.format(original, gloss, ending))
    
    for each in parses:
        print(each)

def create_pair(query):
    """Processes query array and words array of objects, each having content and suffix properties."""
    words = []

    for each in query:
        word = find_stem(each)
        suffix = each[(len(word)-1):]

        if suffix:
            words.append({'original': each, 'content': word, 'suffix': suffix})
        else:
            words.append({'original': each, 'content': word, 'suffix': None})

    parse(words)

def find_stem(word):
    """Looks up the content stem of each queried word and returns it to create_pair()."""
    entry = None

    for index in range(len(word), 0, -1):
        for key in content.keys():
            if key.endswith(word[0:index]):
                entry = content[key]
    
    return entry

def retrieve():
    """Requests query string from user and formats input correctly as array of words."""
    query_string = input('Enter a Spanish phrase here: ')
    query = query_string.split(' ')

    for each in query:
        each = '^' + each

    create_pair(query)

if __name__ == '__main__':
    retrieve()
