from graphics import *
from gridutil import generate_locations

import random
import math
import numpy as np


class LocWorldEnv:
    actions = "turnleft turnright forward".split()

    def __init__(self, size, walls, start_loc, sigma_move, sigma_perc, dt):
        self.size = size
        self.walls = walls
        self.action_sensors = []
        self.locations = {*generate_locations(self.size)}.difference(self.walls)
        self.start_loc = start_loc
        self.sigma_move = sigma_move
        self.sigma_perc = sigma_perc
        self.dt = dt
        self.lives = 3
        self.reset()
        self.finished = False

    def reset(self):
        self.agent_loc = self.start_loc
        self.agent_vel = 1
        self.agent_dir = 'N'

    def get_percept(self):
        percept = self.agent_loc[0] + random.gauss(0.0, self.sigma_perc)

        return percept

    def do_action(self):
        points = -1

        if (self.agent_loc[0] > self.size - 2 and self.agent_vel > 0) or \
            (self.agent_loc[0] < 2 and self.agent_vel < 0):
            self.agent_vel *= -1

        self.agent_vel += random.gauss(0.0, self.sigma_move)
        action = self.agent_vel * self.dt

        print('velocity %.3f' % self.agent_vel)
        self.agent_loc = ((self.agent_loc[0] + action) % self.size, self.agent_loc[1])

        return points  # cost/benefit of action


class LocView:
    # LocView shows a view of a LocWorldEnv. Just hand it an env, and
    #   a window will pop up.

    Size = .5
    Points = {'N': (0, -Size, 0, Size), 'E': (-Size, 0, Size, 0),
              'S': (0, Size, 0, -Size), 'W': (Size, 0, -Size, 0)}

    color = "black"

    def __init__(self, state, height=800, title="Loc World"):
        xy_size = state.size
        win = self.win = GraphWin(title, 1.33 * height, height, autoflush=False)
        win.setBackground("gray99")
        win.setCoords(-.5, -.5, 1.33 * xy_size - .5, xy_size - .5)
        cells = self.cells = {}
        for x in range(xy_size):
            for y in range(xy_size):
                cells[(x, y)] = Rectangle(Point(x - .5, y - .5), Point(x + .5, y + .5))
                cells[(x, y)].setWidth(0)
                cells[(x, y)].draw(win)
        self.agt = None
        self.arrow = None
        self.prob_prims = []
        self.chart_prims = []
        center = 1.167 * (xy_size - .5)

        self.agentName = Text(Point(center, (xy_size - 1) * .5), "").draw(win)
        self.agentName.setSize(20)
        self.agentName.setFill("Orange")

        self.info = Text(Point(center, (xy_size - 1) * .25), "").draw(win)
        self.info.setSize(20)
        self.info.setFace("courier")

        self.update(state)

    def set_agent(self, name):
        self.agentName.setText(name)

    def set_info(self, info):
        self.info.setText(info)

    def update(self, state, x=None, P=None):
        # View state in exiting window
        for loc, cell in self.cells.items():
            if loc in state.walls:
                cell.setFill("black")
            else:
                cell.setFill("white")

        for prim in self.prob_prims:
            prim.undraw()
        self.prob_prims = []
        if x is not None and P is not None:
            vals, vecs = np.linalg.eigh(P)

            smaller_val = vals[0]
            larger_val = vals[1]
            smaller_vec = vecs[:, 0]
            larger_vec = vecs[:, 1]

            angle = np.arctan2(larger_vec[1], larger_vec[0])
            if angle < 0.0:
                angle += 2 * math.pi

            # for 1, 2, and 3 standard deviations
            for conf in [1.0, 2.0, 3.0]:
                chisquare_val = conf
                n_pts = 100
                theta_grid = np.arange(0, 2 * math.pi, 2 * math.pi / (n_pts - 1))
                phi = angle
                X0 = x[0]
                Y0 = x[1]
                a = chisquare_val * math.sqrt(larger_val)
                b = chisquare_val * math.sqrt(smaller_val)

                # the ellipse in x and y coordinates
                ellipse_x_r = a * np.cos(theta_grid)
                ellipse_y_r = b * np.sin(theta_grid)

                # Define a rotation matrix
                R = np.array([[np.cos(phi), np.sin(phi)],
                              [-np.sin(phi), np.cos(phi)]])

                # let's rotate the ellipse to some angle phi
                r_ellipse = np.stack([ellipse_x_r, ellipse_y_r]).transpose() @ R

                offset = state.agent_loc[1]
                points = []
                for pt in r_ellipse:
                    points.append(Point(X0 + pt[0], Y0 + pt[1] + offset))
                # points.append(Point(state.size - 1.0, offset))
                poly = Polygon(points)
                poly.setWidth(1)
                # self.prob_prim.setFill("blue")
                poly.draw(self.win)

                self.prob_prims.append(poly)

            for prim in self.chart_prims:
                prim.undraw()
            self.chart_prims = []
            for y in np.arange(-2.0, 3.0, 1.0):
                self.chart_prims.append(self.draw_line((0.0, offset + y),
                                                       (state.size, offset + y),
                                                       color="black",
                                                       width=1))
                self.chart_prims.append(self.draw_text((state.size + 1, offset + y), str(y), color="black"))
            self.chart_prims.append(self.draw_line((0.0, state.agent_loc[1] + state.agent_vel),
                                                   (state.size, state.agent_loc[1] + state.agent_vel),
                                                   color="red",
                                                   width=1))

        if self.agt:
            self.agt.undraw()
        if state.agent_loc:
            self.agt = self.draw_arrow(state.agent_loc, state.agent_dir, 5, self.color)

    def draw_rect(self, loc, height, color="blue"):
        x, y = loc
        a = Rectangle(Point(x - .5, y - .5), Point(x + .5, y - .5 + 4 * height))
        a.setWidth(0)
        a.setFill(color)
        a.draw(self.win)
        return a

    def draw_dot(self, loc, color="blue"):
        x, y = loc
        a = Circle(Point(x, y), .1)
        a.setWidth(1)
        a.setFill(color)
        a.draw(self.win)
        return a

    def draw_text(self, loc, text, color="blue"):
        x, y = loc
        a = Text(Point(x, y), text)
        a.setFill(color)
        a.draw(self.win)
        return a

    def draw_line(self, loc1, loc2, color="blue", width=2):
        x1, y1 = loc1
        x2, y2 = loc2
        p1 = Point(x1, y1)
        p2 = Point(x2, y2)
        a = Line(p1, p2)
        a.setWidth(width)
        a.setFill(color)
        a.draw(self.win)
        return a

    def draw_arrow(self, loc, heading, width, color):
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

    def close(self):
        self.win.close()
