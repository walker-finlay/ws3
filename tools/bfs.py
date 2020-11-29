"""Basic breadth first-search for pathfinding (adjacency list representation as dictionary)\n
Matthew Walker Finlay\n
November 2020"""

from . import grid

# BFS for robot path finding
def bfs(G, s, d):
    # Initialization
    visited = []
    Q = []
    Q.append(s)
    visited.append(s)
    parent = {}
    parent[s] = None

    # Do the bfs
    while Q:
        s = Q.pop(0)
        for neighbor in G[s]:
            if neighbor not in visited:
                parent[neighbor] = s
                if neighbor == d:
                    return grid.backtrace(neighbor, parent)
                visited.append(neighbor)
                Q.append(neighbor)
    return None


