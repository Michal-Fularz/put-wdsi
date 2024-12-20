# prob.py

import random
import numpy as np
import queue
import math

from gridutil import generate_locations


class Agent:
    def __init__(self, size, walls, loc, dir, sigma_move, sigma_perc, dt):
        self.size = size
        self.walls = walls
        # list of valid locations
        self.locations = list({*generate_locations(self.size)}.difference(self.walls))
        # dictionary from location to its index in the list
        self.loc_to_idx = {loc: idx for idx, loc in enumerate(self.locations)}
        self.loc = loc
        self.dir = dir
        self.dt = dt
        self.action_dir = 1

        self.t = 0

        # create matrices used in Kalman filter
        # TODO PUT YOUR CODE HERE


        # ------------------

    def __call__(self):
        # use information about requested action to update posterior
        # TODO PUT YOUR CODE HERE


        # ------------------

        # this function does not return anything
        return

    def predict_posterior(self):
        # predict posterior
        # TODO PUT YOUR CODE HERE


        # ------------------

        # this function does not return anything
        return

    def correct_posterior(self, percept):
        # correct posterior using measurements
        # TODO PUT YOUR CODE HERE


        # ------------------

        # this function does not return anything
        return

    def get_posterior(self):
        return self.mu, self.Sigma
