#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 16:10:01 2020

@author: lucas
"""

import nltk, spacy, re
#import pandas as pd
import complexidade_textual as ct


# # Carregamento dos modelos de bigramas e trigramas
# bigram_model = Phrases.load('./n_gram_models/bigram_gen_model')
# trigram_model = Phrases.load('./n_gram_models/trigram_gen_model')

# # Carregamento do modelo Spacy
# nlp = spacy.load('pt_core_news_lg')

# Inicializando Corpus
corpus = ct.corpus_yeeter("./corpora/Redações")

# Inicializando o sentence Tokeninzer
sent_tokenizer = nltk.data.load('tokenizers/punkt/portuguese.pickle')

for path, doc in corpus:
    doc.read()
    redacao = doc.get_body()
    # Retirando espaços em branco extras
    redacao = re.sub('\s{2,}',' ',redacao).strip()
    print("redação foi lida")
    # Separacao da redação em sentenças
    sentencas = sent_tokenizer.tokenize(redacao)
    print("redação separada em sentenças")
    # Obtenção dos numeros de bigramas e trigramas
    print("número de bigramas e trigramas: %d" % ct.bi_trigram_counter(sentencas))

    # Obtenção do número de sequências mais frequentes
    print("Número de sequências de pos tag relevantes: %d" % ct.n_most_freq_pos_tag_seq(sentencas))

    # Número de elementos no sujeito
    print("Número de elementos no sujeito: %d" % ct.subj_n_elements(sentencas))
