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
    def __init__(self, data_dir, results_dir, num_frames, imgsize, dpi, colourmap, map_settings):
        self.results_dir = results_dir
        self.data_dir = data_dir
        self.num_frames = num_frames
        self.imgsize = imgsize
        self.dpi = dpi
        self.colourmap = colourmap
        self.map_settings = map_settings

        self.tracklist = None
        self.track_plotters = None
    
    def _ReadTrack(self, filename) -> Track:
        t = Track()
        t.load_gpx(f"{self.data_dir}/{filename}")
        print(f"Read {filename}")
        return t

    def _GenerateResultsDir(self) -> None:
        try:
            shutil.rmtree(self.results_dir)
        except FileNotFoundError:
            pass

        try:
            os.mkdir(self.results_dir)
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

    def GenerateFrames(self, crop = False):
        filenames = [f for f in os.listdir(self.data_dir) if ".gpx" in f]

        with ProcessPoolExecutor(max_workers=8) as executor:
            futures = [executor.submit(self._ReadTrack, filename) for filename in filenames]

            self._GenerateResultsDir()
            map_ = Map(self.map_settings)

            aspect_ratio = map_.img.shape[0] / map_.img.shape[1]
            size = (self.imgsize, int(aspect_ratio*self.imgsize))

            self.tracklist = list(map(lambda f: f.result(), futures))
            self.tracklist.sort(key=lambda trk: trk.timestamps[-1])

            max_t = max(self.tracklist, key= lambda trk: trk.timestamps[-1]).timestamps[-1]
            time_steps = np.linspace(0, max_t, self.num_frames)

            colours = self.colourmap(np.linspace(0,1, len(self.tracklist)))
            
            extrema = None
            if crop:
                extrema = self._FindExtrema()
            
            self.track_plotters = [trk.get_track_plotter(extrema, color=col) for trk, col in zip(self.tracklist, colours)]

            futures = [executor.submit(self._GenerateSingleFrame, time_steps, map_, size, frame) for frame in range(self.num_frames)]
            map(lambda f: f.result, futures)

    def BuildVideo(self, fps):
        framenames = os.listdir(self.results_dir)
        framenames.sort()

        firstframe = cv2.imread(f"{self.results_dir}/{framenames[0]}")
        size = firstframe.shape[1], firstframe.shape[0]
        out = cv2.VideoWriter('result.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, size)

        with ProcessPoolExecutor() as executor:
            futures = [executor.submit(cv2.imread, f"{self.results_dir}/{f}") for f in framenames]
            for f in futures:
                out.write(f.result())

        out.release()