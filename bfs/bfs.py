# Python breadth first-search (adjacency list representation)
# Matthew Walker Finlay
# November 2020

# Get path
def backtrace(node, parent):
    path = [node]
    while parent[node]:
        path.append(parent[node])
        node = parent[node]
    path.reverse()
    return path


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
                    return backtrace(neighbor, parent)
                visited.append(neighbor)
                Q.append(neighbor)
    return None


# Testing
graph = {
    'r': ['s', 'v'],
    's': ['r', 'w'],
    't': ['w', 'x', 'u'],
    'u': ['t', 'x', 'y'],
    'v': ['r'],
    'w': ['s', 't', 'x'],
    'x': ['w', 't', 'u', 'y'],
    'y': ['x', 'u']
}
print(bfs(graph, 's', 't'))
