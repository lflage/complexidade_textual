from lxml import etree
import re
from nltk.tokenize import sent_tokenize, word_tokenize

parser = etree.XMLParser()

class Document:

    def __init__(self, name):

        self.__fname = name
        self.__doc = {}
        self.sent_lst = []

        # conll constants
        self.__ID_index = 0
        self.__TOKEN_index = 1
        self.__POS_index = 4
        self.__NODEID_index = 6
        self.__EDGE_index = 7
        

    def process_body(self, node):               # como referenciar os nós?
        """
          Recursevely it gets node body text
        """

        # recursively getting the node body
        pairs_wrong_right = []
        q = node.getchildren()
        if node.text:
            essay_text = node.text # the original text of the student 
        else:
            essay_text = ""

        tail = []                                                               
        if node.tail is not None:               
            tail_node = etree.Element("p")      
            tail_node.text = node.tail          
            tail = [tail_node]                  
        q = q + tail                            
        wrong_content = None

        while q != []:
            n = q.pop(0)

            if n.tag == "correct":
                pairs_wrong_right.append((wrong_content, n.text))       # Insere dois valores?
                wrong_content = None
            else:
                if n.tag == "wrong":
                    wrong_content = n.text
                else:
                    if wrong_content is not None:
                        # wrong content without correction
                        pairs_wrong_right.append((wrong_content,None))
                        wrong_content = None
                if n.text:
                    essay_text = essay_text + " " + n.text.strip()
      
                
            if n.tail is not None:
                essay_text = essay_text + " " + n.tail.strip()
        return (essay_text, pairs_wrong_right) 

    def process_skills(self, node):

        q = node.getchildren()
        skills_lst = []
        gradere = re.compile("[0-9][0-9]*,[0-9]|[0-9][0-9]*.[0-9]")

        while q != []:
           n = q.pop(0)

           if n.tag == "skill":
               childrenn = n.getchildren()
               desc = None
               grade = None
               for s in childrenn:
                  if s.tag == "desc":
                      desc = s.text.strip()
                  if s.tag == "grade":
                      number = gradere.search(s.text)
                      try:
                          number = number.group()
                          grade = float(number.replace(",","."))
                      except AttributeError:
                          desc = s.text.strip()
                  skills_lst.append((desc, grade))
        return skills_lst

    def read_conll(self):                   

        file_conll = self.__fname

        fd_conll = open(file_conll, "r")

        sent = []

        for l in fd_conll:
            token_lst = l.replace('\n', '').split()
            if len(token_lst) == 0:
                 self.sent_lst.append(sent)
                 sent = []
            else:
                 tok_id = token_lst[self.__ID_index]
                 tok = token_lst[self.__TOKEN_index]
                 pos = token_lst[self.__POS_index]
                 nodeid = token_lst[self.__NODEID_index]
                 edge = token_lst[self.__EDGE_index]
                 sent.append((tok_id, tok, pos, nodeid, edge))
        fd_conll.close()

    def read_prompt(self, file_prompt):

        tree = etree.parse(file_prompt, parser)
        self.__doc["prompt_title"] = tree.xpath('//title/text()')[0]
        self.__doc["prompt_body"] = tree.xpath('//body/text()')[0]

    def read(self):

        # print("--> ", self.__fname)
        tree = etree.parse(self.__fname, parser)
        root = tree.getroot()
        q = root.getchildren()
        while q != []:
            n = q.pop()
            if n.tag == "body":
                essay_text, pairs_wrong_right = self.process_body(n)
                self.__doc[n.tag] = essay_text
                self.__doc["corrections"] = pairs_wrong_right
                # print(self.__doc[n.tag])
            elif n.tag == "skills":
                self.__doc["skills"] = self.process_skills(n)
            else:
                self.__doc[n.tag] = self.process_title(n)
        #if len(self.__doc.keys())!=7:
        #    print(self.__fname)

    def process_title(self, node):

        q = node.getchildren()
        txt_title = ""

        if node.text is not None:
            txt_title = txt_title + " " + node.text

        while q != []:
            n = q.pop(0)

            if n.tag == "wrong":

                if n.text is not None:
                    txt_title = txt_title + " " + n.text 

                if n.tail is not None:
                    txt_title = txt_title + " " + n.tail

                q = q + n.getchildren()

        if node.tail is not None:
            txt_title = txt_title + " " + node.tail
        
        return txt_title

    def get_prompttitle(self):
        return self.__doc["prompt_title"]

    def get_promptbody(self):
        return self.__doc["prompt_body"]

    def get_skills(self):
        return self.__doc["skills"]

    def get_finalgrade(self):
        return self.__doc["finalgrade"].strip()

    def get_title(self):
        return self.__doc["title"]

    def get_body(self):
        return self.__doc["body"]

    def get_generalcomment(self):
        return self.__doc["generalcomment"]

    def get_fname(self):
        return self.__fname

    def get_specificaspects(self):
        return self.__doc["specificaspects"]

    def num_sentences(self):
        sent_list = sent_tokenize(self.__doc["body"])
        return len(sent_list)

    def num_words(self):
        word_list = word_tokenize(self.__doc["body"])
        return len(word_list)

    def num_words_specificaspects(self):
        word_list = word_tokenize(self.__doc["specificaspects"])
        return len(word_list)

    def num_words_generalcomment(self):
        word_list = word_tokenize(self.__doc["generalcomment"])
        return len(word_list)

    def num_words_comments(self):
        return self.num_words_specificaspects() + \
               self.num_words_generalcomment()



    