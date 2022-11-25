import tensorflow as tf
import os
from image_processing.preprocessing import resizeAndScale
import numpy as np

def load_model(filepath = os.path.join('models', 'DetectionModel2.h5')):
    model = tf.keras.models.load_model(filepath=filepath)
    return model

def prediction_on_single_image(image, model):
    image = resizeAndScale(image)
    image = np.array([image])
    predictions = model.predict(image)
    return predictions


