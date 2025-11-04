# prob.py
# This is

import random
import numpy as np
from math import sqrt
from queue import PriorityQueue
from gridutil import generate_locations

class Agent:
    def __init__(self, size, walls, loc, dir, goal):
        self.size = size
        self.walls = walls
        # list of valid locations
        self.locations = list({*generate_locations(self.size)}.difference(self.walls))
        # dictionary from location to its index in the list
        self.loc_to_idx = {loc: idx for idx, loc in enumerate(self.locations)}
        self.loc = loc
        self.dir = dir
        self.goal = goal

        self.t = 0
        self.path, self.actions = self.find_path()
        self.actual_step = 0

    def __call__(self):
        action = 'N'

        # select action to reach first location in self.path
        # TODO PUT YOUR CODE HERE
        if self.actual_step < len(self.actions):
            action = self.actions[self.actual_step]
            self.actual_step += 1
        
        
        # ------------------
    
        return action
    def locations_to_graph(self):
        graph = {}
        self.locations.sort(key=lambda x: x[0])
        for loc in self.locations:
            if loc not in graph:
                graph[loc] = []
            if loc[0] > 0 and (loc[0] - 1, loc[1]) not in self.walls:
                graph[loc].append((loc[0] - 1, loc[1]))
            if loc[0] < self.size - 1 and (loc[0] + 1, loc[1]) not in self.walls:
                graph[loc].append((loc[0] + 1, loc[1]))
            if loc[1] > 0 and (loc[0], loc[1] - 1) not in self.walls:
                graph[loc].append((loc[0], loc[1] - 1))
            if loc[1] < self.size - 1 and (loc[0], loc[1] + 1) not in self.walls:
                graph[loc].append((loc[0], loc[1] + 1))
        return graph

    def a_star_algo(self):
        def heuristic(a, b):
            # Euclidian distance
            return sqrt((a[0] - b[0])*(a[0] - b[0]) + (a[1] - b[1])*(a[1] - b[1]))
        
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        
        s = self.loc
        g = self.goal
        nodes = self.locations_to_graph()
        #print(nodes)
        # zbiór wierzchołków odwiedzonych
        visited = set()
        # słownik kosztów
        cost = {n: float('inf') for n in nodes}
        # słownik poprzedników
        parent = {n: None for n in nodes}
        # utwórz kolejke, w której elementy są ułożone nie w kolejności wprowadzania, lecz w kolejności priorytetu.
        q = PriorityQueue()
        # dodaj wierzchołek startowy
        q.put((0,s))
        cost[s] = 0
        # dopóki kolejka nie jest pusta, czyli są jeszcze jakieś wierzchołki do odwiedzenia
        while not q.empty():
            # pobierz wierzchołek o najmniejszym priotytecie i usuń go z kolejki
            _, cur_n = q.get()
            # przerwij jeśli odwiedzony
            if cur_n in visited:
                continue
            # dodaj wierzchołek do listy odwiedonych
            visited.add(cur_n)
            # przerwij jeśli dotarliśmy do celu
            if cur_n == g:
                break
            # dla wszystkich krawędzi z aktualnego wierzchołka   
            for nh in nodes[cur_n]:
                # przerwij jeśli sąsiad był już odwiedzony
                if nh in visited:
                    continue  
                # pobierz koszt sąsiada lub przypisz mu inf
                old_cost = cost[nh]
                # oblicz koszt dla danego wierzchołka
                if nh[0] > cur_n[0]:
                    new_cost = cost[cur_n] + 2
                elif nh[0] < cur_n[0]:
                    new_cost = cost[cur_n] + 5
                elif nh[1] > cur_n[1]:
                    new_cost = cost[cur_n] + 1
                else:
                    new_cost = cost[cur_n] + 4 # ruch do tyłu czyli dwa obroty w prawo 
                    
                if new_cost < old_cost:
                    # zaktualizuj wartość sąsiada w słowniku kosztów
                    cost[nh] = new_cost
                    # ustaw poprzednika
                    parent[nh] = cur_n
                    # oblicz koszt uzwględniając heurystykę
                    priority = new_cost + heuristic(g, nh)
                    # dodaj sąsiada do kolejki zgodnie z priorytetem         
                    q.put((priority, nh))
        # odtwórz ścieżkę
        path = []
        actions = []
        direct_table = []
        cur_n = g
        dir_vector = {(0, 1): 'N', (0, -1): 'S', (1, 0): 'E', (-1, 0): 'W'}

        DIRECTION_ACTIONS = {
            # (current, next): [actions]
            ('N', 'E'): ['turnright', 'forward'],
            ('N', 'W'): ['turnleft', 'forward'],
            ('E', 'S'): ['turnright', 'forward'],
            ('E', 'N'): ['turnleft', 'forward'],
            ('S', 'W'): ['turnright', 'forward'],
            ('S', 'E'): ['turnleft', 'forward'],
            ('W', 'N'): ['turnright', 'forward'],
            ('W', 'S'): ['turnleft', 'forward'],
        }
        
        while cur_n is not None:
            path.append(cur_n)
            if parent[cur_n] != None:
                par_x = parent[cur_n][0]
                par_y = parent[cur_n][1]
                cur_x = cur_n[0]
                cur_y = cur_n[1]
                direct_table.append(dir_vector[(cur_x - par_x, cur_y - par_y)])
            cur_n = parent[cur_n]
        
        direct_table.append('N')
        direct_table.reverse()
        for i in range(len(direct_table) - 1):
            current_dir = direct_table[i]
            next_dir = direct_table[i + 1]
            if current_dir == next_dir:
                actions.append('forward')
            else:
                actions.extend(DIRECTION_ACTIONS.get((current_dir, next_dir)))
        
        path.reverse()
        print(direct_table)
        print(path)
        print(actions)        
        return path, actions

    def find_path(self):
        path, actions = self.a_star_algo()
        return path, actions

    def get_path(self):
        return self.path
