#!/usr/bin/env python
# coding: utf-8

# Forked from https://github.com/dsaldana/CSE360-MobileRobotics


# In[]:

import matplotlib
from matplotlib import pyplot as plt
from matplotlib.pyplot import plot
import numpy as np

# get_ipython().run_line_magic('pylab', 'inline')
# plt.style.use('dark_background')
# pylab.rcParams['figure.figsize'] = (10.0, 6.0)
matplotlib.rcParams['animation.embed_limit'] = 2**128


# # Potential functions

# In[2]:


# Potential functions
def force_goal(x, y, goal):
    goal_x, goal_y, k_goal = goal
    Fx_goal, Fy_goal = k_goal * (goal_x - x), k_goal *(goal_y - y)
    return Fx_goal, Fy_goal

def force_obstacle(x, y, obstacle):
    (obs_x, obs_y, k_obs) = obstacle
    dist_x, dist_y = x - obs_x, y - obs_y
    dist_obs = np.hypot(dist_x, dist_y)
    Fx_obs = (dist_x / dist_obs) * k_obs / dist_obs ** 3
    Fy_obs = (dist_y / dist_obs) * k_obs / dist_obs ** 3

    return Fx_obs, Fy_obs 

def total_force(x, y, goal, obstacles):
    Fx, Fy = force_goal(x, y, goal)

    for obs in obstacles:
        Fo_x, Fo_y = force_obstacle(x, y, obs)
        Fx += Fo_x
        Fy += Fo_y
    return Fx, Fy


# In[68]:

def plot_vector_field(goal, obstacles, ax=plt, fmax = .5):
   X, Y = np.meshgrid(np.arange(-10, 10, .5), np.arange(-10, 10, .5))

   # Vector field of the forces
   Fx, Fy = total_force(X, Y, goal, obstacles)

   # For visualization
   F_m = np.hypot(Fx, Fy)
   Fx[F_m > fmax], Fy[F_m > fmax] = None, None
   # Plot
   # quiver(X, Y, Fx, Fy,  F_m, color='0.4', scale=None)
   ax.quiver(X, Y, Fx, Fy, color='0.4')
   
def simulate(q, goal, obstacles, num_steps=200, delta_time=1.9):
   trajectory = []
   for i in range(num_steps):
       force = total_force(q[0], q[1], goal, obstacles)
       # Robot velocity follows the force vector
       vel = np.array(force)
       # Integrate
       q += vel * delta_time
       trajectory.append(np.copy(q))

   return np.array(trajectory)
