# -*-coding: utf-8 -*
'''NAMES OF THE AUTHOR(S): Gael Aglin <gael.aglin@uclouvain.be>, Francois Aubry <francois.aubry@uclouvain.be>'''
from search import *


#################
# Problem class #
#################
class Pacmen(Problem):

    def __init__(self, initial):
        super().__init__(initial)
        self.initial.initial_scan()
        self.nb_explored_nodes = 0

    def successor(self, state):
        self.nb_explored_nodes += 1
        pass

    def goal_test(self, state):
        pass


###############
# State class #
###############
class State:
    def __init__(self, grid):
        self.nbr = len(grid)
        self.nbc = len(grid[0])
        self.grid = grid

        # Positions of the pacmen
        self.pacmen = []
        # Positions of the foods
        self.foods = []
        # Number of foods remaining
        self.foods_left = 0

    def __str__(self):
        s = ""
        for a in range(nsharp):
            s = s + "#"
        s = s + '\n'
        for i in range(0, self.nbr):
            s = s + "# "
            for j in range(0, self.nbc):
                s = s + str(self.grid[i][j]) + " "
            s = s + "#"
            if i < self.nbr:
                s = s + '\n'
        for a in range(nsharp):
            s = s + "#"
        return s

    def __eq__(self, o) -> bool:
        return self.grid.__eq__(o.grid)

    def __hash__(self) -> int:
        return self.grid.__hash__()

    def clone(self):
        """Clone method of State, allowing a deep copy of the state class."""
        new_grid = [[0 for i in range(self.nbc)] for j in range(self.nbr)]
        for i in range(0, self.nbr):
            new_grid[i] = list(self.grid[i])
        new_state = State(new_grid)
        new_state.pacmen = list(self.pacmen)
        new_state.foods = list(self.foods)
        new_state.foods_left = self.foods_left
        return new_state

    def initial_scan(self):
        """Initial_scan scans the grid and stores the position of the pacmen and the foods in the appropriate fields"""
        for i in range(0, self.nbr):
            for j in range(0, self.nbc):
                tile = self.grid[i][j]
                if tile == '$':
                    self.pacmen.append((i, j))
                elif tile == '@':
                    self.foods.append((i, j))
                    self.foods_left += 1


######################
# Auxiliary function #
######################
def read_instance_file(filename):
    lines = [[char for char in line.rstrip('\n')[1:][:-1]] for line in open(filename)]
    nsharp = len(lines[0]) + 2
    lines = lines[1:len(lines) - 1]
    n = len(lines)
    m = len(lines[0])
    grid_init = [[lines[i][j] for j in range(1, m, 2)] for i in range(0, n)]
    return grid_init, nsharp


######################
# Heuristic function #
######################
def heuristic(node):
    h = 0.0
    # ...
    # compute an heuristic value
    # ...
    return h


#####################
# Launch the search #
#####################
grid_init, nsharp = read_instance_file(sys.argv[1])
init_state = State(grid_init)

problem = Pacmen(init_state)

node = astar_graph_search(problem, heuristic)

# example of print
path = node.path()
path.reverse()

print('Number of moves: ' + str(node.depth))
for n in path:
    print(n.state)  # assuming that the __str__ function of state outputs the correct format
    print()
