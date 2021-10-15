from document import Document
import os
import re

        
prog = re.compile('(\.xml)$')
prop = re.compile('(prompt)')
doc_list = []
sair = ""

f = []
fps = []
for dirpath, dirnames, filenames in os.walk("./Redações"):
    for filename in filenames:
        fps.append(os.path.normpath(os.path.join(dirpath,filename)))
            
for path in fps:
    if re.search(prog,path):
        f.append(path)
        doc_list.append(Document(path))
       

        
while sair != "n":
    n = int(input("Insira o número da redação a ser lida"))
    doc_list[n].read()
    print(doc_list[n].get_title())
    print(doc_list[n].get_body())
    sair = input("Deseja continuar? s ou n?")
