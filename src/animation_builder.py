import shutil
import os
from concurrent.futures import ProcessPoolExecutor

import matplotlib.pyplot as plt
import numpy as np
import cv2

from src.defines import LAT, LON
from src.track import Track
from src.map import Map

class AnimationBuilder:
    results_dir = "result"
    data_dir = "data"

    def __init__(self, num_frames, imgsize, dpi, colourmap, map_settings):
        self.num_frames = num_frames
        self.imgsize = imgsize
        self.dpi = dpi
        self.colourmap = colourmap
        self.map_settings = map_settings

        self.tracklist = None
        self.track_plotters = None
    
    @classmethod
    def set_results_dir(cls, new_val) -> None:
        cls.results_dir = new_val
    
    @classmethod
    def set_data_dir(cls, new_val) -> None:
        cls.data_dir = new_val

    @classmethod
    def _ReadTrack(cls, filename) -> Track:
        t = Track()
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

        for trk in self.tracklist:
            extrema["max_lon"] = max(extrema["max_lon"], max(trk.locations[:, LON]))
            extrema["min_lon"] = min(extrema["min_lon"], min(trk.locations[:, LON]))
            extrema["max_lat"] = max(extrema["max_lat"], max(trk.locations[:, LAT]))
            extrema["min_lat"] = min(extrema["min_lat"], min(trk.locations[:, LAT]))
        return extrema

    def _GenerateSingleFrame(self, T: list, map_: Map, size: tuple, frame: int) -> plt.figure:
        fig = plt.figure(figsize=size, dpi=self.dpi)
        ax = plt.gca()

        map_.plot(ax)

        ntracks = len(self.track_plotters)
        for i in range(ntracks):
            self.track_plotters[i].print_until_time(ax, T[frame])
        for i in range(ntracks):
            self.track_plotters[i].location(ax)

        ax.axis('off')
        fig.savefig(f'{self.results_dir}/frame{frame:0>5}.png', bbox_inches='tight')
        plt.close(fig)
        print(f'Generated frame {frame}')

    def GenerateFrames(self):
        filenames = [f for f in os.listdir(self.data_dir) if ".gpx" in f]

        with ProcessPoolExecutor() as executor:
            futures = [executor.submit(self._ReadTrack, filename) for filename in filenames]
            self.tracklist = [future.result() for future in futures]
            self.tracklist.sort(key=lambda trk: trk.timestamps[-1])

        self._GenerateResultsDir()
        map_ = Map(self.map_settings)

        aspect_ratio = map_.img.shape[0] / map_.img.shape[1]
        size = (self.imgsize, int(aspect_ratio*self.imgsize))

        max_t = max(self.tracklist, key= lambda trk: trk.timestamps[-1]).timestamps[-1]
        time_steps = np.linspace(0, max_t, self.num_frames)

        colours = self.colourmap(np.linspace(0,1, len(self.tracklist)))
        extrema = self._FindExtrema()
        self.track_plotters = [trk.get_track_plotter(extrema, color=col) for trk, col in zip(self.tracklist, colours)]

        _ = [self._GenerateSingleFrame(time_steps, map_, size, frame) for frame in range(self.num_frames)]

    @classmethod
    def BuildVideo(cls, fps):
        framenames = os.listdir("result")
        framenames.sort()

        firstframe = cv2.imread(f"{cls.results_dir}/{framenames[0]}")
        size = firstframe.shape[1], firstframe.shape[0]
        out = cv2.VideoWriter('result_sample.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, size)

        with ProcessPoolExecutor() as executor:
            futures = [executor.submit(cv2.imread, f"{cls.results_dir}/{filename}") for filename in framenames]
            _ = [out.write(f.result()) for f in futures]
        out.release()