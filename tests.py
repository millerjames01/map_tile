import unittest
import utils

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

        # utils.bounding_box(point, half-side) gives the proper coordinates

    def test_bounding_box_to_tiles(self):
        return True
        # utils.bouding_box_to_tiles(nw, se, zoom):

    def test_bounding_box_to_tile_nums(self):
        return True
        # utils.bounding_box_to_tile_nums(nw, se, zoom)

    def test_bound_pyramid_to_tile_nums(self):
        return True
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
