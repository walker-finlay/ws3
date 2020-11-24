from bfs import bfs


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
print(bfs(graph, 's', 'y'))