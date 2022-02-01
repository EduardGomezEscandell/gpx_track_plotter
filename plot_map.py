import json
import matplotlib.pyplot as plt

from src.map import Map

fig = plt.figure()
ax = plt.gca()
with open("data/map/vissir.json", "r") as f:
    params = json.loads(f.read())

m = Map(params["vissir3_zoom"])
m.plot(ax)
plt.show()