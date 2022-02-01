# GPX track plotter
Draws and animates GPX tracks onto a map!

Here is an example with a few publicly-shared tracks from Koomot:

https://user-images.githubusercontent.com/47142856/152042667-e08d864d-d58d-4006-9c8c-45551afd3d7a.mp4

# Using a map
In order to put a map in the background, you'll need to provide an image file with the map and some metadata in json format:
```
"vissir3_barcelona": {
        "path" : "data/sample/barcelona.tiff",   <-- The path to the image file
        "keypoints" :   <-- A pair of locations in the map. This is needed to match it to the coordinates.
        [
            {
                "name" : "Tibidabo",     <--- This is ignored. It's here to make things easier.
                "pixel" : [1632, 1739],  <--- The pixel coordinates of the point [row, column]
                "lat" : 41.423,          <--- Latitude of the point in the real world
                "lon" : 2.119            <--- Longitude of the point in the real world
            },
            {
                "name" : "La Morella",
                "pixel" : [2182, 1047],
                "lat" : 41.2966,
                "lon" : 1.9155
            }
        ]
    }
```

# Sources
The sample routes are publicly shared from [Komoot](komoot.com.com).


The sample map is provided by http://www.icc.cat/vissir3/
