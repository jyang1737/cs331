import random, math
language = ['en','nl']
attributes = {attrname:choices}

def plurality(ex):
    res = dict()
    for lan in language:
        res[lan] = 0
    for x in ex:
        if ex[x] == 'en':
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
    b = -(q * math.log(q,2) + (1-q) * math.log(1-q, 2))
    return b

#finish tomorrwo
def importance(attr, ex):
    gain = dict()
    en = 0
    total = 0
    for x in ex:
        if (ex[x] == 'en'):
            en += 1
        total += 1
    
    for a in attr:
        
def dtree(ex, attr, parent_ex):
    if not ex:
        return plurality(parent_ex)
    elif all(x == list(ex.keys)[0] for x in ex.values()):
        return list(ex.values())[0]
    elif not attr:
        return plurality(ex)
    else:
        a = maxgain(importance(attr, ex))
        tree = {a:dict()}
        #change later to accommodate for different attributes
        for choice in attributes[a]:
            exs = {x:ex[x] for x in ex if ex[x] == choice}
            subtree = dtree(exs, attr.pop(a), ex)
            tree[a][choice] = subtree
        return tree

def main():
    return

if __name__ == '__main__':
    main()
