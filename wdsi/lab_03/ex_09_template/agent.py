# prob.py

import numpy as np
import math


class Agent:
    def __init__(self, size, sigma_move, sigma_perc):
        self.size = size
        self.sigma_sq_move = sigma_move ** 2
        self.sigma_sq_perc = sigma_perc ** 2
        self.action_dir = -1

        self.t = 0
        # initial belief
        self.mu = 0.0
        self.sigma_sq = 1.0

    def __call__(self):
        # if reached one of the ends then start moving in the opposite direction
        if self.t % 20 == 0:
            self.action_dir *= -1

        # move by random distance in range [1, 2)
        action = self.action_dir * (1.0 + np.random.random_sample(1))

        # use information about requested action to update posterior
        # TODO PUT YOUR CODE HERE

        self.predict_posterior(action)
 
        # ------------------

        self.t += 1

        return action

    def predict_posterior(self, action):
        # predict posterior using requested action
        # TODO PUT YOUR CODE HERE

        self.mu = (self.mu + action) % self.size
        self.sigma_sq += self.sigma_sq_move

        # ------------------

        return

    def correct_posterior(self, percept):
        # correct posterior using measurements
        # TODO PUT YOUR CODE HERE

        self.mu = ((self.sigma_sq * self.mu + self.sigma_sq_perc * percept) / (self.sigma_sq + self.sigma_sq_perc)) % self.size
        self.sigma_sq = 1 / (1.0 / self.sigma_sq + 1.0 / self.sigma_sq_perc)
        # ------------------

        return

    def get_posterior(self):
        return self.mu, math.sqrt(self.sigma_sq)
