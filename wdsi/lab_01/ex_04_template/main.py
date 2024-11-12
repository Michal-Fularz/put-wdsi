#!/usr/bin/env python

"""code template"""

import random
import numpy as np

from graphics import *
from agent import Agent
from env import LocWorldEnv, LocView


def main():
    # comment to get different scenarios
    # random.seed(13)
    # rate of executing actions
    rate = 1
    # size of the environment
    env_size = 16
    # map of the environment: 1 - wall, 0 - free
    map = np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])
    # build the list of walls locations
    walls = []
    for i in range(map.shape[0]):
        for j in range(map.shape[1]):
            if map[i, j] == 1:
                walls.append((j, env_size - i - 1))

    graph = {(0, 4): [(5, 5), (0, 7)],
             (0, 7): [(0, 4), (3, 8)],
             (1, 10): [(3, 8), (3, 11)],
             (3, 8): [(0, 7), (1, 10), (5, 5), (5, 10)],
             (3, 11): [(1, 10)],
             (5, 5): [(0, 4), (3, 8), (9, 4)],
             (5, 10): [(3, 8), (8, 8), (10, 10)],
             (8, 7): [(9, 4)],
             (8, 8): [(5, 10), (10, 10)],
             (9, 4): [(5, 5), (8, 7), (10, 7)],
             (10, 7): [(9, 4), (10, 10), (12, 5)],
             (10, 10): [(5, 10), (8, 8), (10, 7), (12, 9)],
             (12, 5): [(10, 7), (12, 7)],
             (12, 7): [(12, 5), (12, 9), (15, 8)],
             (12, 9): [(10, 10), (12, 7), (14, 10)],
             (14, 4): [(15, 8)],
             (14, 10): [(12, 9), (15, 8)],
             (15, 8): [(12, 7), (14, 4), (14, 10)]}

    # list of valid locations
    locs = list(graph.keys())
    # start and goal location
    start_goal = random.sample(locs, k=2)
    # start = start_goal[0]
    start = (8, 8)
    # goal = start_goal[1]
    goal = (8, 7)

    # create the environment and viewer
    env = LocWorldEnv(env_size, walls, graph, start, goal)
    view = LocView(env)

    # create the agent
    agent = Agent(env.size, env.walls, env.graph, env.agent_loc, env.agent_dir, goal)
    t = 0
    while env.agent_loc != goal:
        print('step %d' % t)

        # get agent's path
        path = agent.get_path()
        # get agent's action
        action = agent()

        print('action ', action)

        view.update(env, path)
        update(rate)
        # uncomment to pause before action
        view.pause()

        env.do_action(action)

        t += 1

    # pause until mouse clicked
    view.pause()


if __name__ == '__main__':
    main()
