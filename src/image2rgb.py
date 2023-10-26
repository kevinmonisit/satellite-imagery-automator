from PIL import Image
import numpy as np
import os
import json

width = 80
height = 80


def extract_rgb_channels(data):
    if len(data) != 3:
        raise ValueError("Input data should have 3 channels.")

    if len(data[0]) != width * height:
        raise ValueError("Input data should have 19200 integers.")

    red_channel = data[0]
    green_channel = data[1]
    blue_channel = data[2]

    if len(red_channel) != len(green_channel) or len(red_channel) != len(blue_channel):
        raise ValueError("Input data should have 19200 integers.")

    return red_channel, green_channel, blue_channel


def read_and_prepare_image(image_path):
    image = Image.open(image_path)

    image = image.resize((80, 80))

    if image.mode != 'RGB':
        image = image.convert('RGB')

    data = []
    bands = [0, 1, 2] # where 0 = R

    for band in bands:
        pixels = list(image.getdata(band=band))
        data.append(pixels)

    return data


def list_files_in_dir(dir_path):
    return [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]


def save_to_json(data, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=True, separators=(',', ':'), indent=4)
        print(f"Data successfully saved to {file_path}")
    except Exception as e:
        print(f"An error occurred while saving the data to JSON: {e}")


if __name__ == '__main__':
    data = []
    labels = []
    input_dir = 'input/rgb_extract/'
    output_filename = 'out/json/image_data_w={w}_h={h}.json'.format(w=width, h=height)
    potential_images = list_files_in_dir(input_dir)

    for image_name in potential_images:
        if image_name.endswith('.png') is False:
            continue

        class_indicator = image_name[0]
        if class_indicator.isdigit() is False or int(class_indicator) not in range(0, 2):
            print(f"Skipping {image_name} because it doesn't start with a classification indicator.")
            continue

        res = read_and_prepare_image(os.path.join(input_dir, image_name))

        for channel in extract_rgb_channels(res):
            data.append(channel)

        labels.append(int(class_indicator))

    res = {}
    res['data'] = data
    res['labels'] = labels

    save_to_json(res, output_filename)
