import re

def recursive_split(text):
    eq_sub = re.compile(r'^\W', flags=re.M)
#    while re.search(r'^=',text):
#        text = re.sub(eq_sub, '', text)
    current_level = []
    contents = re.split(r'\n(?=\w)',text)
    for i in contents:
        if re.search('=', i):
            try:
                nodes = re.split(r'(^\w.+\n)', i)
                next_level = nodes[2]
                while re.search(r'=',next_level):
                    next_level = re.sub(eq_sub, '', next_level)
                current_level.append([nodes[1], recursive_split(next_level)])
            except:
                print('its time to stop')

        else:
            current_level.append([i])
    return current_level

def list_tree(path):
    split_path = os.path.splitext(path)
    parsed_path = "%s_parsed_%s" % (split_path[0],'.txt')
    utt_list = []
    with open(parsed_path,mode='r', encoding='utf8') as file:

        trees = re.sub(r'=-','==', file.read(), flags=re.M)
        trees = re.sub(r'^=+\"=+','',trees, flags=re.M)
        trees = re.sub(r'^\n\W+,','',trees, flags=re.M)

        utts = re.split(r'\nsentence\n', trees)
        for i in utts:
            if re.search('UTT',i):
                #não existem apenas UTTs nas redaçoes, averiguar
                half = re.split('UTT.+\n',i)[1]
                half = re.split('\n\.',half)[0]
                arvere = ['UTT', recursive_split(half)]
                utt_list.append(arvere)
    return utt_list

def adjust_conll(path):
    with open(path, 'r+') as file:
        split_path = os.path.splitext(path)
        new_conll_path = "%s_adaptado%s" % (split_path[0],'.conll')
        with open(new_conll_path,'w+') as f:
            for line in file.readlines():
                if line.startswith('<'):
                    continue
                elif re.search(r'^\d',line):
                    text = line.strip().split('\t')
                    text.extend(['_','_'])
                    f.write('\t'.join(text)+'\n')
                else:
                    f.write(line)
    with open(new_conll_path,'r') as f:
        text = f.read()
        text = re.sub(r'\n\s*\n', '\n\n',text)

    with open(new_conll_path,'w') as f:
        for sent in text.strip().split('\n\n'):
            lines = sent.strip().split('\n')
            if re.search(r'^\D',sent, flags=re.M):
                continue
            for line in lines:
                f.write(line+'\n')
            f.write('\n\n')
    return

def train_test_conll(path):
    split_path = os.path.splitext(path)
    train_path = "%s_train%s" % (split_path[0],'.conll')
    test_path = "%s_test%s" % (split_path[0],'.conll')

    with open(path,'r', encoding='utf-8') as f:
        sentences = f.read().strip().split('\n\n')
        train,test = train_test_split(sentences)

    with open(train_path,'w', encoding='utf-8') as f:
        f.write('\n\n'.join(train))
    with open(test_path,'w', encoding='utf-8') as f:
        f.write('\n\n'.join(test))

def parsed_search(path, path_list):
    split_path = os.path.splitext(path)
    path_to_search = "%s_parsed_%s" % (split_path[0],'.txt')
    if path_to_search in path_list:
        return 1
    else:
        return 0
