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

def discretize(obstacles: np.array, objectives: np.array, n=20, diagonal=False):
    "gridworld is nxn"
    # Setup
    global rw, rh, cd
    cuboids, cylinders = obstacles
    rob, goal = objectives
    # Map scaling
    scale = n/20
    rw = 4*scale 
    rh = 1*scale 
    cd = 1*scale 
    for i in (cuboids[:,0:2], cylinders[:,0:2], rob, goal): i *= scale
    # Shift obstacles over to positive coordinates
    for i in (cuboids[:,0:2], cylinders[:,0:2], rob, goal): i += n/2

    grid = np.zeros((n,n))

    # Rasterize cylinders
    for cylinder in cylinders:
        fillcircle(grid, (cylinder[0], cylinder[1]), cd/2)
    # Rasterize cuboids
    # Transform centers & alphas to corners

    plot_obstacles(cuboids, cylinders, (rob, goal), shift=True, grid=grid, n=n)


def center2corners(rectaangle):
    # In : (x,y,_,_,_,gamma)
    # Out: ((x1,y1),(x2,y2),(x3,y3),(x4,y4))
    tl = array([-rw/2, rh/2])
    tr = array([rw/2, rh/2])
    br = array([rw/2, -rh/2])
    bl = array([-rw/2, -rh/2])

    return

def fillrectangle(grid, rectangle):
    # TODO: Implement me!
    # Convert center (x,y) and alpha to corners/line segments
    return

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
    return

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

def plot_grid(grid):
    fig,ax = plt.subplots()
    im = ax.imshow(grid)
    plt.show()

# Plotem ----------------------------------------------------------------------
def plot_obstacles(cbds, cyl, objectives, shift=False, n=20, grid=None):
    fig,ax = plt.subplots()

    if grid is not None:
        im = ax.imshow(grid.T)
    plt.gca().invert_xaxis()

    if n < 30:
        plt.grid(which='both')
        ax.set_xticks(np.arange(-0.5,n+1))
        ax.set_yticks(np.arange(-0.5,n+1))

    for i in cyl: # -0.5 is to line it up with the imshow at low resolutions
        ax.add_patch(plt.Circle(i-0.5, radius=cd/2, alpha=0.75))
    for i in cbds:
        # coppelia gives us the center, pyplot wants the bottom left
        x = i[0]     # Initial position
        y = i[1]
        alpha = i[5] # Euler angles
        rotation = array([[cos(alpha), -sin(alpha)],
                        [sin(alpha), cos(alpha)]]) # Rotation
        pt = array([(-rw/2), (-rh/2)]) # Bottom left of the rectangle
        new_pt = rotation.dot(pt) + array([x, y])
        ax.add_patch(plt.Rectangle(new_pt-0.5, rw, rh, degrees(alpha)))

    rob, goal = objectives
    plt.plot(*tuple(rob-0.5), 'ro')     # Omnirob
    plt.plot(*tuple(goal-0.5), 'go')  # Goal 

    if shift == False:
        plt.xlim(-10,10)
        plt.ylim(-10,10)
    plt.gca().set_aspect("equal")
    plt.show(block=True)