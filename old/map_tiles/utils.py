import math
import os

import settings

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

def num2url(zoom, x, y):
    """
    Given a zoom, an x, and a y,
    return the url of that tile
    """
    return 'http://api.tiles.mapbox.com/v3/%s/%s/%s/%s.png' % (settings.MAP_ID, zoom, x, y)

def deg2num(lat_deg, lon_deg, zoom):
  """
  From http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Lon..2Flat._to_tile_numbers_2
  """
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
  return (xtile, ytile)
