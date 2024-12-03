# prob.py

import random
import numpy as np
import queue
import math

from gridutil import generate_locations


class Agent:
    def __init__(self, size, doors, eps_move, eps_perc_true, eps_perc_false):
        self.size = size
        self.doors = doors
        self.eps_move = eps_move
        self.eps_perc_true = eps_perc_true
        self.eps_perc_false = eps_perc_false
        # list of valid locations
        self.locations = [loc for loc in range(self.size)]
        # dictionary from location to its index in the list
        self.loc_to_idx = {loc: idx for idx, loc in enumerate(self.locations)}
        self.action_dir = -1

        self.t = 0
        self.P = 1.0 / self.size * np.ones(self.size, dtype=float)

    def __call__(self):
        # change direction after 20 steps
        if self.t % 20 == 0:
            self.action_dir *= -1

        # move by one or two cells
        action = self.action_dir * np.random.choice([1, 2])

        # use information about requested action to update posterior
        # TODO PUT YOUR CODE HERE

        self.predict_posterior(action)

        # ------------------

        self.t += 1

        return action

    def predict_posterior(self, action):
        # predict posterior using requested action
        # TODO PUT YOUR CODE HERE

        P_prev = self.P.copy()
        for cur_loc in range(self.size):
            P_cur = 0.0
            for prev_loc in range(self.size):
                P_trans = 0.0
                diffs = [-2, -1, 0, 1, 2]
                probs = [self.eps_move, 2 * self.eps_move, 1.0 - 6 * self.eps_move, 2 * self.eps_move, self.eps_move]
                for i, cur_diff in enumerate(diffs):
                    if (prev_loc + action + cur_diff) % self.size == cur_loc:
                        P_trans += probs[i]
                P_cur += P_trans * P_prev[prev_loc]
            self.P[cur_loc] = P_cur


        # ------------------

        return

    def correct_posterior(self, percept):
        # correct posterior using measurements
        # TODO PUT YOUR CODE HERE

        P_cur = np.zeros_like(self.P)

        for i in range(self.size):
            if percept == True:
                if i in self.doors:
                    P_cur[i] = 1.0 - self.eps_perc_true
                else:
                    P_cur[i] = self.eps_perc_false
            elif percept == False:
                if i in self.doors:
                    P_cur[i] = self.eps_perc_true
                else:
                    P_cur[i] = 1.0 - self.eps_perc_false

        self.P = P_cur * self.P
        self.P /= np.sum(self.P)


        # ------------------
        return

    def get_posterior(self):
        return self.P
