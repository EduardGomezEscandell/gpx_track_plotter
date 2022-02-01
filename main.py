import matplotlib.pylab as plab
import json

from src.animation_builder import AnimationBuilder

num_frames = 420
fps = 30
imgsize = 8
dpi = 300
colourmap = plab.cm.gist_rainbow

with open("data/map/mapdata.json", "r") as f:
    map_settings = json.load(f)["vissir3_zoom"]

b = AnimationBuilder(num_frames, imgsize, dpi, colourmap, map_settings)
b.GenerateFrames()
b.BuildVideo(fps)