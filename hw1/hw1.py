import time

def search(start, end):
    f = open('exampleWords.txt', 'r')
    words = f.read().split()
    current = start
    paths = {}
    paths[current] = None
    frontier = [start]
    explored = []
    letters = 'abcdefghijklmnopqrstuvwxyz'
    while (True):
        if not frontier:
            return False
        if (current == end):
            path = [current]
            prevword = current
            
            while prevword != start:
                parent = paths[prevword]
                path.append(parent)
                prevword = parent

            path.reverse()
            return path
        
        explored.append(current)
        for x in range(len(current)):
            for y in range(len(letters)):
                newword = current[0:x] + letters[y] + current[x+1:len(current)]
                if (newword in words):
                    if (newword not in explored):
                        paths[newword] = current
                        frontier.append(newword)
                        explored.append(newword)
        current = frontier[0]
        frontier = frontier[1:]

if __name__ == '__main__':
    print(search('cold','warm'))
    print(search('small','short'))
