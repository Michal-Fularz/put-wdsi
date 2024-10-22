from graphics import *
from gridutil import generate_locations


class LocWorldEnv:
    actions = 'turnleft turnright forward'.split()

    def __init__(self, size, walls, graph, start_loc, goal_loc):
        self.size = size
        self.walls = walls
        self.action_sensors = []
        self.locations = {*generate_locations(self.size)}.difference(self.walls)
        self.graph = graph
        self.start_loc = start_loc
        self.goal_loc = goal_loc
        self.lives = 3
        self.reset()
        self.finished = False

    def reset(self):
        self.agentLoc = self.start_loc
        self.agentDir = 'N'

    def do_action(self, action):
        points = -1

        # only actions that comply with graph
        if action in self.graph[self.agentLoc]:
            self.agentLoc = action

        return points  # cost/benefit of action


class LocView:
    # LocView shows a view of a LocWorldEnv. Just hand it an env, and
    #   a window will pop up.

    Size = .2
    Points = {'N': (0, -Size, 0, Size), 'E': (-Size, 0, Size, 0),
              'S': (0, Size, 0, -Size), 'W': (Size, 0, -Size, 0)}

    color = 'black'

    def __init__(self, state, height=800, title='Loc World'):
        xy_size = state.size
        win = self.win = GraphWin(title, 1.33 * height, height, autoflush=False)
        win.setBackground('gray99')
        win.setCoords(-.5, -.5, 1.33 * xy_size - .5, xy_size - .5)
        cells = self.cells = {}
        for x in range(xy_size):
            for y in range(xy_size):
                cells[(x, y)] = Rectangle(Point(x - .5, y - .5), Point(x + .5, y + .5))
                cells[(x, y)].setWidth(0)
                cells[(x, y)].draw(win)
        self.agt = None
        self.arrow = None
        self.path_prim = []
        self.graph_prim = []
        center = 1.167 * (xy_size - .5)

        self.agentName = Text(Point(center, (xy_size - 1) * .5), '').draw(win)
        self.agentName.setSize(20)
        self.agentName.setFill('Orange')

        self.info = Text(Point(center, (xy_size - 1) * .25), '').draw(win)
        self.info.setSize(20)
        self.info.setFace('courier')

        self.update(state, [])

    def set_agent(self, name):
        self.agentName.setText(name)

    def set_info(self, info):
        self.info.setText(info)

    def update(self, state, path):
        # View state in exiting window
        for loc, cell in self.cells.items():
            if loc in state.walls:
                cell.setFill('black')
            elif loc == state.goal_loc:
                cell.setFill('yellow')
            else:
                cell.setFill('white')

        for prim in self.graph_prim:
            prim.undraw()
        self.graph_prim = []
        for node, edges in state.graph.items():
            self.graph_prim.append(self.draw_dot(node, 'black'))
            for nh in edges:
                self.graph_prim.append(self.draw_line(node, nh, 'black'))

        for prim in self.path_prim:
            prim.undraw()
        self.path_prim = []
        for i in range(len(path)):
            self.path_prim.append(self.draw_dot(path[i]))
            if i < len(path) - 1:
                self.path_prim.append(self.draw_line(path[i], path[i + 1]))

        if self.agt:
            self.agt.undraw()
        if state.agentLoc:
            self.agt = self.draw_arrow(state.agentLoc, state.agentDir, 5, self.color)

    def draw_dot(self, loc, color='blue'):
        x, y = loc
        a = Circle(Point(x, y), .1)
        a.setWidth(1)
        a.setFill(color)
        a.draw(self.win)
        return a

    def draw_line(self, loc1, loc2, color='blue'):
        x1, y1 = loc1
        x2, y2 = loc2
        p1 = Point(x1, y1)
        p2 = Point(x2, y2)
        a = Line(p1, p2)
        a.setWidth(2)
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
