from tools.bfs import bfs
from tools.astar import astar
from numpy import array, zeros, concatenate, append
from copy import copy
from tools.fields import cuboids2fields, cylinders2fields
from tools.Potential_functions import plot_vector_field
from matplotlib import pyplot as plt
from tools.grid import discretize, build_graph, plot_grid

Manhattan = [
    array([0,1]),
    array([1,0]),
    array([0,-1]),
    array([-1,0])
]
Diagonal = copy(Manhattan)
Diagonal.extend(
    [
        array([1,1]),
        array([1,-1]),
        array([-1,-1]),
        array([-1,1])
    ]
)

# Cylinders [x,y,z]
cylinders = array([[-0.51850247, 6.2966156, 1.50205004],
    [-5.12347126, 3.42501903,   1.50205004],
    [ 2.81749773, -4.84758282,  1.50205004],
    [ 4.39067745,  0.87337959,  1.50204992],
    [ 2.42127442,  4.07621098,  1.50204992],
    [ 7.27389908, -7.7498498,   1.50204992],
    [-5.7925663,  -0.97721177,  1.50204992],
    [-1.76908493,  2.09850359,  1.50204992]])

# Cuboids [x,y,z,alpha,beta,gamma]
cuboids = array([
    [-5.15000153e+00, -6.20000076e+00,  1.00204980e+00,  7.74395964e-11, -1.65637074e-10,  2.61799550e+00],
    [ 2.72499943e+00, -2.62746937e-07,  1.00204980e+00,  7.19939275e-10,  9.51887902e-10, -6.98131919e-0],
    [ 7.42500019e+00,  4.72499943e+00,  1.00204980e+00, -1.20863564e-09,  1.59285729e-09, -2.19689253e-10],
    [-1.02500236e+00, -1.50000072e+00,  1.00204980e+00,  5.95255734e-10, -8.81065887e-10,  3.89464933e-10],
    [-6.70000172e+00,  6.40000153e+00,  1.00204980e+00, -4.02774747e-09, -4.97467756e-09, -1.31661071e-11]]
)

rob = array([7.625, 8.55])
goal = array([-7.425, -7.925])

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


# Potential Fields
# cub_fields = cuboids2fields(cuboids)
# cyl_fields = cylinders2fields(cylinders)
# obstacles = concatenate((cub_fields,cyl_fields),axis=0)
# plot_vector_field(append(goal, 0.02), obstacles)
# plt.gca().set_aspect("equal")
# plt.show()

# Graph algorithms
grid, poi = discretize((cuboids, cylinders), (rob, goal),n=50)
rob, goal = poi
G = build_graph(grid, heuristic=Diagonal)
path = bfs(G, rob, goal)
# path = astar(G, rob, goal)
plot_grid(grid,path)