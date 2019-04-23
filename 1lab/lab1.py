import sys
from PIL import Image
from heapq import *
import math

terrains = {(248,148,18,255):1.5,     #open land
            (255,192,0,255):3,      #rough meadow
            (255,255,255,255):4,    #easy forest
            (2,208,60,255):5,         #slow forest
            (2,136,40,255):6,       #walk forest
            (5,73,24,255):10,         #impassible veg
            (0,0,255,255):10,         #lake/swamp
            (153,230,255,255):1,      #ice
            (102,64,42,255):7,         #mud
            (71,51,3,255):1,          #paved road
            (0,0,0,255):1,          #footpath
            (205,0,101,255):100       #out of bounds
            }
#U, UR, R, DR, D, DL, L, UL
dx = [0, 1, 1, 1, 0, -1, -1, -1]
dy = [1, 1, 0, -1, -1, -1, 0, 1]

#pixel conversion
xpix = 10.29
ypix = 7.55

'''
Algorithm Functions
'''

def heuristic(elevationpix, start, end):
    distX = abs(start[0] - end[0]) * xpix
    distY = abs(start[1] - end[1]) * ypix
    distZ = abs(elevationpix[start[0]][start[1]] - elevationpix[end[0]][end[1]])
    return math.sqrt(distX * distX + distY * distY + distZ * distZ)

def heuristicT(terrainpix, elevationpix, start, end):
    distX = abs(start[0] - end[0]) * xpix
    distY = abs(start[1] - end[1]) * ypix
    distZ = abs(elevationpix[start[0]][start[1]] - elevationpix[end[0]][end[1]])
    elevationadj = 1
    if (distZ >= 1):
        elevationadj = distZ
    terrainadj = terrains[terrainpix[start[0], start[1]]]
    return math.sqrt(distX * distX + distY * distY) * terrainadj + elevationadj

def distance(dir):
    distX = abs(dx[dir]) * xpix
    distY = abs(dy[dir]) * ypix
    return math.sqrt(distX * distX + distY * distY)

def astar(terrainpix, elevationpix, start, end):
    camefrom = {}
    closeset = set()
    gscore = {start:0}
    fscore = {start:heuristicT(terrainpix, elevationpix, start, end)}
    xcor = start[0]
    ycor = start[1]
    openset = [(fscore[start], (xcor,ycor))]
    while (len(openset) != 0):
        cur = heappop(openset)[1]
        if (cur[0] == end[0] and cur[1] == end[1]):
            data = []
            while cur in camefrom:
                data.append(cur)
                cur = camefrom[cur]
            return data

        closeset.add(cur)

        for i in range(8):
            newX = cur[0] + dx[i]
            newY = cur[1] + dy[i]
            if (not (0 < newX < 395 and 0 < newY < 500)):
                continue

            neighbor = (newX, newY)
            estgvalue = gscore[cur] + heuristicT(terrainpix, elevationpix, cur, neighbor)
                      
            if (neighbor in closeset and estgvalue >= gscore.get(neighbor, 0)):
                continue

            if (estgvalue < gscore.get(neighbor,0) or neighbor not in [i[1] for i in openset]):
               camefrom[neighbor] = cur
               gscore[neighbor] = gscore[cur] + distance(i)
               fscore[neighbor] = gscore[cur] + heuristicT(terrainpix, elevationpix, neighbor, end)
               heappush(openset, (fscore[neighbor], neighbor))
    return False

'''
Image modifying functions
'''

def winter(terrainpix):
    edges = []
    for i in range(395):
        for j in range(500):
            cur = (i, j)
            if (terrainpix[cur[0], cur[1]] != (0,0,255,255)):
                for k in range(8):
                    if (terrainpix[cur[0], cur[1]] != (153, 230, 255, 255)):
                        if not (0 <= cur[0]+dx[k] < 395 and 0 <= cur[1]+dy[k] < 500):
                            continue
                        if (terrainpix[cur[0]+dx[k], cur[1]+dy[k]] == (0,0,255,255)):
                            edges.append(cur)
    bfs(terrainpix,edges)
    return True

