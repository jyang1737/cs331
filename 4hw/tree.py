import numpy as np



def data():
    f = open('dtree-data','r')
    d = {}
    for x in range(0,8):
        d['attr'+str(x)] = list()
    d['res'] = list()
    for line in f:
        line = line.split()
        for x in range(0,8):
            d['attr'+str(x)].append(line[x])
        d['res'].append(line[8])
    return d

def process(d):
    a = {}
    numA = 0
    numB = 0
    total = 0
    for x in d['res']:
        if (x == 'A'):
            numA += 1
        elif (x == 'B'):
            numB += 1
        total += 1
    a['S'] = (numA/total, numB/total)

    for x in range(0,8):
        true = 0
        false = 0
        total = 0
        for y in d['attr'+str(x)]:
            if (y == 'True'):
                true += 1
            elif (y == 'False'):
                false += 1
            total += 1
        a['attr'+str(x)] = (true/total, false/total)
    return a
                
def entropy(x):
    e = {}
    e['S'] = x['S'][0] * np.log2(1/x['S'][0]) +x['S'][1] * np.log2(1/x['S'][1])
    for y in range(0,8):
        e['attr'+str(y)] = x['attr'+str(y)][0] * np.log2(1/x['attr'+str(y)][0]) \
                           + x['attr'+str(y)][1] * np.log2(1/x['attr'+str(y)][1])
    return e
    
    
def main():
    d = data()
    x = process(d)
    e = entropy(x)
    print(e)
if __name__ == '__main__':
    main()
