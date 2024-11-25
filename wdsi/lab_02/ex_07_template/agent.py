# prob.py
# This is

import random
import numpy as np
import queue
import math

from gridutil import generate_locations


class Agent:
    def __init__(self, size, walls, loc, dir, eps_move, eps_perc):
        self.size = size
        self.walls = walls
        self.eps_move = eps_move
        self.eps_perc = eps_perc
        # list of valid locations
        self.locations = list({*generate_locations(self.size)}.difference(self.walls))
        # dictionary from location to its index in the list
        self.loc_to_idx = {loc: idx for idx, loc in enumerate(self.locations)}
        self.loc = loc
        self.dir = dir
        self.action_dir = 1

        self.t = 0
        self.P = np.zeros(self.size, dtype=float)
        # we start from 0
        self.P[loc[0]] = 1.0

    def __call__(self):
        # most probable location
        loc = np.argmax(self.P)
        # if reached one of the ends then start moving in the opposite direction
        if (self.action_dir == 1 and loc == self.size - 1) or \
           (self.action_dir == -1 and loc == 0):
            self.action_dir *= -1

        # move by one or two cells
        action = self.action_dir * np.random.choice([1, 2])

        # use information about requested action to update posterior
        # TODO PUT YOUR CODE HERE
        # self.loc = (loc, 16)
        self.predict_posterior(action)

        # ------------------

        return action

    # Jak będzie wyglądał rozkład  P(Xt|Xt−1,ut) ? Uzupełnij funkcję predict_posterior(self, action), aby dokonywała
    # predykcji na podstawie otrzymanej wartości action, oznaczającej komendę, która powinna zostać wykonana
    # (ale niekoniecznie wykonaną ze względu na niedoskonałość układu napędowego), oraz uwzględniając model niepewności.

    def predict_posterior(self, action):

        # 1−6∗ϵm , że poruszy się prawidłowo (action),
        # 2ϵm , że poruszy się o jedną komórkę za mało (action - 1),
        # 2ϵm , że poruszy się o jedną komórkę za dużo (action + 1),
        # ϵm , że poruszy się o dwie komórki za mało (action - 2),
        # ϵm , że poruszy się o dwie komórki za dużo (action + 2).

        # predict posterior using requested action
        # TODO PUT YOUR CODE HERE

        P_prev = self.P.copy()
        for cur_loc in range(self.size):
            P_cur = 0.0
            for prev_loc in range(self.size):
                P_trans = 0.0
                diffs = [-2, -1, 0, 1, 2]
                probs = [
                    self.eps_move,
                    2 * self.eps_move,
                    1.0 - 6 * self.eps_move,
                    2 * self.eps_move,
                    self.eps_move,
                ]
                for i, cur_diff in enumerate(diffs):
                    if (
                        min(max(prev_loc + action + cur_diff, 0), self.size - 1)
                        == cur_loc
                    ):
                        P_trans += probs[i]
                P_cur += P_trans * P_prev[prev_loc]
            self.P[cur_loc] = P_cur

        # ------------------

        return

    def predict_posterior_my(self, action):
        # predict posterior using requested action
        # TODO PUT YOUR CODE HERE

        print(f"{self.loc=}")
        print(f"{action=}")

        # 1−6∗ϵm , że poruszy się prawidłowo (action),
        # 2ϵm , że poruszy się o jedną komórkę za mało (action - 1),
        # 2ϵm , że poruszy się o jedną komórkę za dużo (action + 1),
        # ϵm , że poruszy się o dwie komórki za mało (action - 2),
        # ϵm , że poruszy się o dwie komórki za dużo (action + 2).
        loc = self.loc[0]
        self.P_previous = self.P.copy()
        self.P = np.zeros(self.size, dtype=float)
        for i in range(0, self.size):
            if self.P_previous[i] != 0:
                p = self.P_previous[i]
                if 0 <= (i + action - 2) < self.size:
                    self.P[i + action - 2] += p * 1 * self.eps_move
                if 0 <= (i + action - 1) < self.size:
                    self.P[i + action - 1] += p * 2 * self.eps_move
                if 0 <= (i + action) < self.size:
                    self.P[i + action] += p * (1 - 6 * self.eps_move)
                if 0 <= (i + action + 1) < self.size:
                    self.P[i + action + 1] += p * 2 * self.eps_move
                if 0 <= (i + action + 2) < self.size:
                    self.P[i + action + 2] += p * 1 * self.eps_move

        print(np.argmax(self.P))

        # bel¯¯¯¯¯¯(xt)=P(xt|z1:t−1,u1:t)=∑xt−1P(xt|xt−1,ut)bel(xt−1)

        # ------------------

        return

    def correct_posterior(self, percept):
        # TODO PUT YOUR CODE HERE
        # correct posterior using measurements

        # 1−6∗ϵp , że pomiar będzie prawidłowy (percept),
        # 2ϵp , że pomiar wskaże jedną komórkę za mało (percept - 1),
        # 2ϵp , że pomiar wskaże jedną komórkę za dużo (percept + 1),
        # ϵp , że pomiar wskaże dwie komórki za mało (percept - 2),
        # ϵp , że pomiar wskaże dwie komórki za dużo (percept + 2).

        P_cur = np.zeros_like(self.P)

        P_cur[percept] += 1.0 - 6 * self.eps_perc
        P_cur[max(percept - 1, 0)] += 2 * self.eps_perc
        P_cur[max(percept - 2, 0)] += self.eps_perc
        P_cur[min(percept + 1, self.size - 1)] += 2 * self.eps_perc
        P_cur[min(percept + 2, self.size - 1)] += self.eps_perc

        self.P = P_cur * self.P
        self.P /= np.sum(self.P)

        # ------------------
        return

    def get_posterior(self):
        return self.P
