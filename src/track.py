import numpy as np
from xml.etree import ElementTree


class Track:
    def __init__(self, **kwargs: dict) -> None:
        self.name: str = None
        self._data: np.ndarray = None

        self._parse_kwargs(**kwargs)
       
    def _parse_kwargs(self, **kwargs: dict) -> None:
        for (key, value) in kwargs.items():
            if not hasattr(self, key):
                raise KeyError(f"Unrecognized key: {key}")
            setattr(self, key, value)

    def load_gpx(self, filepath: str):
        data = ElementTree.parse(filepath)
