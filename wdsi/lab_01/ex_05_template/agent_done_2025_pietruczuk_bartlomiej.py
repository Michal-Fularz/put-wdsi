# prob.py
# This is
import heapq
import random
import numpy as np
import queue
from enum import Enum

from gridutil import generate_locations


class Kierunek(Enum):
    N = 0
    E = 1
    S = 2
    W = 3
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
        self.graph = {}
        self.t = 0
        self.path, self.actions = self.find_path()

    def __call__(self):

        action= self.actions[self.t]
        self.t+=1

        # select action to reach first location in self.path
        # TODO PUT YOUR CODE HER

        return action

    def heuristic(self,a, b):
        # Euclidian distance
        return np.sqrt((a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1]))
    def find_path(self):
        path = []
        visited = set()
        cost = {}
        parent = {}
        for x in range(0,16):
            for y in range(0,16):
                cost[(x,y)] = float('inf')
        cost[self.loc] = 0
        pq = [(0, self.loc,self.dir)]
        directions = [ [1, 0],[0, -1],[-1, 0],[0, 1]]
        direction_names = ["N","E","S","W"]
        while pq:
            cur_dis, cur_node,cur_dir = heapq.heappop(pq)
            if cur_node == self.goal:
                break
            if cur_node in visited:
                continue
            visited.add(cur_node)
            child_direction = -1
            for x_sum, y_sum in directions:
                child_direction+=1
                child = (cur_node[0] + x_sum, cur_node[1] + y_sum)
                if child[0]<0 or child[0]>15:
                    continue
                if child[1]<0 or child[1]>15:
                    continue
                if child in self.walls:
                    continue
                if child in visited:
                    continue
                b = Kierunek[cur_dir].value - child_direction
                move_cost = 0
                if b == 0:
                    move_cost = 1
                if b == 1 or b== -3:
                    move_cost = 3
                if b ==2 or b==-2:
                    move_cost = 5
                if b ==3 or b==-1:
                    move_cost = 6
                new_cost=cur_dis+move_cost
                old_cost = cost[child]
                heuristic = self.heuristic(child,self.goal)
                if new_cost<old_cost:
                    cost[child] = new_cost
                    parent[child] = cur_node
                    heapq.heappush(pq, (new_cost+heuristic, child,direction_names[child_direction]))
        if self.goal not in parent:
            print("Nie znaleziono ścieżki")
            return [], []
        current = self.goal
        while current != self.loc:
            path.append(current)
            current = parent[current]
        path.append(self.loc)
        path.reverse()
        actions = self.frompath_toactions(path)
        return path, actions

    def get_path(self):
        return self.path
    def frompath_toactions(self,path):
        actions = []
        parent_dir = self.dir
        child_dir = 'N'
        for i in range(0, len(path) - 1):

            parent = path[i]
            child = path[i + 1]
            x_diff = parent[0] - child[0]
            y_diff = parent[1] - child[1]
            if y_diff == 1:
                child_dir = 'S'
            if y_diff == -1:
                child_dir = 'N'
            if x_diff == 1:
                child_dir = 'E'
            if x_diff == -1:
                child_dir = 'W'
            ddd = Kierunek[parent_dir].value - Kierunek[child_dir].value
            if ddd == 0:
                actions.append('forward')
            if ddd == 1 or ddd == -3:
                actions.append('turnright')
                actions.append('forward')
            if ddd == 2 or ddd == -2:
                actions.append('turnright')
                actions.append('turnright')
                actions.append('forward')
            if ddd == 3 or ddd == -1:
                actions.append('turnleft')
                actions.append('forward')
            parent_dir = child_dir
        return actions