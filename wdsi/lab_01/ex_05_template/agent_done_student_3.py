import random
import numpy as np
import queue

from gridutil import *


class Agent:
    def __init__(self, size, walls, loc, dir, goal):
        self.size = size
        self.walls = walls
        # Lista dostępnych lokalizacji
        self.locations = list({*generate_locations(self.size)}.difference(self.walls))
        # Słownik mapujący lokalizację na indeks
        self.loc_to_idx = {loc: idx for idx, loc in enumerate(self.locations)}
        self.loc = loc
        self.dir = dir
        self.goal = goal

        self.t = 0  # Czas potrzebny do osiągnięcia celu
        self.path, self.actions = self.find_path()

    def __call__(self):
        # Zwróć następną akcję z wyliczonej ścieżki
        return self.actions.pop(0) if self.actions else 'N'

    def find_path(self):
        path = []
        actions = []

        visited = set()
       
        my_queue = queue.PriorityQueue()  
        my_queue.put((0, self.loc, self.dir, [], []))  # (priorytet, loc, dir, path, actions)
        visited.add((self.loc, self.dir))

        while not my_queue.empty():
            total_cost, loc, dir, current_path, current_actions = my_queue.get()  

            if loc == self.goal:
                path = current_path
                actions = current_actions
                break

            for action in ['turnleft', 'turnright', 'forward']:
                new_loc, new_dir, action_time = self.apply_action(loc, dir, action)
                
                # sciany i notvisited
                if new_loc not in self.walls and (new_loc, new_dir) not in visited:
                    visited.add((new_loc, new_dir))
                    new_path = current_path + [new_loc]
                    new_actions = current_actions + [action]
                    new_cost = total_cost + action_time  
                    my_queue.put((new_cost, new_loc, new_dir, new_path, new_actions))  #uptade kosztów etc
        return path, actions

    def apply_action(self, loc, dir, action):
        
        if action == 'turnleft':
            new_dir = left_turn(dir)
            time_cost = 5
            new_loc = loc  
        elif action == 'turnright':
            new_dir = right_turn(dir)
            time_cost = 2
            new_loc = loc  
        elif action == 'forward':
            new_dir = dir
            time_cost = 1
            new_loc = next_loc(loc, dir)
        return new_loc, new_dir, time_cost

    def get_path(self):
        return self.path
