import unittest
import utils
import settings
import sqlite3
import os
import urllib
import shutil

class UtilTest(unittest.TestCase):

    def setUp(self):
        self.point = (41.312604, -72.929916)

        # Verified using (WA says the diagonal distance is .1415 km, or sqrt(100m^2 + 100m^2))
        # https://www.wolframalpha.com/input/?i=++++++distance+from+%2841.312604%2C+-72.929916%29+to+%2841.31350332160592%2C+-72.92871869079472%29&a=*C.distance-_*GeoQueryType-
        self.northeast100 = (41.31350332160592, -72.92871869079472)

        # https://www.wolframalpha.com/input/?i=++++++distance+from+%2841.312604%2C+-72.929916%29+to+%2841.31170467839408%2C+-72.93111330920529%29&a=*C.distance-_*GeoQueryType-
        self.southwest100 = (41.31170467839408, -72.93111330920529)

        def prepare_database_images(tile_numbers):
            base_url = "http://api.tiles.mapbox.com/v3/examples.map-9ijuk24y/%d/%d/%d.png"

            if os.path.exists('test'):
                shutil.rmtree('test')
            os.mkdir('test')

            def download_image(tn):
                urllib.urlretrieve(base_url % (tn[2], tn[0], tn[1]), "test/%d_%d_%d.png" % tn )
            for tn in tile_numbers:
                download_image(tn)
        self.prepare_database_images = prepare_database_images

    def test_wkt_to_uniq_tile_nums_excludes_duplicates(self):
        wkt_string = """
             MULTIPOLYGON (((-72.928795 41.307331,
             -72.922573 41.310361,
             -72.918948 41.319578,
             -72.923261 41.320223,
             -72.92575  41.316274,
             -72.932102 41.312986,
             -72.933625 41.308892,
             -72.928795 41.307331)),

           ((-72.963514   41.311312,
             -72.95845    41.310861,
             -72.959051   41.314342,
             -72.963342   41.314471,
             -72.963514   41.311312))
             )
           """
        tns = utils.wkt_to_uniq_tile_nums(wkt_string, 3, 15)

        # Make sure no duplicates are included (levels 3 through 10)
        def filter_by_zoom_level(z):
            return [tn for tn in tns if tn[2] == z]
        self.assertEquals(len(filter_by_zoom_level(3)), 1)
        self.assertEquals(len(filter_by_zoom_level(4)), 1)
        self.assertEquals(len(filter_by_zoom_level(5)), 1)
        self.assertEquals(len(filter_by_zoom_level(6)), 1)
        self.assertEquals(len(filter_by_zoom_level(7)), 1)
        self.assertEquals(len(filter_by_zoom_level(8)), 1)
        self.assertEquals(len(filter_by_zoom_level(9)), 1)
        self.assertEquals(len(filter_by_zoom_level(10)), 1)

        # Make sure yale bowl is included at zoom level 12 and beyond:
        self.assertEquals(len(filter_by_zoom_level(12)), 3)
        self.assertEquals(len(filter_by_zoom_level(13)), 3)
        self.assertEquals(len(filter_by_zoom_level(14)), 5)
        self.assertEquals(len(filter_by_zoom_level(15)), 8)

    def test_wkt_to_uniq_tile_nums(self):
        wkt_string = """
           POLYGON ((-72.928795 41.307331,
           -72.922573 41.310361,
           -72.918948 41.319578,
           -72.923261 41.320223,
           -72.92575  41.316274,
           -72.932102 41.312986,
           -72.933625 41.308892,
           -72.928795 41.307331))
           """

        tns = utils.wkt_to_uniq_tile_nums(wkt_string, 3, 15)

        # http://api.tiles.mapbox.com/v3/examples.map-9ijuk24y/3/2/2.png
        self.assertEquals(tns[0], (2, 2, 3))

        # http://api.tiles.mapbox.com/v3/examples.map-9ijuk24y/4/4/5.png
        self.assertEquals(tns[1], (4, 5, 4))

        # http://api.tiles.mapbox.com/v3/examples.map-9ijuk24y/5/9/11.png
        self.assertEquals(tns[2], (9, 11, 5))

        # http://api.tiles.mapbox.com/v3/examples.map-9ijuk24y/5/9/11.png
        self.assertEquals(tns[3], (19, 23, 6))

        # http://api.tiles.mapbox.com/v3/examples.map-9ijuk24y/5/9/11.png
        self.assertEquals(tns[4], (38, 47, 7))

        # http://api.tiles.mapbox.com/v3/examples.map-9ijuk24y/5/9/11.png
        self.assertEqual(tns[5], (76, 95, 8))
        self.assertEqual(tns[8], (609, 765, 11))

        self.assertEqual(tns[9:11], [
          (1218, 1530, 12),
          (1218, 1531, 12)])

        self.assertEqual(tns[11:13], [
            (2436, 3061, 13),
            (2436, 3062, 13)
            ])

        self.assertEqual(tns[13:17], [
             (4872, 6123, 14),
             (4872, 6124, 14),
             (4873, 6123, 14),
             (4873, 6124, 14)
            ])

        self.assertEqual(tns[17:23], [
             (9745, 12246, 15),
             (9745, 12247, 15),
             (9745, 12248, 15),
             (9746, 12246, 15),
             (9746, 12247, 15),
             (9746, 12248, 15)
            ])

    def test_polygon_wkt_to_bounding_boxes(self):
        wkt_polygon_string = """
                             POLYGON ((-80.190262 25.774252,
                             -66.118292 18.466465,
                             -64.75737 32.321384,
                             -80.190262 25.774252))
                             """
        bounding_boxes = utils.wkt_to_bounding_boxes(wkt_polygon_string)
        self.assertEqual(len(bounding_boxes), 1)

        bb = bounding_boxes[0]
        self.assertEqual(len(bb), 2)
        ne, sw = bb
        self.assertEqual(ne[0], 32.321384)
        self.assertEqual(ne[1], -64.75737)

        self.assertEqual(sw[0], 18.466465)
        self.assertEqual(sw[1], -80.190262)

    def test_multipolygon_wkt_to_bounding_boxes(self):
        wkt_multipolygon_string = """
                             MULTIPOLYGON (((-80.190262 25.774252,
                             -66.118292 18.466465,
                             -64.75737 32.321384,
                             -80.190262 25.774252)),
                             ((31.5 32,
                               30 33.5,
                               25 33,
                               17 17,
                               31.5 32)))
                             """

        bounding_boxes = utils.wkt_to_bounding_boxes(wkt_multipolygon_string)
        self.assertEqual(len(bounding_boxes), 2)

        # First bounding box, around the bermuda triangle
        bb = bounding_boxes[0]
        self.assertEqual(len(bb), 2)
        ne, sw = bb
        self.assertEqual(ne[0], 32.321384)
        self.assertEqual(ne[1], -64.75737)
        self.assertEqual(sw[0], 18.466465)
        self.assertEqual(sw[1], -80.190262)

        # Second bounding box, around the spiky quadirlateral
        bb = bounding_boxes[1]
        self.assertEqual(len(bb), 2)
        ne, sw = bb
        self.assertEqual(ne[0], 33.5)
        self.assertEqual(ne[1], 31.5)
        self.assertEqual(sw[0], 17)
        self.assertEqual(sw[1], 17)

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

    def test_wkt_to_mbtiles(self):
        in_fn = "polygon.wkt"
        tile_nums = [   (4, 5, 4),
                        (9, 11, 5),
                        (19, 23, 6),
                        (38, 47, 7),
                        (76, 95, 8),
                        (152, 191, 9),
                        (304, 382, 10),
                        (608, 765, 11),
                        (609, 765, 11),
                        (1217, 1530, 12),
                        (1218, 1530, 12),
                        (1218, 1531, 12),
                        (2435, 3061, 13),
                        (2436, 3061, 13),
                        (2436, 3062, 13),
                        (4871, 6123, 14),
                        (4872, 6123, 14),
                        (4872, 6124, 14),
                        (4873, 6123, 14),
                        (4873, 6124, 14),
                        (9742, 12247, 15),
                        (9743, 12247, 15),
                        (9745, 12246, 15),
                        (9745, 12247, 15),
                        (9745, 12248, 15),
                        (9746, 12246, 15),
                        (9746, 12247, 15),
                        (9746, 12248, 15) ]
        self.prepare_database_images(tile_nums)
        out_fn = "test_out.mbtiles"
        utils.wkt_to_mbtiles(in_fn, out_fn, 3, 15)

        conn = sqlite3.connect(out_fn)
        cursor = conn.cursor()
        for tile_num in tile_nums:
            cursor.execute("SELECT * from tiles WHERE tile_column = %d AND tile_row = %d AND zoom_level = %d" % tile_num)
            tile_data = cursor.fetchone()[3]
            on_disk = open("test/%d_%d_%d.png" % tile_num, 'rb').read()
        cursor.close()
        conn.close()
        os.remove(out_fn)

    def test_tile_nums_to_mbtiles(self):
        tile_nums = [(2, 2, 3),
            (4, 5, 4),
            (9, 11, 5)]
        self.prepare_database_images(tile_nums)
        # TODO(syu): replace with random temp file naem
        fn = "test.mbtiles"

        utils.tile_nums_to_mbtiles(tile_nums, fn)

        conn = sqlite3.connect(fn)
        cursor = conn.cursor()
        for tile_num in tile_nums:
            cursor.execute("SELECT * from tiles WHERE tile_column = %d AND tile_row = %d AND zoom_level = %d" % tile_num)
            tile_data = cursor.fetchone()[3]

            on_disk = open("test/%d_%d_%d.png" % tile_num, 'rb').read()

            self.assertEqual(len(tile_data), len(on_disk))
            self.assertEqual(str(tile_data), str(on_disk))

        cursor.close()
        conn.close()
        os.remove(fn)

if __name__ == '__main__':
    unittest.main()
