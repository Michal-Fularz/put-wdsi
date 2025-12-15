from graphics import *
from gridutil import *

import random
import math
import numpy as np


class LocWorldEnv:
    actions = "turnleft turnright forward".split()

    def __init__(self, size, walls, start_loc, sigma_move, sigma_perc):
        self.size = size
        self.walls = walls
        self.action_sensors = []
        self.locations = {*locations(self.size)}.difference(self.walls)
        self.start_loc = start_loc
        self.sigma_move = sigma_move
        self.sigma_perc = sigma_perc
        self.lifes = 3
        self.reset()
        self.finished = False

    def reset(self):
        self.agentLoc = self.start_loc
        self.agentDir = 'N'

    def getPercept(self):
        percept = self.agentLoc[0] + random.gauss(0.0, self.sigma_perc)

        return percept

    def doAction(self, action):
        points = -1

        action += random.gauss(0.0, self.sigma_move)

        print('executed action %.3f' % action)
        self.agentLoc = ((self.agentLoc[0] + action) % self.size, self.agentLoc[1])

        return points  # cost/benefit of action


class LocView:
    # LocView shows a view of a LocWorldEnv. Just hand it an env, and
    #   a window will pop up.

    Size = .5
    Points = {'N': (0, -Size, 0, Size), 'E': (-Size, 0, Size, 0),
              'S': (0, Size, 0, -Size), 'W': (Size, 0, -Size, 0)}

    color = "black"

    def __init__(self, state, height=800, title="Loc World"):
        xySize = state.size
        win = self.win = GraphWin(title, 1.33 * height, height, autoflush=False)
        win.setBackground("gray99")
        win.setCoords(-.5, -.5, 1.33 * xySize - .5, xySize - .5)
        cells = self.cells = {}
        for x in range(xySize):
            for y in range(xySize):
                cells[(x, y)] = Rectangle(Point(x - .5, y - .5), Point(x + .5, y + .5))
                cells[(x, y)].setWidth(0)
                cells[(x, y)].draw(win)
        self.agt = None
        self.arrow = None
        self.prob_prims = []
        ccenter = 1.167 * (xySize - .5)
        # self.time = Text(Point(ccenter, (xySize - 1) * .75), "Time").draw(win)
        # self.time.setSize(36)
        # self.setTimeColor("black")

        self.agentName = Text(Point(ccenter, (xySize - 1) * .5), "").draw(win)
        self.agentName.setSize(20)
        self.agentName.setFill("Orange")

        self.info = Text(Point(ccenter, (xySize - 1) * .25), "").draw(win)
        self.info.setSize(20)
        self.info.setFace("courier")

        self.update(state)

    def setAgent(self, name):
        self.agentName.setText(name)

    # def setTime(self, seconds):
    #     self.time.setText(str(seconds))

    def setInfo(self, info):
        self.info.setText(info)

    def update(self, state, p=None, w=None):
        # View state in exiting window
        for loc, cell in self.cells.items():
            if loc in state.walls:
                cell.setFill("black")
            else:
                cell.setFill("white")

        for prim in self.prob_prims:
            prim.undraw()
        self.prob_prims = []
        if w is not None:
            w = w / np.sum(w)
            # minimum weight, so it is visible
            w = np.maximum(w, 0.1 / len(w))
        if p is not None:
            offset = state.agentLoc[1] + 2
            for i in range(len(p)):
                size = 1.0
                if w is not None:
                    size = w[i] * 10.0
                self.prob_prims.append(self.drawLine((p[i], offset), (p[i], offset + size), 'blue'))

        if self.agt:
            self.agt.undraw()
        if state.agentLoc:
            self.agt = self.drawArrow(state.agentLoc, state.agentDir, 5, self.color)

    def drawRect(self, loc, height, color="blue"):
        x, y = loc
        a = Rectangle(Point(x - .5, y - .5), Point(x + .5, y - .5 + 4 * height))
        a.setWidth(0)
        a.setFill(color)
        a.draw(self.win)
        return a

    def drawDot(self, loc, color="blue", size=0.1):
        x, y = loc
        a = Circle(Point(x, y), size)
        a.setWidth(1)
        a.setFill(color)
        a.draw(self.win)
        return a

    def drawLine(self, loc1, loc2, color="blue"):
        x1, y1 = loc1
        x2, y2 = loc2
        p1 = Point(x1, y1)
        p2 = Point(x2, y2)
        a = Line(p1, p2)
        a.setWidth(2)
        a.setFill(color)
        a.draw(self.win)
        return a

    def drawArrow(self, loc, heading, width, color):
        x, y = loc
        dx0, dy0, dx1, dy1 = self.Points[heading]
        p1 = Point(x + dx0, y + dy0)
        p2 = Point(x + dx1, y + dy1)
        a = Line(p1, p2)
        a.setWidth(width)
        a.setArrow('last')
        a.setFill(color)
        a.draw(self.win)
        return a

    def pause(self):
        self.win.getMouse()

    # def setTimeColor(self, c):
    #     self.time.setTextColor(c)

    def close(self):
        self.win.close()
