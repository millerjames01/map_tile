require 'pry'


def get_tile_number(lat_deg, lng_deg, zoom)
  lat_rad = lat_deg.to_f/180 * Math::PI
  n = 2.0 ** zoom
  x = ((lng_deg + 180.0) / 360.0 * n).to_i
  coef = n.to_f / ( 2.0 * Math::PI)
  y = (
    (1.0 - Math::log(
      Math::tan(lat_rad)    +    (1 / Math::cos(lat_rad))
    )) * coef
  ).to_i
  return {:x => x, :y =>y}
end

# Tile numbers to lon./lat.
def get_lat_lng_for_number(xtile, ytile, zoom)
  n = 2.0 ** zoom
  lon_deg = xtile / n * 360.0 - 180.0
  lat_rad = Math::atan(Math::sinh(Math::PI * (1 - 2 * ytile / n)))
  lat_deg = 180.0 * (lat_rad / Math::PI)
  {:lat_deg => lat_deg, :lng_deg => lon_deg}
end

alias :gtn :get_tile_number
