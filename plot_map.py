"""
This file can help with creating the metadata file.

It plots the map and you can hover any point to see its pixel coordinates.
"""

import json
import matplotlib.pyplot as plt

from src.map import Map

with open("data/map/barcelona.json", "r", encoding="utf-8") as f:
    params = json.loads(f.read())

for name, map in params.items():
    fig, [axL, axR] = plt.subplots(nrows=1, ncols=2)
    m = Map(map)
    
    axL.set_title(name + " in pixel coordinates")
    axR.set_title(name + " in lon/lat coordinates")
    m.plot_raw(axL)
    m.plot(axR)

    for p in map["keypoints"]:
        px = p["pixel"]
        l = axL.plot(px[1], px[0], "x")
        axL.text(px[1], px[0], p['name'], fontsize=8)

        axR.plot(p["lon"], p["lat"], "x", c=l[0].get_color())
        axR.text(p["lon"], p["lat"], p['name'], fontsize=8)

    fig.show()

plt.show()
