from concurrent.futures import ProcessPoolExecutor
import matplotlib.pyplot as plt
import numpy as np
import shutil
import cv2
import os

from src.defines import LAT, LON
from src import track
from src import map

class AnimationBuilder:
    results_dir = "result"
    data_dir = "data"

    def __init__(self, num_frames, imgsize, dpi, colourmap, map_settings):
        self.num_frames = num_frames
        self.imgsize = imgsize
        self.dpi = dpi
        self.colourmap = colourmap
        self.map_settings = map_settings

    @classmethod
    def _ReadTrack(cls, filename) -> track.Track:
        t = track.Track()
        t.load_gpx(f"{cls.data_dir}/{filename}")
        print(f"Read {filename}")
        return t

    @classmethod
    def _GenerateResultsDir(cls) -> None:
        try:
            shutil.rmtree(cls.results_dir)
        except FileNotFoundError:
            pass

        try:
            os.mkdir(cls.results_dir)
        except FileExistsError:
            pass

    def _FindExtrema(self):
        extrema = {
            "max_lon" : -360,
            "min_lon" :  360,
            "max_lat" : -360,
            "min_lat" :  360
        }
        for track in self.tracklist:
            extrema["max_lon"] = max(extrema["max_lon"], max(track.locations[:, LON]))
            extrema["min_lon"] = min(extrema["min_lon"], min(track.locations[:, LON]))
            extrema["max_lat"] = max(extrema["max_lat"], max(track.locations[:, LAT]))
            extrema["min_lat"] = min(extrema["min_lat"], min(track.locations[:, LAT]))
        return extrema

    def _GenerateSingleFrame(self, T: list, map_: map.Map, size: tuple, frame: int) -> plt.figure:
        fig = plt.figure(figsize=size, dpi=self.dpi)
        ax = plt.gca()

        map_.plot(ax)

        ntracks = len(self.track_plotters)
        for i in range(ntracks):
            self.track_plotters[i].next_frame(ax, T[frame])

        ax.axis('off')
        fig.savefig(f'{self.results_dir}/frame{frame:0>5}.png', bbox_inches='tight')
        plt.close(fig)
        print(f'Generated frame {frame}')

    def GenerateFrames(self):
        filenames = os.listdir("data")

        with ProcessPoolExecutor() as exec:
            futures = [exec.submit(self._ReadTrack, filename) for filename in filenames if ".gpx" in filename]
            self.tracklist = [future.result() for future in futures]
            self.tracklist.sort(key=lambda trk: trk.time_reference)

        self._GenerateResultsDir()
        map_ = map.Map(self.map_settings)

        AR = map_.img.shape[0] / map_.img.shape[1]
        size = (self.imgsize, int(AR*self.imgsize))

        max_t = max(self.tracklist, key= lambda trk: trk.timestamps[-1]).timestamps[-1]
        time_steps = np.linspace(0, max_t, self.num_frames)

        colors = self.colourmap(np.linspace(0,1,12))
        extrema = self._FindExtrema()
        self.track_plotters = [trk.get_track_plotter(extrema, color=colors[trk.time_reference.month-1]) for trk in self.tracklist]

        #ax, T[frame], color=colors[month]
        [self._GenerateSingleFrame(time_steps, map_, size, frame) for frame in range(self.num_frames)]

    @classmethod
    def BuildVideo(cls, fps):
        framenames = os.listdir("result")
        framenames.sort()

        firstframe = cv2.imread(f"{cls.results_dir}/{framenames[0]}")
        size = firstframe.shape[1], firstframe.shape[0]
        out = cv2.VideoWriter('project.avi', cv2.VideoWriter_fourcc(*'DIVX'), fps, size)

        with ProcessPoolExecutor() as exec:
            images = [cv2.imread(f"{cls.results_dir}/{filename}") for filename in framenames]
            [out.write(img) for img in images]
        out.release()