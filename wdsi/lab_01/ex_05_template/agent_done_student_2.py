# prob.py
# This is

import random
import numpy as np
import queue
import heapq

from gridutil import generate_locations, left_turn, DIRECTIONS


class Agent:
    def __init__(self, size, walls, loc, dir, goal):
        self.size = size
        self.walls = walls
        self.locations = list({*generate_locations(self.size)}.difference(self.walls))
        self.loc_to_idx = {loc: idx for idx, loc in enumerate(self.locations)}
        self.loc = loc
        self.dir = dir
        self.goal = goal

        self.t = 0
        self.path, self.actions = self.find_path()

    def __call__(self):
        action = '--- no action ---'


        if self.actions:
            action = self.actions.pop(0)

        # ------------------

        return action

    def get_neighbours(self, current_location):
        x, y = current_location

        return list({
            (x+1, y), 
            (x, y+1),
            (x-1, y),
            (x, y-1)
        }.difference(self.walls).difference(self.loc))


    def determine_cost(self, current_location, target_location, agent_direction):
        current_x, current_y = current_location
        target_x, target_y = target_location
        actions = []

        if current_x < target_x:
            correct_direction = 'E'
        elif current_x > target_x:
            correct_direction = 'W'
        elif current_y < target_y:
            correct_direction = 'N'
        else:
            correct_direction = 'S'

        turn_diff = DIRECTIONS.find(agent_direction) - DIRECTIONS.find(correct_direction)

        if turn_diff == 1 or turn_diff == -3:
            actions.append('turnleft')
        elif turn_diff != 0:
            while turn_diff != 0:
                actions.append('turnright')
                turn_diff += 1

        total_cost = 0

        cost_of_action = {
            'turnright': -2,
            'turnleft': -5
        }

        for action in actions:
            total_cost += cost_of_action[action]

        total_cost -= 1

        return total_cost

    def manhattan_cost(self, current_location) -> int:
        current_x, current_y = current_location
        final_x, final_y = self.goal
        return abs(current_x - final_x) + abs(current_y - final_y)

    def find_path(self):
        
        fringe = [(0, self.loc)]
        came_from = {self.loc: None}
        cost_so_far = {self.loc: 0}

        while fringe:
            current: tuple[int, int] = heapq.heappop(fringe)[1]

            if current == self.goal:
                break
                
            for next_node in self.get_neighbours(current):
                enter_cost = self.determine_cost(
                    current_location=current, 
                    target_location=next_node, 
                    agent_direction=self.dir
                )
                
                new_cost = cost_so_far[current] + abs(enter_cost)
                
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + self.manhattan_cost(next_node)
                    heapq.heappush(fringe, (priority, next_node))
                    came_from[next_node] = current

        path = self.reconstruct_path(came_from)
        actions = self.recreate_actions(path)
        self.actions = actions
        return path, actions
    


    def reconstruct_path(self, came_from: dict[tuple[int, int], tuple[int, int]]) -> list[tuple[int, int]]:
        current = self.goal
        path = []

        if self.goal not in came_from:
            return []
        
        while current != self.loc:
            path.append(current)
            current = came_from[current]
        path.append(self.loc)
        path.reverse()
        return path
    


    def recreate_actions(self, path: list[tuple[int, int]]) -> list[str]:
        actions = []
        agent_direction = self.dir

        for i in range(len(path) - 1):
            x, y = path[i]
            next_x, next_y = path[i+1]

            proper_direction: str
            if x < next_x:
                proper_direction = 'W'
            elif x > next_x:
                proper_direction = 'E'
            elif y < next_y:
                proper_direction = 'N'
            else: # y < next_y
                proper_direction = 'S'


            if agent_direction != proper_direction:
                match (agent_direction, proper_direction):
                    case ('N', 'E'):
                        actions.append('turnleft')
                    case ('N', 'W'):
                        actions.append('turnright')
                    case ('E', 'S'):
                        actions.append('turnleft')
                    case ('E', 'N'):
                        actions.append('turnright')
                    case ('S', 'W'):
                        actions.append('turnleft')
                    case ('S', 'E'):
                        actions.append('turnright')
                    case ('W', 'N'):
                        actions.append('turnleft')
                    case ('W', 'S'):
                        actions.append('turnright')
                    case _:
                        actions.append('turnright')
                        actions.append('turnright')

            agent_direction = proper_direction
            actions.append('forward')

        return actions



    def get_path(self):
        return self.path
