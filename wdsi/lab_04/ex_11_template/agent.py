import numpy as np
import math


class Agent:
    def __init__(self, size, sigma_move, sigma_perc):
        self.size = size
        self.sigma_sq_move = sigma_move ** 2
        self.sigma_sq_perc = sigma_perc ** 2
        # list of valid locations
        self.locations = [loc for loc in range(size)]
        # dictionary from location to its index in the list
        self.loc_to_idx = {loc: idx for idx, loc in enumerate(self.locations)}
        self.action_dir = -1

        self.t = 0
        self.n = 20

        # create an initial particle set as 1-D numpy array (self.p)
        # and initial weights as 1-D numpy array (self.w)
        # TODO PUT YOUR CODE HERE
        self.p = np.random.random(self.n) * self.size
        self.w = np.ones(self.n, dtype=float) / self.n
        # ------------------

    def __call__(self):
        # if reached one of the ends then start moving in the opposite direction
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
        for i in range(self.n):
            self.p[i] = (self.p[i] + action + np.random.randn(1) * math.sqrt(self.sigma_sq_move)) % self.size
        # ------------------

        # this function does not return anything
        return

    def calculate_weights(self, percept):
        # calculate weights using percept
        # TODO PUT YOUR CODE HERE
        for i in range(len(self.p)):
            diff = self.p[i] - percept
            self.w[i] = math.exp(-0.5 * (diff ** 2) / self.sigma_sq_perc)
        self.w = self.w / np.sum(self.w)
        # ------------------

        # this function does not return anything
        return

    def correct_posterior(self):
        # correct posterior using measurements
        # TODO PUT YOUR CODE HERE
        beta = 0.0
        idx = 0
        w_max = np.max(self.w)
        p_new = np.zeros_like(self.p)
        for i in range(self.n):
            beta += np.random.random(1) * 2 * w_max
            while self.w[idx] < beta:
                beta -= self.w[idx]
                idx = (idx + 1) % self.n

            p_new[i] = self.p[idx]

        self.p = p_new
        # ------------------

        # this function does not return anything
        return

    def get_particles(self):
        return self.p

    def get_weights(self):
        return self.w
