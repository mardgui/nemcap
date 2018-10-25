#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 18:54:51 2018

@author: calbert
@author: guimard
"""

from pacmen import *
from search import *
import time
import os


def exp(filepath, heuristic):
    grid_init, nsharp = read_instance_file(filepath)
    init_state = State(grid_init, nsharp)

    start_time = time.time()

    problem = Pacmen(init_state)

    node = astar_graph_search(problem, heuristic)

    interval = time.time() - start_time
    print('\tTime : ' + str(interval))
    print('\tNB node explored : ' + str(problem.nb_explored_nodes))

    path = node.path()
    path.reverse()

    print('\tNumber of moves: ' + str(node.depth))
    for n in path:
        print(n.state)  # assuming that the __str__ function of state outputs the correct format
        print()


if __name__ == "__main__":
    heuristics = [h0, h1, h2]
    print("Experiment with all instances and all uninformed search algorithms.")

    for instance in os.listdir("instances"):
        print("\n\nInstance " + instance + " :")
        for heuristic in heuristics:
            print("\n" + str(heuristic))
            exp("instances/" + instance, heuristic)