def bfs(terrainpix, edges):
    openlist = {}
    for pix in edges:
        openlist[pix] = 0
    closelist = []
    
    while (len(openlist) != 0):
        cur = list(openlist.keys())[0]
        if (cur in closelist):
            openlist.pop(cur)
            continue
        for i in range(8):
            nxt = (cur[0] + dx[i], cur[1] + dy[i])
            if not (0 <= nxt[0] < 395 and 0 <= nxt[1] < 500):
                continue
            if (openlist[cur]+1 > 7):
                continue
            if ((nxt[0],nxt[1]) in openlist):
                if (openlist[(nxt[0], nxt[1])]+1 > openlist[cur]):
                    continue
            if (terrainpix[nxt[0],nxt[1]] != (0,0,255,255)) and (terrainpix[nxt[0],nxt[1]] != (153, 230, 255, 255)):
                continue
            else:
                openlist[nxt] = openlist[cur] + 1
        if (terrainpix[cur[0],cur[1]] == (0,0,255,255)):
            terrainpix[cur[0],cur[1]] = (153, 230, 255, 255)
        openlist.pop(cur)
        closelist.append(cur)
    return True
                

def spring(terrainpix, elevationpix):
    flooded = []
    edges = []
    for i in range(395):
        for j in range(500):
            cur = (i, j)
            if (terrainpix[cur[0], cur[1]] == (0,0,255,255)):
                for k in range(8):
                    if not (0 <= cur[0]+dx[k] < 395 and 0 <= cur[1]+dy[k] < 500):
                        continue
                    if (terrainpix[cur[0]+dx[k], cur[1]+dy[k]] != (0,0,255,255)):
                        edges.append(cur)
    bfsS(terrainpix, elevationpix, flooded, edges)
    flood(terrainpix, flooded)
    return True

def bfsS(terrainpix, elevationpix, flooded, edges): 
    openlist = {}
    for pix in edges:
        openlist[pix] = 0
    closelist = []

    while (len(openlist) != 0):
        cur = list(openlist.keys())[0]
        origheight = elevationpix[cur[0]][cur[1]]    
        
        if (cur in closelist):
            openlist.pop(cur)
            continue
        for i in range(8):
            nxt = (cur[0] + dx[i], cur[1] + dy[i])
            if not (0 <= nxt[0] < 395 and 0 <= nxt[1] < 500):
                continue
            if (terrainpix[nxt[0],nxt[1]] == (0,0,255,255) or terrainpix[nxt[0],nxt[1]] == (205,0,101,255)):
                continue
            if (openlist[cur]+1 > 15):
                continue
            if ((nxt[0],nxt[1]) in openlist):
                if (openlist[(nxt[0], nxt[1])]+1 > openlist[cur]):
                    continue
            openlist[nxt] = openlist[cur] + 1
            if (terrainpix[cur[0],cur[1]] != (0,0,255,255)):
                if (elevationpix[nxt[0]][nxt[1]] - origheight <= 1):
                    flooded.append(nxt)
                else:
                    temp = (nxt[0], nxt[1])
                    openlist.pop(temp)
                    closelist.append(temp)
        openlist.pop(cur)
        closelist.append(cur)
    return True

def flood(terrainpix, pixels):
    for i in pixels:
        terrainpix[i[0],i[1]] = (102,64,42,255)
    return True

def drawpaths(pixels, path):
    for x in path:
        pixels[x[0],x[1]] = (255, 0, 0, 255)

def drawpoints(pixels, points):
    for x in points:
        for i in range(8):
            pixels[x[0]+dx[i],x[1]+dy[i]] = (150, 150, 150, 255)

def getdistance(path):
    total = 0
    if (len(path) > 0):
        initial = path[0]
        for x in path:
            distX = abs(initial[0] - x[0]) * xpix
            distY = abs(initial[1] - x[1]) * ypix
            total +=  math.sqrt(distX * distX + distY * distY)
            initial = x
    return total

def main():
    global terrains
    terrain = Image.open(sys.argv[1])
    terrainpix = terrain.load()
    elevation = open(sys.argv[2], 'r')
    path = open(sys.argv[3], 'r')
    season = sys.argv[4]
    output = sys.argv[5]

    elevationpix = list()
    line = elevation.readline()
    vals = line.split()
    for i in range(0,395):
        elevationpix.append([float(vals[i])])
    for line in elevation:
        vals = line.split()
        for i in range(0,395):
            elevationpix[i].append(float(vals[i]))

    points = list()
    for line in path:
        vals = line.split()
        points.append((int(vals[0]),int(vals[1])))

    if (season == 'winter'):
        winter(terrainpix)

    if (season == 'spring'):
        spring(terrainpix, elevationpix)

    if (season == 'fall'):
        terrains[(2,136,40,255)] = 6
        
    initpoint = points[0]
    result = []
    for i in range(1, len(points)):
        result.extend(astar(terrainpix, elevationpix, initpoint, points[i]))
        initpoint = points[i]

    drawpaths(terrainpix, result)
    drawpoints(terrainpix, points)
    terrain.save(output)
    print("Path length: " + str(getdistance(result)))
            
if __name__ == '__main__':
    main()
