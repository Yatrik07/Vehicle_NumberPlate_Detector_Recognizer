import tensorflow as tf
import numpy as np
import cv2
import sklearn
from sklearn.model_selection import train_test_split
import os
from data_ingestion.data_ingestion import getBoundingBox
from image_processing.preprocessing import getImageAndAnnot
from data_ingestion.data_ingestion import get_transformed_data
from data_formation.data_formation import make_batches
from model_building.build_model import create_model
# # Uncomment this for saving all the imgs in .npy file from scratch




def get_transformed_images_and_annotations():

    # Defining paths
    images_path = os.path.join("dataset", "images")
    imageNames = [os.path.join("dataset", "images", x) for x in os.listdir(images_path)]
    # annotNames = [imageName.replace("images", "annotations").replace(".png", ".xml") for imageName in imageNames]
    annotNames = [imageName.replace("images", "annotations").replace(imageName.replace("images", "annotations").split('.')[-1],
                                                           "xml") for imageName in imageNames]
    annotations = [getBoundingBox(annotPath) for annotPath in annotNames]

    # Ready to get and store transformed images and annotations
    scaled_images = []
    scaled_annots = []

    # count = 0
    for imageName, annot in zip(imageNames, annotations):
        image, annot = getImageAndAnnot(imageName, annot)
        scaled_images.append(image)
        scaled_annots.append(annot)
        # if count<50:
        #   print(imageName, annotNames[count])
        #   count+=1


    return scaled_images, scaled_annots


def save_transformed_imagea_and_annots(images, annotations):
    with open("dataset/scaled/annotations2.npy", "wb") as annotWriter, open("dataset/scaled/images2.npy", "wb") as imageWriter:
        np.save(annotWriter, annotations)
        np.save(imageWriter, images)


def retrieve_and_split_data():
    final_images, final_annotaitons = get_transformed_data()

    X, X_test, y, y_test = train_test_split(final_images, final_annotaitons, test_size=0.1, random_state=32, shuffle=False)
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.1, random_state=32, shuffle=False)

    train_data = make_batches(X_train, y_train)
    test_data = make_batches(X_test, is_test=True)
    val_data = make_batches(X_val, y_val, is_val=True)
    full_data = make_batches(final_images, final_annotaitons)

    return full_data, train_data, test_data, val_data

def get_train_model(data):

    model = create_model()

    tensorboard_callback = tf.keras.callbacks.TensorBoard('tensorboard_logs', histogram_freq=1)

    model.fit()



