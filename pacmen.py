# -*-coding: utf-8 -*
"""NAMES OF THE AUTHOR(S): Gael Aglin <gael.aglin@uclouvain.be>, Francois Aubry <francois.aubry@uclouvain.be>,
   Simon Calbert <simon.calbert@student.uclouvain.be, Quentin Guimard <quentin.guimard@student.uclouvain.be>"""
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

        new_state = state.clone()
        actions = []

        def aux(state, actions):
            """Recursive function that will return all the possible combinations of moves,
               according to the number of pacmen"""
            pacman = len(actions)
            (x, y) = state.pacmen[pacman]

            if x > 0 and state.grid[x - 1][y] in {' ', '@', '$'}:
                new_state = state.clone()
                new_state.move(pacman, 'up')
                new_actions = actions + ['up', ]
                if pacman == len(state.pacmen) - 1:
                    yield (new_actions, new_state)
                else:
                    yield from aux(new_state, new_actions)

            if x + 1 < state.nbr and state.grid[x + 1][y] in {' ', '@', '$'}:
                new_state = state.clone()
                new_state.move(pacman, 'down')
                new_actions = actions + ['down', ]
                if pacman == len(state.pacmen) - 1:
                    yield (new_actions, new_state)
                else:
                    yield from aux(new_state, new_actions)

            if y + 1 < state.nbc and state.grid[x][y + 1] in {' ', '@', '$'}:
                new_state = state.clone()
                new_state.move(pacman, 'right')
                new_actions = actions + ['right', ]
                if pacman == len(state.pacmen) - 1:
                    yield (new_actions, new_state)
                else:
                    yield from aux(new_state, new_actions)

            if y > 0 and state.grid[x][y - 1] in {' ', '@', '$'}:
                new_state = state.clone()
                new_state.move(pacman, 'left')
                new_actions = actions + ['right', ]
                if pacman == len(state.pacmen) - 1:
                    yield (new_actions, new_state)
                else:
                    yield from aux(new_state, new_actions)

        yield from aux(new_state, actions)

    def goal_test(self, state):
        return state.foods_left == 0


###############
# State class #
###############
class State:
    def __init__(self, grid, nsharp):
        self.nbr = len(grid)
        self.nbc = len(grid[0])
        self.grid = grid
        self.nsharp = nsharp

        # Positions of the pacmen
        self.pacmen = []
        # Positions of the foods
        self.foods = []
        # Number of foods remaining
        self.foods_left = 0

    def __str__(self):
        s = ""
        for a in range(self.nsharp):
            s = s + "#"
        s = s + '\n'
        for i in range(0, self.nbr):
            s = s + "# "
            for j in range(0, self.nbc):
                s = s + str(self.grid[i][j]) + " "
            s = s + "#"
            if i < self.nbr:
                s = s + '\n'
        for a in range(self.nsharp):
            s = s + "#"
        return s

    def __eq__(self, o):
        return self.grid == o.grid

    def __hash__(self):
        hashable_grid = []
        for i in range(0, self.nbr):
            hashable_grid.append(tuple(self.grid[i]))
        return hash(tuple(hashable_grid))

    def clone(self):
        """Clone method of State, allowing a deep copy of the state class."""
        new_grid = [[0 for i in range(self.nbc)] for j in range(self.nbr)]
        for i in range(0, self.nbr):
            new_grid[i] = list(self.grid[i])
        new_state = State(new_grid, self.nsharp)
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

    def move(self, pacman, direction):
        """Move modifies the grid according to the chosen pacman and direction.
           The chosen pacman is moved and replaced by a space.
           The variables self.pacmen, self.foods and self.foods_left are updated if needed."""
        (x, y) = self.pacmen[pacman]
        self.grid[x][y] = ' '

        if direction == 'left':
            if self.grid[x][y - 1] == '@':
                self.foods_left -= 1
                self.foods.remove((x, y - 1))
            self.grid[x][y - 1] = '$'
            self.pacmen[pacman] = (x, y - 1)

        elif direction == 'right':
            if self.grid[x][y + 1] == '@':
                self.foods_left -= 1
                self.foods.remove((x, y + 1))
            self.grid[x][y + 1] = '$'
            self.pacmen[pacman] = (x, y + 1)

        elif direction == 'up':
            if self.grid[x - 1][y] == '@':
                self.foods_left -= 1
                self.foods.remove((x - 1, y))
            self.grid[x - 1][y] = '$'
            self.pacmen[pacman] = (x - 1, y)

        elif direction == 'down':
            if self.grid[x + 1][y] == '@':
                self.foods_left -= 1
                self.foods.remove((x + 1, y))
            self.grid[x + 1][y] = '$'
            self.pacmen[pacman] = (x + 1, y)

        else:
            raise ValueError('Impossible to move in this direction.')


