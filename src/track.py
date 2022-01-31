import matplotlib.pyplot as plt
import numpy as np
import re

from xml.etree import ElementTree
from dateutil import parser

class _PointData:
    def __init__(self, xml_node) -> None:
        self.latitude = float(xml_node.attrib["lat"])
        self.longitude = float(xml_node.attrib["lon"])
        self.elevation = float(xml_node.find("ele").text)
        self.time = parser.parse(xml_node.find("time").text)
    
    def __lt__(self, other):
        return self.time < other.time
    
    def __str__(self):
        return f"{self.time} @ [{self.latitude}, {self.longitude}, {self.elevation}]"

class Track:

    __LAT = 0
    __LON = 1
    __ELE = 2

    def __init__(self, **kwargs: dict) -> None:
        self.name: str = None
        self.time_reference: float = None
        self.reference_basis: float = None
        
        self.locations: np.ndarray = None
        self.timestamps: np.ndarray = None

        self.x_range: list = None
        self.y_range:list = None
        
        self._parse_kwargs(**kwargs)
       
    def _parse_kwargs(self, **kwargs: dict) -> None:
        for (key, value) in kwargs.items():
            if not hasattr(self, key):
                raise KeyError(f"Unrecognized key: {key}")
            setattr(self, key, value)

    def load_gpx(self, filepath: str):
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()

        # Removing namespaces
        text = re.sub('xmlns="[^"]*"', '', text)

        root = ElementTree.fromstring(text)

        if self.name is None:
            self.name = root.find("metadata/name").text

        point_data_list = []

        for point in root.find("trk/trkseg").findall("trkpt"):
            point_data_list.append(_PointData(point))
        
        point_data_list.sort()
        n = len(point_data_list)

        self.locations = np.empty(shape=(n,3), dtype=np.float32)
        self.time = np.empty(shape=(n,), dtype=np.float32)

        if self.time_reference is None:
            self.time_reference = point_data_list[0].time

        for i in range(n):
            self.locations[i, self.__LAT] = point_data_list[i].latitude
            self.locations[i, self.__LON] = point_data_list[i].longitude
            self.locations[i, self.__ELE] = point_data_list[i].elevation

            dt = point_data_list[i].time - self.time_reference
            self.time[i] = dt.total_seconds()

    
    def plot_track(self, fig: plt.figure, ax: plt.axes) -> None:
        line = ax.plot(self.locations[:, self.__LON], self.locations[:, self.__LAT], label=self.name)

        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')

        return line

    def plot_track_until(self, fig: plt.figure, ax: plt.axes, until: float) -> None:
        
        
        line = ax.plot(self.locations[:, self.__LON], self.locations[:, self.__LAT], label=self.name)

        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')

        return line
    
    def plot_profile(self, ax: plt.axes) -> None:
        p = ax.plot(self.time / 3600, self.locations[:,self.__ELE])
        ax.set_xlabel('Time [hours]')
        ax.set_ylabel('Elevation [m]')
        ax.plot(0,0,'-')
        return p