import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import matplotlib.animation as animation
import math


height = width = 30
t_max = 100

pix_x = []
pix_y = []
frame_index = []
video = np.zeros((height, width, t_max), np.uint8)
for t in range(t_max):
    cx, cy = width // 2, height // 2
    rx, ry = width // 4, height // 4
    obj_x = cx + rx * math.cos(t/4)
    obj_y = cy + ry * math.sin(t/4)
    video[int(obj_y), int(obj_x), t] = 1

    pix_x.append(int(obj_x))
    pix_y.append(int(obj_y))
    frame_index.append(t)


fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_xlabel('Frame Index (time)')
ax.set_ylabel('Pixel X')
ax.set_zlabel('Pixel Y')

# set axes to t-max, so the axes don't grow over time
ax.set_xlim([0,t_max])
ax.set_ylim([0,width])
ax.set_zlim([0,height])

# set gridline spacing
loc = plticker.MultipleLocator(base=1.0)
ax.yaxis.set_major_locator(loc)
ax.zaxis.set_major_locator(loc)
ax.grid(which='major', axis='both', linestyle='-')



# line for the trajectory of the object
line, = ax.plot([], [], [], linewidth=5, color='r')

# vertices to paint the image onto
X1, Y1 = np.meshgrid(np.arange(0, width), np.arange(0,height))


def draw_background_image(t):
    # clear any existing image
    if len(ax.collections) > 0:
        del ax.collections[0]
    # retrieve the frame
    frame_as_img = np.stack((video[:,:,t],)*4, axis=-1)
    # draw the frame
    ax.plot_surface(0, X1, Y1, rstride=1, cstride=1, facecolors=frame_as_img)


def init():
    draw_background_image(0)

    line.set_data([], [])
    line.set_3d_properties([])
    
    # adjust the camera location
    ax.view_init(elev=0, azim=0)

    return line

def animate(t):
    draw_background_image(t)

    # draw history of trajectory
    frames = frame_index[:t][::-1]
    x = pix_x[:t]
    y = pix_y[:t]
    line.set_data(frames, x)
    line.set_3d_properties(y)

    # adjust the camera location
    altitude = (1.0 * t / t_max) * 90
    azimuth = (1.0 * t / t_max) * 90
    ax.view_init(elev=altitude, azim=azimuth)

    return line

ani = animation.FuncAnimation(fig, animate, frames=t_max, init_func=init)
plt.show()