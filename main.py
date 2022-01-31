from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import matplotlib.pyplot as plt
from src import track
import numpy as np
import imageio
import os
import shutil

num_frames = 120
fps = 30
regenerate = True

def ReadTrack(filename) -> track.Track:
    t = track.Track()
    t.load_gpx(f"data/{filename}")
    print(f"Read {filename}")
    return t

if regenerate:
    filenames = os.listdir("data")
    filenames.sort()

    i = 0
    with ProcessPoolExecutor() as exec:
        futures = [exec.submit(ReadTrack, filename) for filename in filenames]
        tracklist = [future.result() for future in futures]


    max_t = 0
    min_lat =  360
    max_lat = -360
    min_lon =  360
    max_lon = -360

    for trk in tracklist:
        LAT = track.Track.LAT
        LON = track.Track.LON

        max_t = max(max_t, trk.timestamps[-1])

        min_lat = min(min_lat, min(trk.locations[:, LAT]))
        max_lat = max(max_lat, max(trk.locations[:, LAT]))

        min_lon = min(min_lon, min(trk.locations[:, LON]))
        max_lon = max(max_lon, max(trk.locations[:, LON]))

    try:
        shutil.rmtree("result")
    except FileNotFoundError:
        pass

    try:
        os.mkdir("result")
    except FileExistsError:
        pass


    T = np.linspace(0, max_t, num_frames)
    for i in range(num_frames):
        t = T[i]
        fig, ax = plt.subplots(1)
        for trk in tracklist:
            trk.plot_track_until(fig, ax, t)
        print(f't = {t / 60}')

        ax.set_xlim(min_lon, max_lon)
        ax.set_ylim(min_lat, max_lat)
        
        ax.axis('off')
        fig.savefig(f'result/frame{i:0>5}.png', bbox_inches='tight')
        plt.close(fig)

# Build GIF
with imageio.get_writer('mygif.gif', mode='I', fps=fps) as writer:
    framenames = os.listdir("result")
    framenames.sort()
    for filename in framenames:
        image = imageio.imread(f"result/{filename}")
        writer.append_data(image)