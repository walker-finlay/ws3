""" Walker Finlay
Helper functions for grid and graph creation """

import numpy as np
from numpy import array, sin, cos, degrees, floor, ceil, sqrt
import matplotlib.pyplot as plt 

"---------- Globals ----------"
size = 20
rw = None   # Rectangle width
rh = None   # Rectangle height
cd = None   # Cylinder diameter
some_corners = None

def discretize(obstacles: np.array, objectives: np.array, n=20, diagonal:bool=False, sf:float=1.0):
    """gridworld is nxn, takes obstacles=(cuboids,cylinders), objectives = (rob,goal)\n
    Keyword Arguments:\n
    sf: float => scaling factor - grow obstacles so rob doesn't crash into them\n
    diagonal: bool => allow diagonal movement?"""
    # Setup ----------------------
    global rw, rh, cd, some_corners, size
    size = n
    cuboids, cylinders = obstacles
    rob, goal = objectives
    # Map scaling ----------------
    scale = n/20
    rw = 4*scale*sf
    rh = 1*scale*sf
    cd = 1*scale*sf 
    tl = array([-rw/2, rh/2])   # Rectangle corners at the origin
    tr = array([rw/2, rh/2])    # | this should only be
    br = array([rw/2, -rh/2])   # | calculated once
    bl = array([-rw/2, -rh/2])  # |
    some_corners = array([tl, tr, br, bl]).T
    for i in (cuboids[:,0:2], cylinders[:,0:2], rob, goal): i *= scale
    # Shift to pos. --------------
    for i in (cuboids[:,0:2], cylinders[:,0:2], rob, goal): i += n/2

    grid = np.zeros((n,n), dtype=np.int8)
    # Rasterize cuboids
    for cuboid in cuboids: fillrectangle(grid, (cuboid[0], cuboid[1]), cuboid[5])
    # Rasterize cylinders
    for cylinder in cylinders: fillcircle(grid, (cylinder[0], cylinder[1]), cd/2)
    # Move rob and goal to the nearest integer
    poi = (tuple(rob.astype(int)), tuple(goal.astype(int)))

    return grid, poi


def center2corners(center, gamma):
    """returns corners as 2x4 array"""
    # In : ((x,y),gamma)
    # Out: ((x1,y1),(x2,y2),(x3,y3),(x4,y4))
    r = array([[cos(gamma), -sin(gamma)],
               [sin(gamma),  cos(gamma)]])
    return np.add(r.dot(some_corners).T, center).T

def draw_line(grid, edge):
    (x1,y1),(x2,y2) = edge
    # We want to go toward positive x
    if x1 > x2: (x1,y1),(x2,y2) = (x2,y2),(x1,y1)
    dx = x2 - x1
    dy = y2 - y1
    for x in range(int(x1+0.5),int(x2+0.5)):
        if not (x >= size):
            y = int(y1 + dy*(x - x1) / dx)
            grid[x,y] = 1

def fill_helper(grid, corners):
    """Use the drawn lines to fill by scanning vertically"""
    # Draw a box around it
    xmax = int(max(corners[0])+0.5+1)
    ymax = int(max(corners[1])+0.5+1)
    xmin = int(min(corners[0])+0.5-1)
    ymin = int(min(corners[1])+0.5-1)
    first = None
    for x in range(xmin, xmax):
        fill = 0
        if (x >= size): break
        for y in range(ymin, ymax):
            if grid[x,y] == 1:
                first = y
                fill += 1
                if fill == 2: break
                continue
            grid[x,y] = fill
        if fill == 1: 
            grid[x,first:ymax] = 0

def fillrectangle(grid, center, gamma):
    corners = center2corners(center, gamma)
    edges = array([(corners[:,0],corners[:,1]),
                (corners[:,2],corners[:,3]),
                (corners[:,1],corners[:,2]),
                (corners[:,3],corners[:,0])])
    for edge in edges: draw_line(grid, edge)
    fill_helper(grid, corners)

