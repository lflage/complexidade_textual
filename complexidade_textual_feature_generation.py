#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 16:10:01 2020

@author: lucas
"""


import re, nltk
#import pandas as pd
import complexidade_textual as ct


doc_list = ct.corpus_reader("./corpora/Redações")
print("corpus was read")

# Inicializando o sentence Tokeninzer
sent_tokenizer = nltk.data.load('tokenizers/punkt/portuguese.pickle') 
print('sentence tokenizer was imported')

for doc in doc_list:
    doc.read()
    redacao = doc.get_body()
    # Retirando espaços em branco extras
    redacao = re.sub('\s{2,}',' ',redacao).strip()
    print("radação foi lida")
    # Separacao da redação em sentenças
    sentencas = sent_tokenizer.tokenize(redacao)
    print("redação separada em sentenças")
    # Obtenção dos numeros de bigramas e trigramas
    print(ct.bi_trigram_counter(sentencas))

    # Obtenção do número de sequências mais frequentes
    print("Número de sequências de pos tag relevantes: %d" % ct.n_most_freq_pos_tag_seq(sentencas))