
# COlab File Link ---> https://colab.research.google.com/drive/19lJIq5195m4kof8l2U3unF03NsH3QxNh?usp=sharing

import numpy as np
import tensorflow as tf
import cv2
import os
from sklearn.model_selection import train_test_split


# Creating Batches

def make_batches(X, y=None, batch_size=32, reshuffle_each_iteration=True, is_test=False, is_val=False):
    if is_test:
        print("Creating Test Data batches...")
        data = tf.data.Dataset.from_tensor_slices(tf.constant(X))
        data_batch = data.batch(batch_size)
        return data_batch

    elif is_val:
        print("Creating Validation Data batches...")
        data = tf.data.Dataset.from_tensor_slices((tf.constant(X), tf.constant(y)))
        data_batch = data.batch(batch_size)
        return data_batch

    print("Creating Training Data batches...")
    data = tf.data.Dataset.from_tensor_slices((tf.constant(X), tf.constant(y)))
    data = data.shuffle(len(X), reshuffle_each_iteration=reshuffle_each_iteration)
    data_batch = data.batch(batch_size)
    return data_batch


def load_transformed_data():
    with open("dataset/scaled/images2.npy", 'rb') as file:
        images = np.load(file)

    with open("dataset/scaled/annotations2.npy", 'rb') as file:
        annotations = np.load(file)

    return images, annotations


def make_batches(X, y=None, batch_size=32, reshuffle_each_iteration=True, is_test=False, is_val=False):
    if is_test:
        print("Creating Test Data batches...")
        data = tf.data.Dataset.from_tensor_slices(tf.constant(X))
        data_batch = data.batch(32)
        return data_batch

    elif is_val:
        print("Creating Validation Data batches...")
        data = tf.data.Dataset.from_tensor_slices((tf.constant(X), tf.constant(y)))
        data_batch = data.batch(32)
        return data_batch

    print("Creating Training Data batches...")
    data = tf.data.Dataset.from_tensor_slices((tf.constant(X), tf.constant(y)))
    data = data.shuffle(len(X), reshuffle_each_iteration=reshuffle_each_iteration)
    data_batch = data.batch(32)
    return data_batch