def distance():
    return

def fillcircle(grid, center, radius):
    """Set interior of circle to 1 in grid""" # FIXME what if circle is outside grid?
    # Work on a little box around the circle
    x1 = int(center[0] - radius)        # Below right
    y1 = int(center[1] - radius)        # |
    x2 = int(ceil(center[0] + radius))  # Above left
    y2 = int(ceil(center[1] + radius))  # |
    for x in range(x1, x2): # Sampling
        for y in range(y1, y2):
            dx = x - center[0] + 0.5
            dy = y - center[1] + 0.5
            d = sqrt(dx**2 + dy**2)
            if d <= radius+1:
                grid[x,y] = 1

def build_graph(grid, heuristic):
    """Build adjacency list for bfs"""
    G = {}
    n = len(grid)
    for i in range(0, n):
        for j in range(0, n):
            current = (i,j)
            G[current] = []
            for direction in heuristic:
                next_node = (i+direction[0], j+direction[1])
                if next_node[0] >= 0 and next_node[0] < n and next_node[1] >= 0 and next_node[1] < n and grid[next_node] == 0:
                    G[current].append(next_node)
    return G


# Get path
def backtrace(node, parent):
    path = [node]
    while parent[node]:
        path.append(parent[node])
        node = parent[node]
    path.reverse()
    return path

def path2waypoints(path, n, m, t):
    """turn path from nxn grid into waypoints
    in mxm space with time t to get to adjacent squares
    centered at (0,0)"""
    time = 0
    scale = m/n
    waypoints = []
    i = 0
    time_diag = t * (1 + (sqrt(2)/2))
    for square in path:
        time = t
        if i < len(path)-1: # It should travel slower on diagonals
            next_square = path[i+1]
            if abs(next_square[0] - square[0]) > 0.1 and abs(next_square[1] - square[1]) > 0.1:
                time = time_diag
        # Scale & shift to (0,0)
        scaled = (scale * square[0] - m/2, scale * square[1] - m/2)
        waypoints.append([scaled,time])
        i += 1
    return waypoints

# Plotem ----------------------------------------------------------------------
def plot_obstacles(cbds, cyl, poi, n=20, grid=None):
    """Keyword arguments:  
    n -- the size of the map  
    grid -- optional grid to overlay
    """
    fig,ax = plt.subplots()
    offset = 0

    if grid is not None:
        offset = 0.5
        im = ax.imshow(grid.T)
    plt.gca().invert_yaxis()

    if n < 30:
        plt.grid(which='both')
        ax.set_xticks(np.arange(-offset,n+1))
        ax.set_yticks(np.arange(-offset,n+1))

    for i in cyl: # -0.5 is to line it up with the imshow at low resolutions
        ax.add_patch(plt.Circle(i-offset, radius=cd/2, alpha=1-offset/2))
    for i in cbds:
        # coppelia gives us the center, pyplot wants the bottom left
        x = i[0]     # Initial position
        y = i[1]
        gamma = i[5] # Euler angles
        rotation = array([[cos(gamma), -sin(gamma)],
                        [sin(gamma), cos(gamma)]]) # Rotation
        pt = array([(-rw/2), (-rh/2)]) # Bottom left of the rectangle
        new_pt = rotation.dot(pt) + array([x, y])
        ax.add_patch(plt.Rectangle(new_pt-offset, rw, rh, degrees(gamma), alpha=1-offset/2))

    rob, goal = poi
    plt.plot(*tuple(rob-offset), 'ro')     # Omnirob
    plt.plot(*tuple(goal-offset), 'go')  # Goal 

    plt.gca().set_aspect("equal")
    plt.show(block=True)

def plot_grid(grid, path=None):
    if path is not None:
        for p in path:
            grid[p] = 2
    fig, ax = plt.subplots()
    ax.imshow(grid.T)
    plt.gca().invert_yaxis()
    plt.show()
