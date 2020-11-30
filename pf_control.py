import numpy as np
from time import sleep
from tools.Potential_functions import total_force
from tools.fields import cuboids2fields, cylinders2fields
from tools.coppelia import coppelia
from tools.robot import robot

# Setup ---------------------------------------------------
# Get the locations of the obstacles from sim
cuboids, cylinders = coppelia()
cub_fields = cuboids2fields(cuboids)
cyl_fields = cylinders2fields(cylinders)
obstacles = np.concatenate((cub_fields,cyl_fields),axis=0)

# Send commands to omnirob --------------------------------
motor_names = ['Omnirob_FLwheel_motor', 'Omnirob_FRwheel_motor', 'Omnirob_RRwheel_motor', 'Omnirob_RLwheel_motor']
r = robot('Omnirob', motor_names)  # Create an instance of our robot
goal = r.get_object_position('Sphere9')
goal[2] = 0.02

while True:
    x,y,_ = r.get_position()
    # Get current coords and calculate total force on those coords
    Fx, Fy = total_force(x, x, goal, obstacles)
    speed_mult = 3
    Fx, Fy = (Fx*speed_mult, Fy*speed_mult)
    r.send_motor_velocities([-Fy - Fx, Fy - Fx, Fy + Fx, -Fy + Fx])
    sleep(0.2)
    # TODO: find a reasonable exit condition
r.close_connection()
