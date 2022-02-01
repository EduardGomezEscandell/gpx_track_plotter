import json
import matplotlib.pylab as plab

from src.animation_builder import AnimationBuilder

num_frames = 240
fps = 30
imgsize = 8
dpi = 200
colourmap = plab.cm.gist_rainbow

with open("data/map/mapdata.json", "r", encoding="utf-8") as f:
    map_settings = json.load(f)["vissir3_barcelona"]

AnimationBuilder.set_data_dir("sample")
AnimationBuilder.set_results_dir("results_sample")
b = AnimationBuilder(num_frames, imgsize, dpi, colourmap, map_settings)
b.GenerateFrames()
b.BuildVideo(fps)
