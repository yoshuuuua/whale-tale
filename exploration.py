import math
from collections import Counter

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random
from PIL import Image

from tqdm import tqdm

from keras.preprocessing.image import (
    random_rotation, random_shift, random_shear, random_zoom,
    random_channel_shift, transform_matrix_offset_center, img_to_array)

INPUT_DIR = './input'
OUTPUT_DIR = './augmented/'

def plot_images_for_filenames(filenames, labels, rows=4):
    imgs = [plt.imread(f'{INPUT_DIR}/train/{filename}') for filename in filenames]

    return plot_images(imgs, labels, rows)


def plot_images(imgs, labels, rows=4):
    # Set figure to 13 inches x 8 inches
    figure = plt.figure(figsize=(13, 8))

    cols = len(imgs) // rows + 1

    for i in range(len(imgs)):
        subplot = figure.add_subplot(rows, cols, i + 1)
        subplot.axis('Off')
        if labels:
            subplot.set_title(labels[i], fontsize=16)
        plt.imshow(imgs[i], cmap='gray')

def random_greyscale(img, p):
    if random.random() < p:
        return np.dot(img[...,:3], [0.299, 0.587, 0.114])

    return img

def augmentation_pipeline(img_arr):
    img_arr = random_rotation(img_arr, 18, row_axis=0, col_axis=1, channel_axis=2, fill_mode='nearest')
    img_arr = random_shear(img_arr, intensity=0.4, row_axis=0, col_axis=1, channel_axis=2, fill_mode='nearest')
    img_arr = random_zoom(img_arr, zoom_range=(0.9, 2.0), row_axis=0, col_axis=1, channel_axis=2, fill_mode='nearest')
    img_arr = random_greyscale(img_arr, 0.4)

    return img_arr



np.random.seed(42)
train_df = pd.read_csv(INPUT_DIR + '/train.csv')

image_ids_pair = train_df['Id'].value_counts()
few_id_pairs = pd.Series(image_ids_pair).where(lambda x : x<5).dropna()
id_filename_pairs = {}
for id, value in few_id_pairs.items():
    id_filename_pairs[id] = list(train_df[train_df['Id'] == id]['Image'])
for id, file_names in id_filename_pairs.items():
    for i in range(5 - (len(file_names))):
        file_name =  random.choice(file_names)
        img = Image.open(f'{INPUT_DIR}/train/' + file_name)
        img_arr = img_to_array(img).astype(int)
        img = augmentation_pipeline(img_arr)
        # plot_images([img], None, rows=1)
        im = Image.fromarray(img.astype('uint8'))
        im.save(OUTPUT_DIR+ "aug_" + str(i) + "_" + file_name)

# img = Image.open(f'{INPUT_DIR}/train/ff38054f.jpg')
# img_arr = img_to_array(img).astype(int)
# img = augmentation_pipeline(img_arr)
# plot_images([img], None, rows=1)
# im = Image.fromarray(img.astype('uint8'))
# im.save(OUTPUT_DIR+ "aug_" + "ff38054f.jpg")


#
# imgs = [
#     random_rotation(img_arr, 30, row_axis=0, col_axis=1, channel_axis=2, fill_mode='nearest')
#     for _ in range(5)]
# print(imgs[0])
# plot_images(imgs, None, rows=1)

# imgs = [
#     random_shift(img_arr, wrg=0.1, hrg=0.3, row_axis=0, col_axis=1, channel_axis=2, fill_mode='nearest')
#     for _ in range(5)]
# plot_images(imgs, None, rows=1)

# imgs = [
#     random_shear(img_arr, intensity=0.4, row_axis=0, col_axis=1, channel_axis=2, fill_mode='nearest')
#     for _ in range(5)]
# plot_images(imgs, None, rows=1)

# imgs = [
#     random_zoom(img_arr, zoom_range=(1.5, 0.7), row_axis=0, col_axis=1, channel_axis=2, fill_mode='nearest')
#     for _ in range(5)]
# plot_images(imgs, None, rows=1)

# imgs = [
#     random_greyscale(img_arr, 0.5)
#     for _ in range(5)]
#
# plot_images(imgs, None, rows=1)



# plt.show()