######################
# Auxiliary functions #
######################
def read_instance_file(filename):
    lines = [[char for char in line.rstrip('\n')[1:][:-1]] for line in open(filename)]
    nsharp = len(lines[0]) + 2
    lines = lines[1:len(lines) - 1]
    n = len(lines)
    m = len(lines[0])
    grid_init = [[lines[i][j] for j in range(1, m, 2)] for i in range(0, n)]
    return grid_init, nsharp


def manhattan_distance(pos1, pos2):
    """Calculates the manhattan distance between two positions"""
    (x1, y1) = pos1
    (x2, y2) = pos2

    return abs(x2 - x1) + abs(y2 - y1)


def adj(grid, v):
    """Returns the adjacent tiles on which a pacman can move"""
    nbr = len(grid)
    nbc = len(grid[0])
    x = v[0]
    y = v[1]
    neig = []
    if x > 0 and grid[x - 1][y] in {' ', '@', '$'}:
        neig.append((x - 1, y))
    if x + 1 < nbr and grid[x + 1][y] in {' ', '@', '$'}:
        neig.append((x + 1, y))
    if y + 1 < nbc and grid[x][y + 1] in {' ', '@', '$'}:
        neig.append((x, y + 1))
    if y > 0 and grid[x][y - 1] in {' ', '@', '$'}:
        neig.append((x, y - 1))
    return neig


def bfs_matrix(grid, pacman, goal):
    """Performs a BFS in the grid from pacman (position) to a given goal (character)
       It returns the distance to shortest goal found, as well as its position"""
    nbr = len(grid)
    nbc = len(grid[0])
    dist = [[0 for i in range(nbc)] for j in range(nbr)]
    marked = [[False for i in range(nbc)] for j in range(nbr)]

    def bfs(grid):
        queue = []
        marked[pacman[0]][pacman[1]] = True
        queue.append(pacman)
        while len(queue) != 0:
            v = queue.pop(0)
            for w in adj(grid, v):
                if not marked[w[0]][w[1]]:
                    dist[w[0]][w[1]] = dist[v[0]][v[1]] + 1
                    if grid[w[0]][w[1]] in goal:
                        return dist[w[0]][w[1]], (w[0], w[1])
                    marked[w[0]][w[1]] = True
                    queue.append(w)

    return bfs(grid)


######################
# Heuristic functions #
######################
def h0(node):  # Test heuristic, equivalent to BFSg
    return 0.0


def h1(node):  # Simplest consistent heuristic
    return node.state.foods_left


def h2(node):  # Very bad heuristic
    h = 0.0
    for pacman in node.state.pacmen:
        for food in node.state.foods:
            h += manhattan_distance(pacman, food)
    return h


def h4(node):  # Consistent heuristic
    if node.state.foods_left == 0:
        return 0.0
    max_dist_food = 0
    for food in node.state.foods:
        dist, elem = bfs_matrix(node.state.grid, food, ['$'])
        if dist > max_dist_food:
            max_dist_food = dist
    h = max_dist_food
    return h


def h5(node):  # Consistent heuristic for 1 pacman, but inconsistent for more than 1
    if node.state.foods_left == 0:
        return 0.0
    h = 0.0
    for food in node.state.foods:
        dist, elem = bfs_matrix(node.state.grid, food, ['$'])
        h += dist
    return h


def h6(node):  # Inconsistent heuristic, yet very efficient
    if node.state.foods_left == 0:
        return 0.0
    h = 0.0
    for food in node.state.foods:
        dist, elem = bfs_matrix(node.state.grid, food, ['$', '@'])
        h += dist
    return h


#####################
# Launch the search #
#####################
if __name__ == "__main__":
    grid_init, nsharp = read_instance_file(sys.argv[1])
    init_state = State(grid_init, nsharp)

    problem = Pacmen(init_state)

    node = astar_graph_search(problem, h6)

    # example of print
    path = node.path()
    path.reverse()

    print('Number of moves: ' + str(node.depth))
    for n in path:
        print(n.state)  # assuming that the __str__ function of state outputs the correct format
        print()
