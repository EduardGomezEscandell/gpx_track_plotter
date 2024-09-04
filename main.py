import json
import matplotlib.pylab as plab

from src.animation_builder import AnimationBuilder

def main(workdir: str, mapfile: str, outdir: str, num_frames: int, fps: int, imgsize: int, dpi: int, colourmap: plab.Colormap):
    with open(mapfile, "r", encoding="utf-8") as f:
        map_settings = json.load(f)

    b = AnimationBuilder(workdir, outdir, num_frames, imgsize, dpi, colourmap, map_settings)
    b.GenerateFrames()
    b.BuildVideo(fps)


if __name__ == "__main__":
    main("sample", "sample/map/barcelona.json", "result",
        num_frames = 240,
        fps = 30,
        imgsize = 8,
        dpi = 200,
        colourmap = plab.cm.gist_rainbow
    )