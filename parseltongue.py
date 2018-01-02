from content import content
from suffixes import verbs

def return_parse(query):
    output = {}

    for n in range(0, len(query)):
        output[query[n]] = 'none';

    for x in output:
        print('{0}: {1}'.format(x, output[x]))

def retrieve_query():
    query_string = input('Enter a Spanish phrase here: ')
    query = query_string.split(' ')

    return_parse(query)

if __name__ == '__main__':
    retrieve_query()
