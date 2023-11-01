from PIL import Image
import numpy as np
import os
import sys
from datetime import datetime
import shutil


def create_directory(directory_path):
    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        print(f"Directory '{directory_path}' already exists. Deleting and recreating it.")
        shutil.rmtree(directory_path)
    else:
        print(f"Creating directory '{directory_path}'.")

    os.makedirs(directory_path)
    print(f"Directory '{directory_path}' created successfully.")


def split_image(input_image_path, output_folder, n):
    """
    Split an image into N x N squares and save them in the output folder.
    """

    file_name = os.path.basename(input_image_path)
    print("Splitting {file_name} into {n} x {n} tiles...".format(file_name=file_name, n=n))

    img = Image.open(input_image_path)
    img_width, img_height = img.size

    tile_width = img_width // n
    tile_height = img_height // n

    for i in range(0, n):
        for j in range(0, n):
            left = i * tile_width
            upper = j * tile_height
            right = left + tile_width
            lower = upper + tile_height

            img_cropped = img.crop((left, upper, right, lower))

            img_cropped.save(f"{output_folder}/{file_name}_tile_{i}_{j}.png")


def list_files_in_dir(dir_path):
    return [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]


if __name__ == '__main__':

    if len(sys.argv) < 3:
        print("Usage: python3 split_images.py <partitions> <input_dir>")
        sys.exit(1)

    if not os.path.isdir('out/partitions'):
        os.mkdir('out/partitions')

    batch_id = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    batch_directory = os.path.join('out/partitions/', batch_id)
    os.mkdir(batch_directory)

    class_0_dir = os.mkdir(os.path.join(batch_directory, '0'))
    class_1_dir = os.mkdir(os.path.join(batch_directory, '1'))

    data = []
    labels = []

    partitions = int(sys.argv[1])
    input_dir = os.path.abspath(os.path.normpath(sys.argv[2]))

    candidate_images = list_files_in_dir(input_dir)

    for image_name in candidate_images:
        if image_name.endswith('.png') is False:
            continue

        # output_folder = os.path.join('out/partitions',
        #                              '{image_name}_partitions'.format(image_name=image_name))
        # create_directory(output_folder)

        res = split_image(os.path.join(input_dir, image_name), batch_directory, partitions)
