import pickle, sys

def process(line, tree):
    curkey = list(tree.keys())[0]
    curtree = tree
    attr = attributeprocess(line)
    while (curtree != 'nl' and curtree != 'en'):
        curtree = curtree[curkey][attr[curkey]]
        if (curtree != 'nl' and curtree != 'en'):
            curkey = list(curtree.keys())[0]
    return curtree

def attributeprocess(line):
    attr = dict()
    if (line.find('ij') != -1):
        attr['ij'] = True
    else:
        attr['ij'] = False
        
    if (line.find('aa') != -1):
        attr['aa'] = True
    else:
        attr['aa'] = False
        
    if (line.find(' de ') != -1):
        attr['de'] = True
    else:
        attr['de'] = False

    if (line.find(' het ') != -1):
        attr['het'] = True
    else:
        attr['het'] = False

    if (line.find('uu') != -1):
        attr['uu'] = True
    else:
        attr['uu'] = False
        
    if (line.find('ieuw') != -1):
        attr['euw'] = True
    else:
        attr['euw'] = False


    letter = line[0]
    ctr = 0
    for c in line[1:]:
        if (letter == c):
            ctr += 1
        letter = c
    if (ctr > 2):
        attr['double'] = True
    else:
        attr['double'] = False
            
    return attr

def main():
    hypothesis = open(sys.argv[1], 'rb')
    text = open(sys.argv[2], 'r')

    tree = pickle.load(hypothesis)
    print(tree)
    en = 0
    nl = 0
    for line in text:
        line = line.strip()
        line = line.lower()
        #print(line)
        res = process(line,tree)
        '''
        if (res == 'en'):
            en += 1
        else:
            nl += 1
        '''
        print(res)
    #print('en: ' + str(en))
    #print('nl: ' + str(nl))
        
        
    
    
if __name__ == '__main__':
    main()
