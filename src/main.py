import os
import json
import re
import cv2
import threading
from helper import calculate_bottom_right, get_dd_from_poi, download_image_from_poi
from datetime import datetime

from image_downloading import download_image

file_dir = os.path.dirname(__file__)
prefs_path = os.path.join(file_dir, 'preferences.json')
default_prefs = {
        'url': 'https://mt.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        'tile_size': 256,
        'tile_format': 'jpg',
        'dir': os.path.join(file_dir, 'images'),
        'headers': {
            'cache-control': 'max-age=0',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                Chrome/99.0.4844.82 Safari/537.36'
        },
    }


def take_input(messages):
    inputs = []
    print('Enter "r" to reset or "q" to exit.')
    for message in messages:
        inp = input(message)
        if inp == 'q' or inp == 'Q':
            return None
        if inp == 'r' or inp == 'R':
            return take_input(messages)
        inputs.append(inp)
    return inputs


points_of_interest_filename = './input/POIs.txt'
size_of_tile_in_meters = 250
zoom = 20
get_adjacent_tiles = True


def run():
    with open(os.path.join(file_dir, 'preferences.json'), 'r', encoding='utf-8') as f:
        prefs = json.loads(f.read())

    if not os.path.isdir(prefs['dir']):
        os.mkdir(prefs['dir'])

    if not os.path.isfile(points_of_interest_filename):
        print(f'File {points_of_interest_filename} not found.')
        return

    points_of_interests = get_dd_from_poi(points_of_interest_filename)

    batch_id = datetime.now().strftime('z{zoom}_%Y-%m-%d_%H-%M-%S'.format(zoom=zoom))
    batch_directory = os.path.join(prefs['dir'], batch_id)
    os.mkdir(batch_directory)

    counter = 0
    for poi in points_of_interests:
        counter += 1
        download_image_from_poi(poi, counter, batch_directory,
                                prefs, zoom, size_of_tile_in_meters,
                                get_adjacent_tiles)


if os.path.isfile(prefs_path):
    run()
else:
    with open(prefs_path, 'w', encoding='utf-8') as f:
        json.dump(default_prefs, f, indent=2, ensure_ascii=False)

    print(f'Preferences file created in {prefs_path}')
