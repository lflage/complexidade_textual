#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 16:10:01 2020

@author: lucas
"""


import os
import re
import nltk
#import pandas as pd
import complexidade_textual as ct
from document import Document


prog = re.compile('(\.xml)$')
prop = re.compile('(prompt)')
doc_list = []

f = []
fps = []
for dirpath, dirnames, filenames in os.walk("./corpora/Redações"):
    for filename in filenames:
        fps.append(os.path.normpath(os.path.join(dirpath,filename)))
            
for path in fps:
    if re.search(prog,path):
        f.append(path)
        doc_list.append(Document(path))
        
# Inicializando o sentence Tokeninzer
sent_tokenizer = nltk.data.load('tokenizers/punkt/portuguese.pickle') 
    
for doc in doc_list:
    doc.read()
    redacao = doc.get_body()
    # Retirando espaços em branco extras
    redacao = re.sub('\s{2,}',' ',redacao).strip()
    
    # Separacao da redação em sentenças
    sentencas = sent_tokenizer.tokenize(redacao)
    
    # Obtenção dos numeros de bigramas e trigramas
    print(ct.bi_trigram_counter(sentencas))
    