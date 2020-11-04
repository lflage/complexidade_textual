#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 16:10:01 2020

@author: lucas
"""

import nltk, spacy, re, csv,sys
import pandas as pd
import complexidade_textual as ct
from requests.exceptions import ConnectionError


try:
    csv_file = pd.read_csv('./out_files/ct_features.csv')
    csv_file = csv_file.dropna()
    cached_files = csv_file['path'].values
except FileNotFoundError:
    with open('./out_files/ct_features.csv', mode='w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(
        ['path','n_bigram','n_trigram','n_freq_pos_seq','n_subj_el_big',
        'n_subj_el_total', 'hypernym_count','hypernym_count_sent',
        'hyponyms_count','hyponyms_count_sent']
        )
        pass

# Inicializando Corpus
corpus = ct.corpus_yeeter("./corpora/Redações")

# Inicializando o sentence Tokeninzer
sent_tokenizer = nltk.data.load('tokenizers/punkt/portuguese.pickle')
print(len(cached_files))
csv_file = open('./out_files/ct_features.csv', mode='a')
writer = csv.writer(csv_file)
try:
    for path, doc in corpus:
        if path in cached_files:
            print('pulado')
            continue
        row = []
        row.append(path)
        doc.read()
        redacao = doc.get_body()
        # Retirando espaços em branco extras
        redacao = re.sub('\s{2,}',' ',redacao).strip()
        print("redação foi lida")
        # Separacao da redação em sentenças
        sentencas = sent_tokenizer.tokenize(redacao)
        print("redação separada em sentenças")
        # Obtenção dos numeros de bigramas e trigramas
        row.extend(ct.bi_trigram_counter(sentencas))
        # Obtenção do número de sequências mais frequentes
        row.append(ct.n_most_freq_pos_tag_seq(sentencas))
        # Número de elementos no sujeito
        row.extend(ct.subj_n_elements(sentencas))
        # Número de hiperonimos e hiponimos
        row.extend(ct.hypo_hyper_count(sentencas))
        writer.writerow(row)



except (KeyboardInterrupt,ConnectionError) as e:
    print("Shutdown requested...exiting")
    if len(row) != 10:
        csv_file.close()
        print('não fechou a linha')
        pass
    else:
        writer.writerow(row)
        csv_file.close()
        print('fechou a linha')
    sys.exit()
