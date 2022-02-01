"""
This file can help with creating the metadata file.

It plots the map and you can hover any point to see its pixel coordinates.
"""

import json
import matplotlib.pyplot as plt

from src.map import Map

fig = plt.figure()
ax = plt.gca()
with open("data/map/vissir.json", "r", encoding="utf-8") as f:
    params = json.loads(f.read())

m = Map(params["vissir3_zoom"])
m.plot_raw(ax)
plt.show()
