# gridutil.py
#  Some useful functions for navigating square 2d grids

DIRECTIONS = 'NESW'
ORIENTATIONS = {
    'N': (0, 1),
    'E': (1, 0),
    'S': (0, -1),
    'W': (-1, 0)
}


def next_direction(d: str, inc: int) -> str:
    return DIRECTIONS[(DIRECTIONS.index(d)+inc) % len(DIRECTIONS)]


def left_turn(d: str) -> str:
    return next_direction(d, -1)


def right_turn(d: str) -> str:
    return next_direction(d, 1)


def next_loc(loc: tuple[int, int], d: str) -> tuple[int, int]:
    x, y = loc
    dx, dy = ORIENTATIONS[d]
    return x+dx, y+dy


def legal_loc(loc: tuple[int, int], n: int) -> bool:
    x, y = loc
    return 0 <= x < n and 0 <= y < n


def generate_locations(n: int):
    for x in range(n):
        for y in range(n):
            yield x, y


def manhattan_dist(loc1: tuple[int, int], loc2: tuple[int, int]) -> int:
    x1, y1 = loc1
    x2, y2 = loc2
    return abs(x1-x2) + abs(y1-y2)


def adjacent(loc1: tuple[int, int], loc2: tuple[int, int]) -> bool:
    return manhattan_dist(loc1, loc2) == 1
