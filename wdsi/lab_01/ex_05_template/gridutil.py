# gridutil.py
#  Some useful functions for navigating square 2d grids

DIRECTIONS = "NESW"
ORIENTATIONS = {'N': (0, 1), 'E': (1, 0), 'S': (0, -1), 'W': (-1, 0)}

def nextDirection(d, inc):
    return DIRECTIONS[(DIRECTIONS.index(d)+inc)%len(DIRECTIONS)]

def leftTurn(d):
    return nextDirection(d, -1)

def rightTurn(d):
    return nextDirection(d, 1)

def nextLoc(loc, d):
    x,y = loc
    dx, dy = ORIENTATIONS[d]
    return (x+dx, y+dy)

def legalLoc(loc, n):
    x,y = loc
    return 0<=x<n and 0<=y<n

def locations(n):
    for x in range(n):
        for y in range(n):
            yield (x,y)

def manhatDist(loc1, loc2):
    x1,y1 = loc1
    x2,y2 = loc2
    return abs(x1-x2) + abs(y1-y2)

def adjacent(l1,l2):
    x1,y1 = l1
    x2,y2 = l2
    return (abs(x1-x2) + abs(y2-y1)) == 1

