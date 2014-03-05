import unittest
import utils

class UtilTest(unittest.TestCase):

    def test_bounding_box_from_latlng(self):
        # utils.bounding_box(point, half-side) gives the proper coordinates

    def test_bounding_box_to_tiles(self):
        # utils.bouding_box_to_tiles(nw, se, zoom):

    def test_bounding_box_to_tile_nums(self):
        # utils.bounding_box_to_tile_nums(nw, se, zoom)

    def test_bound_pyramid_to_tile_nums(self):
        # utils.bound_pyramid_to_tile_nums(nw, se, zmin, zmax)

"""
    def test_deg2num(self):
        x, y = utils.deg2num(30, -40, 14)
        self.assertEqual((x, y), (6371, 6759))

    def test_num2url(self):
        url = utils.num2url(5, 6371, 6759)
        self.assertEqual(
          url,
          'http://api.tiles.mapbox.com/v3/silviaterra.map-wgl5nho7/5/6371/6759.png'
        )

    def test_pyramid4deg(self):
        urls = utils.pyramid4deg(38, -85)
        expected_first_30 = ['http://api.tiles.mapbox.com/v3/silviaterra.map-wgl5nho7/3/0/1.png',
 'http://api.tiles.mapbox.com/v3/silviaterra.map-wgl5nho7/3/0/2.png',
 'http://api.tiles.mapbox.com/v3/silviaterra.map-wgl5nho7/3/0/3.png',
 'http://api.tiles.mapbox.com/v3/silviaterra.map-wgl5nho7/3/0/4.png',
 'http://api.tiles.mapbox.com/v3/silviaterra.map-wgl5nho7/3/0/5.png',
 'http://api.tiles.mapbox.com/v3/silviaterra.map-wgl5nho7/3/1/1.png',
 'http://api.tiles.mapbox.com/v3/silviaterra.map-wgl5nho7/3/1/2.png',
 'http://api.tiles.mapbox.com/v3/silviaterra.map-wgl5nho7/3/1/3.png',
 'http://api.tiles.mapbox.com/v3/silviaterra.map-wgl5nho7/3/1/4.png',
 'http://api.tiles.mapbox.com/v3/silviaterra.map-wgl5nho7/3/1/5.png',
 'http://api.tiles.mapbox.com/v3/silviaterra.map-wgl5nho7/3/2/1.png',
 'http://api.tiles.mapbox.com/v3/silviaterra.map-wgl5nho7/3/2/2.png',
 'http://api.tiles.mapbox.com/v3/silviaterra.map-wgl5nho7/3/2/3.png',
 'http://api.tiles.mapbox.com/v3/silviaterra.map-wgl5nho7/3/2/4.png',
 'http://api.tiles.mapbox.com/v3/silviaterra.map-wgl5nho7/3/2/5.png',
 'http://api.tiles.mapbox.com/v3/silviaterra.map-wgl5nho7/3/3/1.png',
 'http://api.tiles.mapbox.com/v3/silviaterra.map-wgl5nho7/3/3/2.png',
 'http://api.tiles.mapbox.com/v3/silviaterra.map-wgl5nho7/3/3/3.png',
 'http://api.tiles.mapbox.com/v3/silviaterra.map-wgl5nho7/3/3/4.png',
 'http://api.tiles.mapbox.com/v3/silviaterra.map-wgl5nho7/3/3/5.png',
 'http://api.tiles.mapbox.com/v3/silviaterra.map-wgl5nho7/3/4/1.png',
 'http://api.tiles.mapbox.com/v3/silviaterra.map-wgl5nho7/3/4/2.png',
 'http://api.tiles.mapbox.com/v3/silviaterra.map-wgl5nho7/3/4/3.png',
 'http://api.tiles.mapbox.com/v3/silviaterra.map-wgl5nho7/3/4/4.png',
 'http://api.tiles.mapbox.com/v3/silviaterra.map-wgl5nho7/3/4/5.png',
 'http://api.tiles.mapbox.com/v3/silviaterra.map-wgl5nho7/4/2/4.png',
 'http://api.tiles.mapbox.com/v3/silviaterra.map-wgl5nho7/4/2/5.png',
 'http://api.tiles.mapbox.com/v3/silviaterra.map-wgl5nho7/4/2/6.png',
 'http://api.tiles.mapbox.com/v3/silviaterra.map-wgl5nho7/4/2/7.png',
 'http://api.tiles.mapbox.com/v3/silviaterra.map-wgl5nho7/4/2/8.png']
        self.assertEquals(urls[:30], expected_first_30)
"""

if __name__ == '__main__':
    unittest.main()
