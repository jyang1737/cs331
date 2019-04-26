import random, math, sys, pickle, predict
language = ['en','nl']
max_depth = 5

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

        if (x.find(' het ') != -1):
            attr['het'] = True
        else:
            attr['het'] = False

        if (x.find('uu') != -1):
            attr['uu'] = True
        else:
            attr['uu'] = False

        if (x.find('euw') != -1):
            attr['euw'] = True
        else:
            attr['euw'] = False


        letter = x[0]
        ctr = 0
        for c in x[1:]:
            if (letter == c):
                ctr += 1
            letter = c
        if (ctr > 2):
            attr['double'] = True
        else:
            attr['double'] = False
        
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
def importance(attr, ex, learning):
    gain = dict()
    nl = 0
    total = len(ex)
    for x in ex:
        if (ex[x]['lan'] == 'nl'):
            nl += 1
    totalE = entropy(nl/total)

    #may need to change depending on attributes
    for a in attr: #name of attribute
        totalAttr = 0
        remainder = 0
        nl = 0
        en = 0
        for x in ex: #line of text
            if (ex[x]['attr'][a]):
                totalAttr += 1
                if (ex[x]['lan'] == 'nl'):
                    nl += 1
                #else:
                 #   en += 1
            '''
            else:
                totalAttr += 1
                if (ex[x]['lan'] == 'nl'):
                    nl += 1
                else:
                    en += 1
            '''     
        #print(a)
        #print(totalAttr)
        #print(nl)
        #print(en)
        if (totalAttr != 0):
            singleremainder = (totalAttr/total) * entropy(nl/(totalAttr))
            remainder += singleremainder
        
        gain[a] = totalE - remainder

    #print(gain)
    return gain

def maxgain(gain):
    max = list(gain.keys())[0]
    maxval = gain[max]
    for x in gain:
        if (gain[x] > maxval):
            max = x
            maxval = gain[x]
    return max

def dtree(ex, attr, parent_ex, ctr):
    ctr = 0
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
    elif not attr or ctr >= max_depth:
        return plurality(ex)
    else:
        a = maxgain(importance(attr, ex, 'dt'))
        #print(a)
        tree = {a:dict()}
        #change later to accommodate for different attributes
        for choice in attr[a]:
            exs = {x:ex[x] for x in ex if ex[x]['attr'][a] == choice}
            #print(list(exs.values()))
            #print(attr)
            #print(ex)
            newattr = dict(attr)
            newattr.pop(a)
            subtree = dtree(exs, newattr, ex, ctr+1)
            tree[a][choice] = subtree
        return tree

def adaboost(ex, attr, k):
    n = len(ex)
    for x in ex:
        ex[x]['w'] = 1/n

    h = list()
    z = list()
    for i in range(0,k):
      
        h.append(dtree(ex, attr, list()))
        error = 0
        for x in ex:
            if (predict.process(x, h[i]) != ex[x]['lan']):
                error += ex[x]['w']
        if (error == 0):
            break
        for x in ex:
            if (predict.process(x, h[i]) == ex[x]['lan']):
                ex[x]['w'] *= error/(1-error)
        totalweight = 0
        for x in ex:
            totalweight += ex[x]['w']
        for x in ex:
            ex[x]['w'] /= totalweight
        z.append(math.log((1-error)/error))

    maxweight = z[0]
    maxpos = 0
    for i in range(0,k):
        if (z[i] > maxweight):
            maxweight = z[i]
            maxpos = z[i]
    return h[maxpos]
        
        
    
def main():
    examples = open(sys.argv[1], 'r')
    hypothesis = open(sys.argv[2], 'wb')
    learning = sys.argv[3]
    ex = process(examples)
    ex = attributeprocess(ex)
    attributes = {'ij':[True, False], 'aa':[True, False], 'de':[True, False], 'het':[True, False], 'uu':[True, False], 'euw':[True, False], 'double':[True, False]}

    #print(ex)
    #for x in ex:
     #   print(ex[x]['attr']['het'])
    if (learning == 'dt'):
        tree = dtree(ex, attributes, list(), 0)
    elif (learning == 'ada'):
        tree = adaboost(ex, attributes, 10)
    pickle.dump(tree, hypothesis)
if __name__ == '__main__':
    main()
