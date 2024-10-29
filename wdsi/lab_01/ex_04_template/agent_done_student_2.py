import random
import numpy as np
import queue
import math
import heapq


class Agent:
    def __init__(self, size, walls, graph, loc, dir, goal):
        self.size = size
        self.walls = walls
        self.graph = graph
        # list of valid locations
        self.locations = list(self.graph.keys())
        # dictionary from location to its index in the list
        self.loc_to_idx = {loc: idx for idx, loc in enumerate(self.locations)}
        self.loc = loc
        self.dir = dir
        self.goal = goal

        self.path = self.find_path()

    def euclidean_distance(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def __call__(self):
        if len(self.path) > 1:
            next_location = self.path[1] 

            if next_location in self.graph[self.loc]:
                self.loc = next_location
                self.path.pop(0)
            else:
                next_location = self.loc
        else:
            next_location = self.loc

        return next_location

    def find_path(self):
        distances = {node: float('inf') for node in self.graph}
        distances[self.loc] = 0

        previous_nodes = {node: None for node in self.graph}

        priority_queue = [(0, self.loc)]  

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)
            if current_node == self.goal:
                break

            # visited not updated

            for neighbor in self.graph[current_node]:
                distance = current_distance + self.euclidean_distance(current_node, neighbor)

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))

        path = []
        current = self.goal
        while current is not None:
            path.append(current)
            current = previous_nodes[current]
        # path.append(self.loc)
        path = path[::-1] 

        return path if path[0] == self.loc else []

    def get_path(self):
        return self.path