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
    random.seed(13)
    np.random.seed(13)
    # rate of executing actions
    rate = 1
    # size of the environment
    env_size = 32
    eps_move = 0.02
    eps_perc_true = 0.1
    eps_perc_false = 0.05
    # map of the environment: 1 - wall, 0 - free
    map = np.zeros((env_size, env_size))
    # build the list of walls locations
    walls = []
    for i in range(map.shape[0]):
        for j in range(map.shape[1]):
            if map[i, j] == 1:
                walls.append((j, env_size - i - 1))

    # list of valid locations
    locs = list({*generate_locations(env_size)}.difference(walls))
    # start location
    start = (0, env_size // 2)
    # doors location
    doors = np.random.choice(np.arange(0, env_size), 6, replace=False)

    # create the environment and viewer
    env = LocWorldEnv(env_size, walls, doors, start, eps_move, eps_perc_true, eps_perc_false)
    view = LocView(env)

    # create the agent
    agent = Agent(env.size, doors, eps_move, eps_perc_true, eps_perc_false)
    # list of errors
    errors = []
    t = 0
    while t != 40:
        print('\nstep %d' % t)

        print('performing action')
        # get agent's action and execute it
        action = agent()
        print('action: ', action)
        env.do_action(action)

        P = agent.get_posterior()
        view.update(env, P)
        update(rate)
        # uncomment to pause before action
        view.pause()

        print('performing perception')
        percept = env.get_percept()
        print('percept: ', percept)
        # print('true loc: %d' % env.agentLoc[0])
        agent.correct_posterior(percept)

        P = agent.get_posterior()
        view.update(env, P)
        update(rate)

        # compute error as square root of expected value of squared differences
        diff = np.abs(env.agent_loc[0] - np.arange(0, env.size))
        # take into account that the world is circular
        diff = np.minimum(diff, env.size - diff)
        diff2 = np.square(diff)
        cur_error = np.sqrt((diff2 * P).sum())
        print('current error: %.3f' % cur_error)

        errors.append(cur_error)
        print('mean error: %.3f' % np.array(errors).mean())

        # uncomment to pause before action
        view.pause()

        t += 1

    # pause until mouse clicked
    view.pause()


if __name__ == '__main__':
    main()
