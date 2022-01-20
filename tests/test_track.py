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
        
        # Time checks
        self.assertEqual(len(t.time), 2722)
        self.assertAlmostEqual(t.time[0], 0)
        self.assertAlmostEqual(t.time[-1], 10503, delta=0.5)

        # Location checks
        self.assertEqual(len(t.time), 2722)
        self.assertAlmostEqual(t.locations[0, 0], t.locations[-1, 0], delta=1)
        self.assertAlmostEqual(t.locations[0, 1], t.locations[-1, 1], delta=1)
        self.assertAlmostEqual(t.locations[0, 2], t.locations[-1, 2], delta=15)


if __name__ == "__main__":
    unittest.main()
