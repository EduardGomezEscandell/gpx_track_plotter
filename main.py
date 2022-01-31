from src import track
import matplotlib.pyplot as plt
import os
from concurrent.futures import ProcessPoolExecutor

def ReadTrack(filename) -> track.Track:
    t = track.Track()
    t.load_gpx(f"data/{filename}")
    print(f"Read {filename}")
    return t

filenames = os.listdir("data")
filenames.sort()

i = 0
with ProcessPoolExecutor() as exec:
    futures = [exec.submit(ReadTrack, filename) for filename in filenames]
    tracklist = [future.result() for future in futures]

fig, axs = plt.subplots(1)

for trk in tracklist:
    trk.plot_track(fig, axs)

plt.show()