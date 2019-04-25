import random, math, sys
language = ['en','nl']

def process(f):
    x = dict()
    for line in f:
        line = line.strip()
        line = line.split('|')
        x[line[1].lower()] = {'lan':line[0]}
    return x

def attributeprocess(data):
    for x in data:
        attr = dict()
        if (x.find('ij') != -1):
            attr['ij'] = True
        else:
            attr['ij'] = False
            
        if (x.find('aa') != -1):
            attr['aa'] = True
        else:
            attr['aa'] = False
            
        if (x.find(' de ') != -1):
            attr['de'] = True
        else:
            attr['de'] = False

        data[x]['attr'] = attr

    return data
                    

def plurality(ex):
    res = dict()
    for lan in language:
        res[lan] = 0
    for x in ex:
        if ex[x]['lan'] == 'en':
            res['en'] += 1
        else:
            res['nl'] += 1
    if (res['en'] > res['nl']):
        return 'en'
    elif (res['en'] < res['nl']):
        return 'nl'
    else:
        return random.choice(language)

def entropy(q):
    if (q == 1 or q == 0):
        return 0
    b = -(q * math.log(q,2) + (1-q) * math.log(1-q, 2))
    return b

#finish tomorrwo
def importance(attr, ex):
    gain = dict()
    nl = 0
    total = len(ex)
    for x in ex:
        if (ex[x]['lan'] == 'nl'):
            nl += 1
    totalE = entropy(nl/total)

    remainder = 0
    #may need to change depending on attributes
    for a in attr: #name of attribute
        print(a)
        totalAttr = 0
        nl = 0
        en = 0
        for x in ex: #line of text
            if (ex[x]['attr'][a]):
                totalAttr += 1
                if (ex[x]['lan'] == 'nl'):
                    nl += 1
                else:
                    en += 1
                    
        
        remainder += (totalAttr/total) * entropy(nl/(nl+en))
        
    gain[a] = totalE - remainder

    print(gain)
    return gain

def maxgain(gain):
    max = list(gain.keys())[0]
    maxval = gain[max]
    for x in gain:
        if (gain[x] > maxval):
            max = x
            maxval = gain[x]
    return max

def dtree(ex, attr, parent_ex):
    if not ex:
        return plurality(parent_ex)
    
    test = True
    initial = list(ex.values())[0]['lan']
    for x in ex:
        if (ex[x]['lan'] != initial):
            test = False
            break
    if test:
        return initial
    elif not attr:
        return plurality(ex)
    else:
        a = maxgain(importance(attr, ex))
        print(a)
        tree = {a:dict()}
        #change later to accommodate for different attributes
        for choice in attr[a]:
            exs = {x:ex[x] for x in ex if ex[x]['attr'][a] == choice}
            #print(list(exs.values()))
            #print(attr)
            #print(ex)
            newattr = dict(attr)
            newattr.pop(a)
            subtree = dtree(exs, newattr, ex)
            tree[a][choice] = subtree
        return tree

def main():
    examples = open(sys.argv[1], 'r')
    hypothesis = sys.argv[2]
    learning = sys.argv[3]
    ex = process(examples)
    ex = attributeprocess(ex)
    attributes = {'ij':[True, False], 'aa':[True, False], 'de':[True, False]}

    #print(ex)
    tree = dtree(ex, attributes, list())
    print(tree)
if __name__ == '__main__':
    main()
