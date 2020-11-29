"""Walker Finlay\n
Simple A* implementation for pathfinding\n
Takes graph as adjacency list as dictionary"""

from . import grid
from math import inf
import numpy as np
from numpy import array
from heapq import heappush, heappop
from copy import copy

def astar(G, s, ds):

    def d(start,goal):
        "Euclidian distance"
        (x1,y1),(x2,y2) = start,goal
        dx = x2-x1
        dy = y2-y1
        return np.sqrt((dx**2)+(dy**2))
    
    def h(n):
        "Distance to goal"
        return d(n,ds)

    open_set = []
    heappush(open_set,s)
    came_from = {}
    came_from[s] = None
    n=len(G)
    g_score = np.full((n,n),inf, dtype=np.float32)
    g_score[s] = 0
    f_score = np.full((n,n),inf, dtype=np.float32)
    f_score[s] = h(s)
    while open_set:
        current = heappop(open_set)
        if current == ds:
            return grid.backtrace(current, came_from)
        for neighbor in G[current]:
            tentative_gscore = g_score[current] + d(current, neighbor)
            if tentative_gscore < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_gscore
                f_score[neighbor] = g_score[neighbor] + h(neighbor)
                if neighbor not in open_set:
                    heappush(open_set, neighbor)
    return None
