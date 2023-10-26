import math
from dms2dec.dms_convert import dms2dec
from image_downloading import download_image
import os
import cv2
from geopy.distance import geodesic


def calculate_bottom_right(X, Y, N):
    Y_radians = math.radians(Y)
    DEGREE_OF_LAT_IN_METERS = 111139

    new_latitude = Y - (N / DEGREE_OF_LAT_IN_METERS)

    new_longitude = X + (N / (DEGREE_OF_LAT_IN_METERS * math.cos(Y_radians)))

    return new_longitude, new_latitude


def get_coord_bounds(center_lon, center_lat, size):
    half_side = size // 2

    top_left = geodesic(meters=half_side).destination((center_lat, center_lon), 315) # 315 degrees is NW
    top_left = (top_left[0], top_left[1])

    bottom_right = geodesic(meters=half_side).destination((center_lat, center_lon), 135) # 135 degrees is SE
    bottom_right = (bottom_right[0], bottom_right[1])

    return top_left, bottom_right


def get_dd_from_poi(filename):
    coords_of_interest = []

    with open(filename, 'r') as f:
        lines = f.readlines()

        for line in lines:
            line = line.strip().split(',')
            lon, lat = line[0].strip(), line[1].strip()

            if 'N' in lon + lat:
                lon = dms2dec(lon)
                lat = dms2dec(lat)
            else:
                lon = float(lon)
                lat = float(lat)

            coords_of_interest.append((lon, lat))

    return coords_of_interest


def download_image_from_poi(poi, image_id, batch_dir, prefs,
                            zoom, size_of_tile_in_meters,
                            get_adjacent_tiles=False):
    print("Downloading image {image_id}...".format(image_id=image_id))
    lat1, lon1 = poi

    lat1 = float(lat1)
    lon1 = float(lon1)

    top_left, bottom_right = get_coord_bounds(lon1, lat1, size_of_tile_in_meters)

    lat1, lon1 = top_left
    lat2, lon2 = bottom_right

    if prefs['tile_format'].lower() == 'png':
        channels = 4
    else:
        channels = 3

    img = download_image(lat1, lon1, lat2, lon2, zoom, prefs['url'],
                         prefs['headers'], prefs['tile_size'], channels)

    name = f'img_{image_id}.png'
    cv2.imwrite(os.path.join(batch_dir, name), img)
    print(f'Saved as {name}')
