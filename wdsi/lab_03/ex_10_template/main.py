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
    sigma_move = 0.2
    sigma_perc = 1.0
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
    start = (0.0, float(env_size // 2))
    # time step
    dt = 1.0

    # create the environment and viewer
    env = LocWorldEnv(env_size, walls, start, sigma_move, sigma_perc, dt)
    view = LocView(env)

    # create the agent
    agent = Agent(env.size, env.walls, env.agent_loc, env.agent_dir, sigma_move, sigma_perc, dt)

    t = 0.0
    print('initial state')
    mu, Sigma = agent.get_posterior()
    view.update(env, mu, Sigma)
    # uncomment to pause before action
    view.pause()

    # list of errors
    errors = []
    while t < 40:
        print('\ntime %.3f' % t)

        print('performing action')
        # get agent's action and execute it
        agent()
        env.do_action()

        mu, Sigma = agent.get_posterior()
        view.update(env, mu, Sigma)
        update(0.5 / dt)
        # uncomment to pause before action
        view.pause()

        print('performing perception')
        percept = env.get_percept()
        print('percept: %.3f' % percept)
        print('true loc: %.3f' % env.agent_loc[0])
        agent.correct_posterior(percept)

        mu, Sigma = agent.get_posterior()
        view.update(env, mu, Sigma)
        update(0.5 / dt)

        # compute error as square root of expected value of squared differences
        diff = np.abs(env.agent_loc[0] - mu[0])
        # take into account that the world is circular
        diff = np.minimum(diff, env.size - diff)
        cur_error = diff
        print('current error: %.3f' % cur_error)

        errors.append(cur_error)
        print('mean error: %.3f' % np.array(errors).mean())

        # uncomment to pause before action
        view.pause()

        t += dt

    # pause until mouse clicked
    view.pause()


if __name__ == '__main__':
    main()
