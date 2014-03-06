import math
import os

import settings

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
#
def bound_pyramid_to_tile_nums(ne, sw, zmin, zmax):
    tile_nums = []
    for z in range(zmin, zmax + 1):
        tile_nums += bounding_box_to_tile_nums(ne, sw, z)
    return tile_nums

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

def download_tiles(urls, target_dir='/tmp/tiles'):
    #write urls to file
    fn = '/tmp/tile_urls.txt'
    f = open(fn, 'w')
    f.writelines(['%s\n' % u for u in urls])
    f.close()

    #prep target dir
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    #pull tiles down
    cwd = os.getcwd()
    os.chdir(target_dir)
    os.system('wget --recursive --quiet --no-host-directories --cut-dirs 2 --input-file %s' % fn)
    os.chdir(cwd)

    #cleanup
    #os.remove(fn)

def pyramid4deg(lat_deg, lon_deg, zoom_limit=15, radius=2):
    """
    Given a lat/lng, generate the urls for the pyramid of tiles
    for zoom levels 3-17

    Radius is how many tiles from the center at zoom-limit and above
    (by default zooms 3-15 have radius of 2.  16 has radius 4.  17 radius 8)
    """
    urls = []
    for zoom in range(3, 18):
        ctr_x, ctr_y = deg2num(lat_deg, lon_deg, zoom)
        r = radius * (2 ** (max(zoom, zoom_limit) - zoom_limit))
        for x in range(ctr_x-r, ctr_x+r+1):
            for y in range(ctr_y-r, ctr_y+r+1):
                urls.append(num2url(zoom, x, y))
    return urls

def num2url(x, y, zoom):
    """
    Given a zoom, an x, and a y,
    return the url of that tile
    """
    return 'http://api.tiles.mapbox.com/v3/%s/%s/%s/%s.png' % (settings.MAP_ID, zoom, x, y)

