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


def exp(filepath, search_mode):
    grid_init, nsharp = read_instance_file(filepath)
    init_state = State(grid_init)

    start_time = time.time()

    problem = Pacmen(init_state)

    if search_mode == "h1":
        node = astar_graph_search(problem, h1)
    elif search_mode == "h2":
        node = astar_graph_search(problem, h2)
    else:
        raise ValueError("This search mode does not exist!")

    interval = time.time() - start_time
    print('\tTime : ' + str(interval))
    print('\tNB node explored : ' + str(problem.nb_explored_nodes))

    path = node.path()
    path.reverse()

    print('\tNumber of moves: ' + str(node.depth))


if __name__ == "__main__":
    heuristics = ["h1", "h2"]
    print("Experiment with all instances and all uninformed search algorithms.")

    for instance in os.listdir("instances"):
        print("\n\nInstance " + instance + " :")
        for heuristic in heuristics:
            print("\n" + heuristic)
            exp("instances/" + instance, heuristic)
