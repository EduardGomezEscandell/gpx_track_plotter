import unittest
from src import track

class TrackTests(unittest.TestCase):
    def test_input_parsing(self):
        t = track.Track(name = "Test")

        self.assertEqual(t.name, "Test")
    
    def test_loading(self):
        filename = "../data/2021-12-30_618996228_Creu d'Olorda.gpx"
        t = track.Track()
        t.load_gpx(filename)



if __name__ == "__main__":
    unittest.main()
