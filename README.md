# GPX track plotter
Draws and animates GPX tracks onto a map!

Here is an example with a few publicly-shared tracks from Koomot:

https://user-images.githubusercontent.com/47142856/152042667-e08d864d-d58d-4006-9c8c-45551afd3d7a.mp4

# Using a map
In order to put a map in the background, you'll need to provide an image file with the map and some metadata in json format:
```jsonc
{
    # The path to the image file
    "path" : "sample/map/barcelona.tiff",
    
    # A pair of locations in the map. This is needed to map from pixels to latitude/longitude
    "keypoints" :
    [
        {
            # The name is ignored, it's allowed here for documentation purposes
            "name" : "Tibidabo",

            # The pixel coordinates of the point [row, column]
            "pixel" : [1632, 1739],

            # Latitude and longitude of the point in the real world
            "lat" : 41.423,
            "lon" : 2.119            
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

# Sample data credits
The sample routes are publicly shared from [Komoot](https://www.komoot.com).
The sample map is provided by the [Cartographic and Geological Institute of Catalonia](http://srv.icgc.cat/vissir3)

