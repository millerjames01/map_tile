import math
import os

import settings
import sqlite3
import urllib2

from shapely.wkt import loads
import shapely.geometry
from operator import itemgetter

# For the given lat/lng point, bound it by `padding` distance (in meters) in each
# direction, and then, dump all tiles in zoom levels 3 to 17 that intersect
# the bounding box into a .mbtiles file specified by `fn`
def coord_to_mbtiles(lat, lng, padding, fn):
    ne, sw = bounding_box_from_latlng(lat, lng, padding)
    tile_nums = bound_pyramid_to_tile_nums(ne, sw, 3, 17)
    tile_nums_to_mbtiles(tile_nums, fn)

##
# @in_fn
def wkt_to_mbtiles(in_fn="polygon.wkt", out_fn="out.mbtiles", zmin=3, zmax=17):
    wkt_string = open(in_fn, "rb").read()
    uniq_tile_nums = wkt_to_uniq_tile_nums(wkt_string, zmin, zmax)
    print uniq_tile_nums
    tile_nums_to_mbtiles(uniq_tile_nums, out_fn)

def wkt_to_uniq_tile_nums(wkt_string, zmin, zmax):
    bounding_boxes = wkt_to_bounding_boxes(wkt_string)
    tile_nums = []

    for bb in bounding_boxes:
      ne, sw = bb
      tile_nums += bound_pyramid_to_tile_nums(ne, sw, zmin, zmax)

    # Unique, and sort by z x y
    uniq_tile_nums = list(set(tile_nums))
    sorted_tile_nums = sorted(uniq_tile_nums, key=itemgetter(2, 0, 1))
    return sorted_tile_nums

def wkt_to_bounding_boxes(wkt_string):
    g = loads(wkt_string)
    stands = []
    if g.geom_type == "Polygon":
      stands = [g]
    elif g.geom_type == "MultiPolygon":
      stands = g.geoms
    def bounds_tuple_to_bounding_box_coords(bounds_tuple):
        # tuple: (minx, miny, maxx, maxy)
        lng_min, lat_min, lng_max, lat_max = bounds_tuple
        return (lat_max, lng_max), (lat_min, lng_min)
    bb_coords = [bounds_tuple_to_bounding_box_coords(g.bounds) for g in stands]
    return bb_coords

def bb_coords_as_wkt(ne, sw):
  return "POLYGON ((%f %f, %f %f, %f %f, %f %f))" % (ne[1], ne[0], ne[1], sw[0], sw[1], sw[0], sw[1], ne[0])


# @param lat <Float>
# @param lng <Float>
# @param padding <Float> distance, in meters
# @return pair of lat lng coordinates, specifying the NW and SE points
#   [ (ne_lat, ne_lng), (sw_lat, sw_lng) ]
def bounding_box_from_latlng(lat, lng, padding):
    padding = float(padding)
    lat_rad = math.radians(lat)
    lng_rad = math.radians(lng)

    radius = 6371 * 1000 # Of Earth, in meters

    # Radius of the parallel at given latitude
    parallel_radius = radius * math.cos(lat_rad)

    lat_min = lat_rad - padding / radius
    lat_max = lat_rad + padding / radius
    lng_min = lng_rad - padding / parallel_radius
    lng_max = lng_rad + padding / parallel_radius

    ne = (math.degrees(lat_max), math.degrees(lng_max))
    sw = (math.degrees(lat_min), math.degrees(lng_min))

    return [ne, sw]

# @param ne <LatLng tuple> the northeast corner of the region
# @param sw <LatLng tuple> the southwest corner of the region
# @param zoom <Integer> the desired zoom level used to compute the tiles
# @return <List(xyz tuple)> list of tile number tuples at this zoom level
def bounding_box_to_tile_nums(ne, sw, zoom):
    ne_x, ne_y, zoom = coord2tile( ne, zoom)
    sw_x, sw_y, zoom = coord2tile( sw, zoom)
    xmin = min(ne_x, sw_x)
    xmax = max(ne_x, sw_x)
    ymin = min(ne_y, sw_y)
    ymax = max(ne_y, sw_y)

    tile_nums = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            xyz = (x, y, zoom)
            tile_nums.append(xyz)

    return tile_nums

# @param ne <LatLng tuple> the northeast corner of the region
# @param sw <LatLng tuple> the southwest corner of the region
# @param zmin <Integer> min desired zoom range, inclusive
# @param zmax <Integer> max desired zoom range, inclusive
# @return <List(xyz tuple)> list of tile number tuples at this zoom level

def bound_pyramid_to_tile_nums(ne, sw, zmin, zmax):
    tile_nums = []
    for z in range(zmin, zmax + 1):
        tile_nums += bounding_box_to_tile_nums(ne, sw, z)
    return tile_nums

# @param tile_nums <List(xyz tuple)> list of tile number tuples
# @param fn <String> file name for the mbtiles sqlite3 db. File will be clobbered if it already
#                    exists
def tile_nums_to_mbtiles(tile_nums, fn="out.mbtiles"):
    # Create db, clobbering if already exists
    if os.path.isfile(fn):
        os.remove(fn)
    conn = sqlite3.connect(fn)
    conn.execute(
        "CREATE TABLE tiles (zoom_level integer, tile_column integer, tile_row integer, tile_data blob)"
        )

    for tile_num in tile_nums:
        # Get tile_data, as string
        url =  num2url(*tile_num)
        tile_data = urllib2.urlopen(url).read()

        # Insert the tile numbers + blob into db
        # Note: need to convert tile data from string to binary blob
        conn.execute(
            "INSERT INTO tiles VALUES (?, ?, ?, ?)",
            [tile_num[2], tile_num[0], tile_num[1], sqlite3.Binary(tile_data)]
            )

    conn.commit()
    conn.close()

# @param coord <LatLng tuple>
# @param zoom <Integer> the desired zoom level for the tile to return
# @return <tile number tuple: (x, y, zoom)>
def coord2tile(coord, zoom):
    return deg2num(coord[0], coord[1], zoom)

def deg2num(lat_deg, lon_deg, zoom):
  """
  From http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Lon..2Flat._to_tile_numbers_2
  """
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
  return (xtile, ytile, zoom)

def num2url(x, y, zoom):
    """
    Given a zoom, an x, and a y,
    return the url of that tile
    """
    return 'http://api.tiles.mapbox.com/v3/%s/%s/%s/%s.png' % (settings.MAP_ID, zoom, x, y)

