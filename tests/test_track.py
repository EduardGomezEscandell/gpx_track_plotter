import unittest
from test_utils import WorkFolderScope
from src import track

class TrackTests(unittest.TestCase):
    def test_input_parsing(self):
        t = track.Track(name = "Test")

        self.assertEqual(t.name, "Test")
    
    def test_loading(self):
        t = track.Track()

        with WorkFolderScope("../data", __file__):
            filename = "../data/2021-12-30_618996228_Creu d'Olorda.gpx"
            t.load_gpx(filename)
        
        self.assertEqual(t.name, "Creu d'Olorda")



if __name__ == "__main__":
    unittest.main()
