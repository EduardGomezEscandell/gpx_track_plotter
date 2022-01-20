from cProfile import label
from src import track
import matplotlib.pyplot as plt
import matplotlib.collections as plt_c
import numpy as np

def plot_multicolored(ax, x, y, c, **kwargs):
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    lc = plt_c.LineCollection(segments, **kwargs)

    lc.set_array(c)
    lc.set_linewidth(2)

    return ax.add_collection(lc)


T = track.Track(location_reference=np.array([0,0,0]))
T.load_gpx("data/2021-12-30_618996228_Creu d'Olorda.gpx")

fig, axs = plt.subplots(2)

col = T.locations[:, 2]
hi = max(col)
lo = min(col)

col = np.array((col - lo) / (hi - lo) * 255, dtype=int)
thickness = np.ones_like(T.time)

line = plot_multicolored(axs[0], T.locations[:,0], T.locations[:,1], T.locations[:,2], label=None)
cbar = fig.colorbar(line, ax=axs[0])
axs[0].plot(T.locations[0,0], T.locations[0,1], 'ro', label='Home')
axs[0].legend()
axs[0].set_xlabel('Longitude')
axs[0].set_ylabel('Latitude')
cbar.set_label('Elevation (m)')

plot_multicolored(axs[1], T.time, T.locations[:,2], T.locations[:,2])
axs[1].set_xlabel('Time [s]')
axs[1].set_ylabel('Elevation [m]')
axs[1].plot(0,0,'-')

plt.show()