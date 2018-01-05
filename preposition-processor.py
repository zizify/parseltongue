preps = """a-to, at;a través de-across;a la derecha de-to the right of;a la izquierda de-to the left of;al lado de-next to;afuera de-outside of;alrededor de-around;antes de-before;por encima de-above;bajo-under;cerca de-near;con-with;contra-against;de-of, from;debajo de-below;enfrente de-in front of;desde-from, since;dentro de-inside of;despues de-after;detrás de-behindf;durante-during, for;en-in, at;en lugar de-instead of;en medio de-amid;encima de-on top of;entre-between, among;fuera de-outside of;hacia-toward(s);hasta-until;lejos de-far from;más allá de-beyond;mediante-by means of;para-for, in order to;por-by, through, for;según-depending on, according to;sin-without;sobre-on/about"""

def process(some_string):
    words = {}
    prep_list = some_string.split(';')
    
    for each_string in prep_list:
        each = each_string.split('-')
        stem = each[0]
        gloss = each[1]

        words[stem] = {
                'pos': 'particle',
                'category': 'irregular',
                'gloss': gloss,
                'regular': False,
                'parse': ''
            }

    with open("preplist.py", "w") as f:
        print(words, file=f)

if __name__ == '__main__':
    process(preps)