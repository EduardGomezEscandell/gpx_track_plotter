import matplotlib.pyplot as plt

from src.defines import LAT, LON, ELE

class TrackPlotter():
    def __init__(self, track, span = None, **line_properties):
        self.track = track
        self.span = span
        self.end_time = self.track.timestamps[-1]
        self.line_properties = line_properties
        self.latitudes = [0]
        self.longitudes = [0]
        self.step = 0
        self.progress = 0
        self.finished = False
    
    @classmethod
    def __linear_interpolation(cls, x0, x1, y0, y1, x):
        return y0 + (x - x0)/(x1 - x0) * (y1 - y0)
    
    def next_frame(self, ax: plt.axes, time: float):
        if self.finished or time > self.end_time:
            self.finished = True
            self.longitudes = self.track.locations[:, LON]
            self.latitudes = self.track.locations[:, LAT]
        else:
            self.longitudes.pop()
            self.latitudes.pop()

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
        
        line = ax.plot(self.longitudes, self.latitudes, **self.line_properties)

        if self.span is not None:
            ax.set_xlim(self.span["min_lon"], self.span["max_lon"])
            ax.set_ylim(self.span["min_lat"], self.span["max_lat"])

        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')

        return line
    
    def location(self, ax: plt.axes, time:float = -1) -> None:
        if not self.finished:
            ax.plot(self.longitudes[-1], self.latitudes[-1], 'o', **self.line_properties)
    
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
