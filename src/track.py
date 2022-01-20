from math import sin, cos
from turtle import shape
from dateutil import parser
import numpy as np
import re
from xml.etree import ElementTree


_EARTH_RADIUS =  6.3781e6
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
    
    def location(self):
        return np.array([self.latitude, self.longitude, self.elevation])
    
    def vector_from(self, origin: np.array) -> np.array:
        dx_hat = cos(self.latitude)*cos(self.longitude) - cos(origin.latitude)*cos(origin.longitude)
        dy_hat = cos(self.latitude)*sin(self.longitude) - cos(origin.latitude)*sin(origin.longitude)
        



class Track:
    def __init__(self, **kwargs: dict) -> None:
        self.name: str = None
        self.time_reference: float = None
        self.location_reference: float = None
        
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
        re.sub('xmlns="[^"]*"', '', text)       

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

        if self.location_reference is None:
            self.location_reference = point_data_list[0].location()

        for i in range(n):
            self.locations[i, 0] = point_data_list[i].longitude
            self.locations[i, 1] = point_data_list[i].latitude
            self.locations[i, 2] = point_data_list[i].elevation
            self.locations[i,:] -= self.location_reference

            dt = point_data_list[i].time - self.time_reference
            self.time[i] = dt.total_seconds()
