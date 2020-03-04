# -*- coding: utf-8 -*-
"""
Criado por Lucas Fonseca Lage em 04/03/2020
"""

import re
import spacy
from unicodedata import normalize

def remover_acentos(text):
    return normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')

def pre_process(text):
    # Retira espaços em branco extras
    text = re.sub('\s{2,}',' ',text).strip().lower()
    nlp = spacy.load('pt_core_news_sm')
    doc = nlp(text)
    #Retira numeros
    text = ' '.join([token.text for token in doc if token.is_alpha == True
                     and token.pos_ == 'PUNCT'])
    return remover_acentos(text)

def bigram_number(bigram_text):
    count = 0
    for token in bigram_text.split():
        if re.search(u'_',token):
            count += 1
    return count

def trigram_number(trigram_text):
    count = 0
    for token in trigram_text.split():
        if re.search(u'(?<=_).+_',token):
            count += 1
    return count