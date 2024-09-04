
import matplotlib.pyplot as plt
import numpy as np

from src.defines import LAT, LON

class Map:
    def __init__(self, parameters) -> None:
        self.img = plt.imread(parameters["path"])

        loc1 = self.__get_location_from_json(parameters["keypoints"][0])
        px1 = np.array(parameters["keypoints"][0]["pixel"], dtype = np.float32)

        loc2 = self.__get_location_from_json(parameters["keypoints"][1])
        px2 = np.array(parameters["keypoints"][1]["pixel"], dtype = np.float32)

        # Bootom left corner
        px_00 = np.array([self.img.shape[0], 0], dtype=np.float32)
        loc_00 = self.__linear_interpolation(px1, px2, loc1, loc2, px_00)

        # Upper rigth corner
        px_nn = np.array([0, self.img.shape[1]], dtype=np.float32)
        loc_nn = self.__linear_interpolation(px1, px2, loc1, loc2, px_nn)

        # Extent
        self.extent = [loc_00[LON], loc_nn[LON], loc_00[LAT], loc_nn[LAT]]
    
    @classmethod
    def __get_location_from_json(cls, json_obj: dict) -> np.array:
        P = np.zeros((2,), dtype=np.float32)
        P[LAT] = json_obj["lat"]
        P[LON] = json_obj["lon"]
        return P

    def plot(self, ax: plt.Axes):
        im = ax.imshow(self.img, extent=self.extent, aspect='auto')
        return im
    
    def plot_raw(self, ax: plt.Axes):
        im = ax.imshow(self.img)
        return im

    @classmethod
    def __linear_interpolation(cls, x0:float, x1: float, y0, y1, x:float):
        return y0 + (x - x0)/(x1 - x0) * (y1 - y0)