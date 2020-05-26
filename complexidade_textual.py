# -*- coding: utf-8 -*-
"""
Criado por Lucas Fonseca Lage em 04/03/2020
"""

import re
import spacy
from unicodedata import normalize
from gensim.models import Phrases

bigram_model = Phrases.load('./n_gram_models/bigram_gen_model')
trigram_model = Phrases.load('./n_gram_models/trigram_gen_model')

nlp = spacy.load('pt_core_news_sm')

def remover_acentos(text):
    return normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')

def pre_process(text):
    # Retira espaços em branco extras
    text = re.sub('\s{2,}',' ',text).strip().lower()
    
    doc = nlp(text)
    #Retira numeros
    text = ' '.join([token.text for token in doc if token.is_alpha == True
                     and token.pos_ != 'PUNCT'])
    return remover_acentos(text)

def bi_trigram_counter(sentence_list):
    # Retorna uma tupla com o numero de bigramas e trigramas
    # Recebe como entrada o texto seguimentado em sentencas
    bi_sent_list = []
    tri_sent_list = []

    
    for sentence in sentence_list:
        proc_sent = pre_process(sentence).lower().split()
        bigram_sentence = bigram_model[proc_sent]
        bi_sent_list.append(bigram_sentence)
    
    for bi_sent in bi_sent_list:
        tri_sent = trigram_model[bi_sent]
        tri_sent_list.append(tri_sent)
        
    return(bigram_number(bi_sent_list),trigram_number(tri_sent_list))
    
def bigram_number(bigram_sent_list):
    count = 0
    for sent in bigram_sent_list:
        for token in sent:
            if re.search(u'_',token):
                count += 1
    return count

def trigram_number(trigram_sent_list):
    count = 0
    for sent in trigram_sent_list:
        for token in sent:
            if re.search('(?<=_).+_',token):
                count += 1
    return count


