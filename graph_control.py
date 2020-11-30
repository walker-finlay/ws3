from tools.coppelia import coppelia
from tools.bfs import bfs
from tools.astar import astar
from tools.grid import discretize, build_graph, path2waypoints, plot_grid
from robot import robot
from numpy import array, linspace
import time


Diagonal = [
    array([0,1]),
    array([1,0]),
    array([0,-1]),
    array([-1,0]),
    array([1,1]),
    array([1,-1]),
    array([-1,-1]),
    array([-1,1])
]

# Get obstacle info from sim
cuboids, cylinders = coppelia()

# Initialize rob & get goal
motor_names = ['Omnirob_FLwheel_motor', 'Omnirob_FRwheel_motor', 'Omnirob_RRwheel_motor', 'Omnirob_RLwheel_motor']
r = robot('Omnirob', motor_names)  # Create an instance of our robot
rob = r.get_position()[0:2]
goal = r.get_object_position('Sphere9')[0:2]

# Discretize, build graph, bfs
grid, poi = discretize((cuboids, cylinders), (rob, goal),n=50, sf=2)
rob, goal = poi # Points of interest in discrete coordinates
G = build_graph(grid, heuristic=Diagonal)
# path = bfs(G, rob, goal)
path = astar(G, rob, goal)

# Scale down path & add times
n = len(grid)
# Array of waypoints looking like [center, time]
# Scaled and shifted to coppelia map
waypoints = path2waypoints(path, n, 20, 0.5)

# Execute it as a polyline trajectory
i = 0
for wp in waypoints:
    print(wp)
    tf = wp[1]
    time_steps = linspace(0, tf, 500)
    robot_position = r.get_position()[0:2]
    desired_position = wp[0]

    a1 = (desired_position - robot_position) / tf
    a0 = robot_position

    for t in time_steps:
        point_traj = a1 * t + a0
        vel_traj = a1
        
        # Sensing
        robot_position = r.get_position()[0:2]
        
        # Trajectory tracker
        u = 10 * (point_traj - robot_position) + vel_traj
        
        vx, vy = u
        r.send_motor_velocities([-vy - vx, vy - vx, vy + vx, -vy + vx])
        
        time.sleep(tf/500)

r.close_connection()