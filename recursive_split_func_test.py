#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 18:49:22 2020

@author: lucas
"""
import re

def recursive_split(text):
    eq_sub = re.compile(r'^=', flags=re.M)
    current_level = []
    if re.search(r'=',text):
        contents = re.split(r'\n(?=\w)',text)
        for i in contents:
            nodes = re.split(r'(^\w.+\n)', i)
            equal_remove = re.sub(eq_sub, '', nodes[2])
            current_level.append([nodes[1], recursive_split(equal_remove)])
        return current_level
    else:   
        return re.split(r'\n', text)
      
text = 'SOURCE: Running text\n1. A menina que brincava no parque perdeu a boneca\nA1\nUTT:cl(fcl)\nS:g(np)\n=D:pron(det "o" <*> <artd> DET F S) A\n=H:n("menina" F S) menina\n=D:cl(fcl)\n==S:pron(indp "que" <rel> M S) que\n==P:v(fin "brincar" IMPF 3S IND VFIN) brincava\n==A:g(pp)\n===H:prp("em" <sam-> <right>) em\n===D:g(np)\n====D:pron(det "o" <-sam> <artd> DET M S) o\n====H:n("parque" M S) parque\nP:v(fin "perder" <fmc> PS 3S IND VFIN) perdeu\nOd:g(np)\n=D:pron(det "o" <artd> DET F S) a\n=H:n("boneca" F S) boneca'


if re.search('UTT',text):
    _half = re.split('UTT.+\n',text)[1]
    _half = re.split('\n\.',_half)[0]
    arvere = ['UTT', recursive_split(_half)]

#arvere = recursive_split(text)