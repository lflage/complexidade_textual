# -*- coding: utf-8 -*-
"""
Crawler para receber os textos parseados pelo Parser Sintático Palavras
"""

import os, nltk, sys
import complexidade_textual as ct
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import Select

path_to_corpus = sys.argv[1]

# Setting up Firefox
driver = webdriver.Firefox()
driver.get("https://visl.sdu.dk/visl/pt/parsing/automatic/trees.php")
assert "VISL - Tree structure" in driver.title

# Reading corpus
corpus = ct.corpus_yeeter(path_to_corpus)
#corpus = ct.corpus_yeeter('./corpora/Redações')

# Sentence tokenizer
sent_tokenizer = nltk.data.load('tokenizers/punkt/portuguese.pickle') 


for path, doc in corpus:
    # Leitura do documento
    doc.read()
    redacao = doc.get_body()
    
    # Tratamento do path
    caminho = os.path.splitext(path)
    
    parsed_sent_list = []
    for sent in sent_tokenizer.tokenize(redacao):
        try:
            #Textbox element that will receive the parsed text
            text_box = driver.find_element_by_name("text")
            text_box.clear()
            text_box.send_keys(sent)

            # Select vertical visualization from dropdown box
            visualization = Select(driver.find_element_by_name('visual'))
            visualization.select_by_visible_text("Source")

            # Click to show parsed text
            exp_down = driver.find_element_by_name("go")
            exp_down.click()

            parsed_text = driver.find_element_by_tag_name('pre')
            parsed_sent_list.append(parsed_text.text)
        except:
            print(path)
            exit()
            
    with open ("%s_parsed_%s" % (caminho[0],'.txt'), 'w') as file:
        file.write("\nsentence\n".join(parsed_sent_list))

    sleep(1.5)