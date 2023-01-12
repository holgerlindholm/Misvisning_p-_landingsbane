
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FormatStrFormatter



#opens data file, has to be in the same folder as this script 
data= pd.read_csv("magdata.csv")
#prints the header  
print("data struktur")
print(data.columns)


#assignes the x,y,z data to variables
#x = data.z
#y = data.y
#z = data.x

#assignes the rawx,rawy, rawz data to variables 
rawx = data.x_rå
rawy = data.y_rå
rawz = data.z_rå


def set_axes_equal(ax):
    '''Make axes of 3D plot have equal scale so that spheres appear as spheres,
    cubes as cubes, etc..  This is one possible solution to Matplotlib's
    ax.set_aspect('equal') and ax.axis('equal') not working for 3D.

    Input
      ax: a matplotlib axis, e.g., as output from plt.gca().
     
    from https://stackoverflow.com/questions/13685386/matplotlib-equal-unit-length-with-equal-aspect-ratio-z-axis-is-not-equal-to
    '''

    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    x_range = abs(x_limits[1] - x_limits[0])
    x_middle = np.mean(x_limits)
    y_range = abs(y_limits[1] - y_limits[0])
    y_middle = np.mean(y_limits)
    z_range = abs(z_limits[1] - z_limits[0])
    z_middle = np.mean(z_limits)

    # The plot bounding box is a sphere in the sense of the infinity
    # norm, hence I call half the max range the plot radius.
    plot_radius = 0.5*max([x_range, y_range, z_range])

    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
    ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])

#creates a scatterplot with the x,y,z data

fig1 = plt.figure(1)
ax1 = fig1.add_subplot(projection='3d')
ax1.set_aspect('auto')

scat = ax1.scatter(rawx, rawy, rawz, c="r")
ax1.set_xlabel("x")
ax1.set_ylabel("y")
ax1.set_zlabel("z")
ax1.set_title("Rå flad data")
ax1.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
ax1.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
ax1.zaxis.set_major_formatter(FormatStrFormatter('%.0f'))


set_axes_equal(ax1)
plt.show()
