import requests
from nltk.corpus import wordnet as wn

def to_pulo(ss_list, pos='NOUN'):
    pulo_off=[]
    for ss in ss_list:
        to_list = str(ss.offset())
        for i in range(8 - len(to_list)):
            to_list = '0' + to_list
        to_list = 'por-30-'+ to_list + '-n'
        pulo_off.append(to_list)
    print(pulo_off)
    return pulo_off

def req_parse(response):
    '''Parseia a lista de synsets e retorna uma lista de tuplas contendo POS e offset para o Wordnet'''
    return response.split('-')[-2].replace('0','')

def get_gloss(ss, lang='por'):
    pulo='http://wordnet.pt/api/gloss/%s' % ss
    gloss_dict = requests.get(pulo).json()
    if 'gloss' in gloss_dict.keys():
        return gloss_dict['gloss']
    else:
        return None

def my_lesk(context_setence, amb_word, lang='por',synsets=None):
    context = set(context_setence)
    if synsets == None:
        synsets = wn.synsets(amb_word,lang=lang)
    if not synsets:
        return None
    #pulo_ss = zip(synsets,to_pulo(synsets))
    pulo_ss = to_pulo(synsets)
    _, sense = max(
    (len(context.intersection(get_gloss(ss).split())),ss) for ss in pulo_ss
    )
    sense = wn.synset_from_pos_and_offset('n',int(req_parse(sense)))
    return sense
