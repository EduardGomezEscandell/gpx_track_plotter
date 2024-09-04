"""
This file can help with creating the metadata file.

It plots the map and you can hover any point to see its pixel coordinates.
"""

import json
import matplotlib.pyplot as plt

from src.map import Map

with open("sample/map/barcelona.json", "r", encoding="utf-8") as f:
    params = json.loads(f.read())

fig, [axL, axR] = plt.subplots(nrows=1, ncols=2)
m = Map(params)

axL.set_title("Pixel coordinates")
axR.set_title("Lon/lat coordinates")
m.plot_raw(axL)
m.plot(axR)

for p in params["keypoints"]:
    px = p["pixel"]
    l = axL.plot(px[1], px[0], "x")
    axL.text(px[1], px[0], p['name'], fontsize=8)

    axR.plot(p["lon"], p["lat"], "x", c=l[0].get_color())
    axR.text(p["lon"], p["lat"], p['name'], fontsize=8)

plt.show()
