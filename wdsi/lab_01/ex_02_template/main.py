#!/usr/bin/env python

"""code template"""

import random
import numpy as np

from graphics import *
from gridutil import generate_locations
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
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                    [1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0],
                    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                    [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
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

    # list of valid locations
    locs = list({*generate_locations(env_size)}.difference(walls))
    # start and goal location
    start_goal = random.sample(locs, k=2)
    start = start_goal[0]
    goal = start_goal[1]

    # create the environment and viewer
    env = LocWorldEnv(env_size, walls, start, goal)
    view = LocView(env)

    # create the agent
    agent = Agent(env.size, env.walls, env.agent_loc, env.agent_dir, goal)
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
