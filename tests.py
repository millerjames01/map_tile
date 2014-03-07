import unittest
import utils
import settings
import sqlite3
import os

class UtilTest(unittest.TestCase):

    def setUp(self):
      self.point = (41.312604, -72.929916)

      # Verified using (WA says the diagonal distance is .1415 km, or sqrt(100m^2 + 100m^2))
      # https://www.wolframalpha.com/input/?i=++++++distance+from+%2841.312604%2C+-72.929916%29+to+%2841.31350332160592%2C+-72.92871869079472%29&a=*C.distance-_*GeoQueryType-
      self.northeast100 = (41.31350332160592, -72.92871869079472)

      # https://www.wolframalpha.com/input/?i=++++++distance+from+%2841.312604%2C+-72.929916%29+to+%2841.31170467839408%2C+-72.93111330920529%29&a=*C.distance-_*GeoQueryType-
      self.southwest100 = (41.31170467839408, -72.93111330920529)

    def test_bounding_box_from_latlng_when_padding_is_zero(self):
        ret = utils.bounding_box_from_latlng( self.point[0], self.point[1], 0 )
        self.assertEqual(ret[0], self.point)
        self.assertEqual(ret[1], self.point)

    def test_bounding_box_from_latlng(self):
        ret = utils.bounding_box_from_latlng( self.point[0], self.point[1], 100 )
        self.assertEqual(ret[0], self.northeast100)
        self.assertEqual(ret[1], self.southwest100)

    def test_bounding_box_to_tiles_at_zoom_17(self):
        tile_nums = utils.bounding_box_to_tile_nums( self.northeast100, self.southwest100, 17)

        # Details on verifying this test:
        # http://pastebin.com/C2kV7Dha

        # nw
        self.assertEqual( len(tile_nums), 4)

        # NW corner
        self.assertEqual( tile_nums[0], (38982, 48990, 17))

        # NE corner
        self.assertEqual( tile_nums[1], (38982, 48991, 17))

        # SW corner
        self.assertEqual( tile_nums[2], (38983, 48990, 17))

        # se corner
        self.assertEqual( tile_nums[3], (38983, 48991, 17))

    def test_bound_pyramid_to_tile_nums(self):
        tile_nums = utils.bound_pyramid_to_tile_nums( self.northeast100, self.southwest100, 3, 17)
        self.assertEqual(tile_nums,
            [(2, 2, 3),
            (4, 5, 4),
            (9, 11, 5),
            (19, 23, 6),
            (38, 47, 7),
            (76, 95, 8),
            (152, 191, 9),
            (304, 382, 10),
            (609, 765, 11),
            (1218, 1530, 12),
            (2436, 3061, 13),
            (4872, 6123, 14),
            (9745, 12247, 15),
            (19491, 24495, 16),
            (38982, 48990, 17),
            (38982, 48991, 17),
            (38983, 48990, 17),
            (38983, 48991, 17)]
            )


    def test_coord2tile(self):
        tile = utils.coord2tile(self.point, 17)
        self.assertEqual(tile, (38983, 48991, 17))
        # http://api.tiles.mapbox.com/v3/examples.map-9ijuk24y/17/38983/48991.png

        tile = utils.coord2tile(self.point, 16)
        self.assertEqual(tile, (19491, 24495, 16))
        # http://api.tiles.mapbox.com/v3/examples.map-9ijuk24y/16/19491/24495.png

    def test_deg2num(self):
        x, y, z = utils.deg2num(30, -40, 14)
        self.assertEqual((x, y, z), (6371, 6759, 14))

    def test_num2url(self):
        url = utils.num2url(6371, 6759, 5)
        self.assertEqual(
          url,
          'http://api.tiles.mapbox.com/v3/%s/5/6371/6759.png' % settings.MAP_ID
        )

    def test_tile_nums_to_mbtiles(self):
        tile_nums = [(2, 2, 3),
            (4, 5, 4),
            (9, 11, 5)]

        # TODO(syu): replace with random temp file naem
        fn = "test.mbtiles"

        utils.tile_nums_to_mbtiles(tile_nums, fn)

        conn = sqlite3.connect(fn)
        cursor = conn.cursor()
        for tile_num in tile_nums:
            cursor.execute("SELECT * from tiles WHERE tile_column = %d AND tile_row = %d AND zoom_level = %d" % tile_num)
            tile_data = cursor.fetchone()[3]

            on_disk = open("test/%d_%d_%d.png" % tile_num, 'rb').read()

            self.assertEquals(len(tile_data), len(on_disk))
            self.assertEquals(str(tile_data), str(on_disk))

        cursor.close()
        conn.close()
        os.remove(fn)

if __name__ == '__main__':
    unittest.main()
