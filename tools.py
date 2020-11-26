import numpy as np
from numpy import array, sin, cos, degrees, floor, ceil, sqrt
import matplotlib.pyplot as plt 

"---------- Globals ----------"
Manhattan = [
    array([0,1]),
    array([1,0]),
    array([0,-1]),
    array([-1,0])
]
Diagonal = Manhattan.append(
    [
        array([1,1]),
        array([1,-1]),
        array([-1,-1]),
        array([-1,1])
    ]
)
rw = None   # Rectangle width
rh = None   # Rectangle height
cd = None   # Cylinder diameter
some_corners = None

def discretize(obstacles: np.array, objectives: np.array, n=20, diagonal=False):
    "gridworld is nxn"
    # Setup
    global rw, rh, cd, some_corners
    cuboids, cylinders = obstacles
    rob, goal = objectives
    # Map scaling
    scale = n/20
    rw = 4*scale 
    rh = 1*scale 
    cd = 1*scale 
    tl = array([-rw/2, rh/2])   # Rectangle corners at the origin
    tr = array([rw/2, rh/2])    # | this should only be
    br = array([rw/2, -rh/2])   # | calculated once
    bl = array([-rw/2, -rh/2])  # |
    some_corners = array([tl, tr, br, bl]).T
    for i in (cuboids[:,0:2], cylinders[:,0:2], rob, goal): i *= scale
    # Shift map over to positive coordinates
    for i in (cuboids[:,0:2], cylinders[:,0:2], rob, goal): i += n/2

    grid = np.zeros((n,n))

    # Rasterize cylinders
    for cylinder in cylinders: fillcircle(grid, (cylinder[0], cylinder[1]), cd/2)
    # Rasterize cuboids
    for cuboid in cuboids: fillrectangle(grid, (cuboid[0], cuboid[1]), cuboid[5])

    plot_obstacles(cuboids, cylinders, (rob, goal), grid=grid, n=n)


def center2corners(center, gamma):
    "returns corners as 2x4 array"
    # In : ((x,y),gamma)
    # Out: ((x1,y1),(x2,y2),(x3,y3),(x4,y4))
    r = array([[cos(gamma), -sin(gamma)],
               [sin(gamma),  cos(gamma)]])
    return np.add(r.dot(some_corners).T, center).T

def draw_line(grid, edge):
    # TODO: Implement me!
    (x1,y1),(x2,y2) = edge
    slope = (y2-y1)/(x2-x1)
    for x in np.arange(int(x1),int(x2)):
        grid[x, x+int(slope)] = 1

def fillrectangle(grid, center, gamma):
    return
    # TODO: Implement me!
    corners = center2corners(center, gamma)
    edges = array([(corners[:,0],corners[:,1]),
                (corners[:,2],corners[:,3]),
                (corners[:,1],corners[:,2]),
                (corners[:,3],corners[:,0])])
    for edge in edges: draw_line(grid, edge)

def fillcircle(grid, center, radius):
    "Set interior of circle to 1 in grid" # FIXME what if circle is outside grid?
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

def build_graph(n, heuristic=Manhattan):
    "Build adjacency list for bfs"
    G = {}
    return
    for i in range(0, n):
        for j in range(0, n):
            current = (i,j)
            G[current] = []
            for direction in heuristic:
                next = (i+direction[0], j+direction[1])
                if next[0] >= 0 and next[0] < n and next[1] >= 0 and next[1] < n :
                    G[current].append(next)

# Plotem ----------------------------------------------------------------------
def plot_obstacles(cbds, cyl, poi, n=20, grid=None):
    fig,ax = plt.subplots()
    offset = 0

    if grid is not None:
        im = ax.imshow(grid.T)
        offset = 0.5
    plt.gca().invert_xaxis()

    testcorners = center2corners((cbds[0,0],cbds[0,1]), cbds[0,5])
    plt.plot(testcorners[0]-offset,testcorners[1]-offset,'wo')
    print(testcorners)

    if n < 30:
        plt.grid(which='both')
        ax.set_xticks(np.arange(-offset,n+1))
        ax.set_yticks(np.arange(-offset,n+1))

    for i in cyl: # -0.5 is to line it up with the imshow at low resolutions
        ax.add_patch(plt.Circle(i-offset, radius=cd/2, alpha=0.75))
    for i in cbds:
        # coppelia gives us the center, pyplot wants the bottom left
        x = i[0]     # Initial position
        y = i[1]
        gamma = i[5] # Euler angles
        rotation = array([[cos(gamma), -sin(gamma)],
                        [sin(gamma), cos(gamma)]]) # Rotation
        pt = array([(-rw/2), (-rh/2)]) # Bottom left of the rectangle
        new_pt = rotation.dot(pt) + array([x, y])
        ax.add_patch(plt.Rectangle(new_pt-offset, rw, rh, degrees(gamma)))

    rob, goal = poi
    plt.plot(*tuple(rob-offset), 'ro')     # Omnirob
    plt.plot(*tuple(goal-offset), 'go')  # Goal 

    plt.gca().set_aspect("equal")
    plt.show(block=True)