## To run:

```
% python
>>> import utils
>>> utils.wkt_to_mbtiles("polygon.wkt", "out.mbtiles", 3, 15)
[(2, 2, 3), (4, 5, 4), (9, 11, 5), (19, 23, 6), (38, 47, 7), (76, 95, 8), (152, 191, 9), (304, 382, 10), (608, 765, 11), (609, 765, 11), (1217, 1530, 12), (1218, 1530, 12), (1218, 1531, 12), (2435, 3061, 13), (2436, 3061, 13), (2436, 3062, 13), (4871, 6123, 14), (4872, 6123, 14), (4872, 6124, 14), (4873, 6123, 14), (4873, 6124, 14), (9742, 12247, 15), (9743, 12247, 15), (9745, 12246, 15), (9745, 12247, 15), (9745, 12248, 15), (9746, 12246, 15), (9746, 12247, 15), (9746, 12248, 15)]

% du -sh out.mbtiles
684K    out.mbtiles
```

The included `sample.mbtiles` is generated from `polygon.wkt` at zoom levels 3 to 17, with the following command:
```
utils.wkt_to_mbtiles('polygon.wkt', 'sample.mbtiles', 3, 17)
```

## Tests:
The tests writes files (temporary image files) to the `test` directory, which is NOT checked into the repo.

To run tests:
```
% python tests.py
```


## About polygon.wkt
The included `polygon.wkt` file defines two polygons, one of Yale University campus, one of the Yale Bowl quadrangle. Notes included below:
Polygon.wkt defines two polygons, one of Yale University campus, one of the Yale Bowl quadrangle.
```
# lat	lng	description

Yale campus
41.307331	-72.928795	chapel & college
41.310361	-72.922573	grove & church/whitney
41.319578	-72.918948	whitney and edwards
41.320223	-72.923261	prospect and edwards
41.316274	-72.92575	Mansfield and Sachem (corner of the whale)
41.312986	-72.932102	western corner of stiles / the gym
41.308892	-72.933625	Chapel and Park
41.307331	-72.928795	chapel & college (closing the polygon)

Yale bowl
41.311312	-72.963514	sw corner
41.310861	-72.95845	se corner
41.314342	-72.959051	ne
41.314471	-72.963342	nw
```
