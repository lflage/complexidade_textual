# -*- coding: utf-8 -*-
"""
Criado por Lucas Fonseca Lage em 04/03/2020
"""

import re, os
import spacy
from unicodedata import normalize
from gensim.models import Phrases
from document import Document

bigram_model = Phrases.load('./n_gram_models/bigram_gen_model')
trigram_model = Phrases.load('./n_gram_models/trigram_gen_model')

nlp = spacy.load('pt_core_news_sm')

freq_pos_tag = [('DET', 'NOUN', 'ADP', 'NOUN', 'ADP', 'DET', 'NOUN'),
 ('VERB', 'DET', 'NOUN', 'ADP', 'NOUN', 'ADP', 'NOUN'),
 ('VERB', 'DET', 'NOUN', 'ADP', 'DET', 'NOUN', 'PUNCT'),
 ('DET', 'NOUN', 'ADP', 'NOUN', 'ADP', 'NOUN', 'PUNCT'),
 ('NOUN', 'ADP', 'NOUN', 'ADP', 'DET', 'NOUN', 'PUNCT'),
 ('VERB', 'ADP', 'DET', 'NOUN', 'ADP', 'NOUN', 'PUNCT'),
 ('VERB', 'DET', 'NOUN', 'ADP', 'NOUN', 'ADP', 'DET'),
 ('DET', 'NOUN', 'ADP', 'DET', 'NOUN', 'ADP', 'NOUN'),
 ('NOUN', 'ADP', 'DET', 'NOUN', 'ADP', 'NOUN', 'PUNCT'),
 ('VERB', 'DET', 'NOUN', 'ADP', 'NOUN', 'ADJ', 'PUNCT')]


def corpus_reader(path):
    prog = re.compile('(\.xml)$')
    #prop = re.compile('(prompt)')
    doc_list = []

    f = []
    fps = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            fps.append(os.path.normpath(os.path.join(dirpath,filename)))
            
    for path in fps:
        if re.search(prog,path):
            f.append(path)
            doc_list.append(Document(path))
    return (doc_list,f)

def corpus_yeeter(path):
    prog = re.compile('(\.xml)$')
    #prop = re.compile('(prompt)')

    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if re.search(prog,filename):
                path = os.path.normpath(os.path.join(dirpath,filename))
                yield (path, Document(path))
                
def all_fps(path_to_dir):
    fps = []
    for dirpath, dirnames, filenames in os.walk(path_to_dir):
        for filename in filenames:
            fps.append(os.path.normpath(os.path.join(dirpath,filename)))
    return fps

def parsed_search(path, path_list):
    split_path = os.path.splitext(path)
    path_to_search = "%s_parsed_%s" % (split_path[0],'.txt')
    if path_to_search in path_list:
        return 1
    else:
        return 0


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

def n_most_freq_pos_tag_seq(sent_list):
    n = 0
    pos_list = []
    
    for i in sent_list:
        sent_nlp = nlp(i)
        sent_pos = []
        for token in sent_nlp:
            sent_pos.append(token.pos_)
        pos_list.append(sent_pos)
        
    for line in pos_list:
        if len(line) < 7:
            continue
    if len(line) >= 7:
        while len(line) >= 7:
            t = tuple(line[0:7])
            if t in freq_pos_tag:
                n+=1
            line.pop(0)
    return n


