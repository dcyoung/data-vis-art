import os.path as osp
import numpy as np
import cv2
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import matplotlib.animation as animation
import math

fish = cv2.imread(osp.join('images', 'fish_small.png'), cv2.IMREAD_UNCHANGED)
# print(fish.shape)
# fish = cv2.resize(img, dsize=(54, 140), interpolation=cv2.INTER_CUBIC)

# convert bgra to rgba
fish = fish[..., [2,0,1,3]]
fish = fish.astype(np.float32) / 255.0
fh, fw, _ = fish.shape
# print(fish.shape)

height = width = 50
t_max = 100

pix_x = []
pix_y = []
frame_index = []
video = np.zeros((height, width, 4, t_max), np.float32)

for t in range(t_max):
    fcx = 0 + 1.0 * width * t / t_max
    fcy = 0 + 1.0 * height * t / t_max
    cx, cy = width // 2, height // 2
    rx, ry = width // 4, height // 4
    # consider the object's position to the the upper left corner
    xmin = int(cx + rx * math.cos(t/4))
    ymin = int(cy + ry * math.sin(t/4))
    xmax = xmin + fw - 1
    ymax = ymin + fh - 1

    video[
        max(0, ymin) : min(height, ymax + 1), 
        max(0, xmin) : min(width, xmax + 1),
        :, 
        t
    ] = fish[
        max(0, -ymin) :  min(fh, max(0, height - ymin)),
        max(0, -xmin) :  min(fw, max(0, width - xmin)),
        :
    ]

    pix_x.append(xmin + fw // 2)
    pix_y.append(height - (ymin + fh // 2))
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
    frame_as_img = np.flip(video[:,:,:,t], 0)
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