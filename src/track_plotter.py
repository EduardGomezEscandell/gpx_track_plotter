import matplotlib.pyplot as plt

from src.defines import LAT, LON, ELE

class TrackPlotter():
    """
    This class is tasked with printing a track to a matplotlib figure

    It may print the full track, a profile view, the track up until a timestamp, etc.
    """

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

    def print_until_time(self, ax: plt.Axes, time: float):
        """
        Prints the track until a specified timestamp (in seconds)
        """
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

    def location(self, ax: plt.Axes) -> None:
        "Plots the location at the last print_until_time"
        if not self.finished:
            ax.plot(self.longitudes[-1], self.latitudes[-1], 'o', **self.line_properties)

    def plot_full_profile(self, ax: plt.Axes) -> None:
        "Plots a graph of elevation over time"
        plot_ = ax.plot(self.track.timestamps / 3600, self.track.locations[:, ELE])
        ax.set_xlabel('Time [hours]')
        ax.set_ylabel('Elevation [m]')
        ax.plot(0,0,'-')
        return plot_

    def plot_full(self, ax: plt.Axes) -> None:
        "Plots the track from start to end"
        line = ax.plot(
            self.track.locations[:, LON],
            self.track.locations[:, LAT],
            'r', label=self.track.name)

        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')

        return line
