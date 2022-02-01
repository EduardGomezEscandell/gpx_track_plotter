import matplotlib.pyplot as plt

from src.defines import LAT, LON, ELE

class TrackPlotter():
    def __init__(self, track, span = None, **line_properties):
        self.step = 0
        self.progress = 0
        self.track = track
        self.end_time = self.track.timestamps[-1]
        self.line_properties = line_properties
        self.latitudes = []
        self.longitudes = []
        self.span = span
    
    @classmethod
    def __linear_interpolation(cls, x0, x1, y0, y1, x):
        return y0 + (x - x0)/(x1 - x0) * (y1 - y0)
    
    def next_frame(self, ax: plt.axes, time: float):
        full_line = time > self.end_time

        if full_line:
            self.longitudes = self.track.locations[:, LON]
            self.latitudes = self.track.locations[:, LAT]
        else:
            end = self.track.timestamps.searchsorted(time)
            loc_0 = self.track.locations[end - 1, :]
            loc_1 = self.track.locations[end, :]
            t_0 = self.track.timestamps[end - 1]
            t_1 = self.track.timestamps[end]
            last_point = self.__linear_interpolation(t_0, t_1, loc_0, loc_1, time)

            if end > self.progress:
                self.longitudes.extend(self.track.locations[self.progress:end, LON])
                self.latitudes.extend(self.track.locations[self.progress:end, LAT])
                self.progress = end

            self.longitudes.append(last_point[LON])
            self.latitudes.append(last_point[LAT])
        
        line = ax.plot(self.longitudes, self.latitudes, label=self.track.name, **self.line_properties)

        if self.span is not None:
            ax.set_xlim(self.span["min_lon"], self.span["max_lon"])
            ax.set_ylim(self.span["min_lat"], self.span["max_lat"])

        if not full_line:
            ax.plot(last_point[LON], last_point[LAT], 'o', color=line[-1].get_color(), label=None)
            self.longitudes.pop()
            self.latitudes.pop()

        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')

        return line
    
    def plot_full_profile(self, ax: plt.axes) -> None:
        p = ax.plot(self.track.timestamps / 3600, self.track.locations[:, ELE])
        ax.set_xlabel('Time [hours]')
        ax.set_ylabel('Elevation [m]')
        ax.plot(0,0,'-')
        return p
    
    def plot_full(self, ax: plt.axes) -> None:
        line = ax.plot(self.track.locations[:, LON], self.track.locations[:, LAT], 'r', label=self.name)

        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')

        return line
