import cv2
import numpy as np
import matplotlib.pyplot as plt
from data_ingestion.data_ingestion import getImage


def resizeAndScale(img, image_shape=(225, 225)):
    '''
    Function Accepts an image and rescale to 0 - 1 range and resizes it to the given IMAGE_SHAPE
    '''
    img = cv2.resize(img, image_shape)
    return img/255


def getImageAndAnnot(imagePath, annot, image_shape=(225, 225)):
    '''
    Function accepts the imagePath, annotations, and image shape
    It reads the image
    extracts the annots from the arg

    AND RESCALES THE ANNOTATIONS TO THE GIVEN IMAGE SHAPE

    Returns 1. resized and rescaled image
            2. scaled xmin, xmax, ymin, ymax

    '''

    image = getImage(imagePath)
    xmin, ymin, xmax, ymax = annot

    # image =
    x_scale = image_shape[1] / image.shape[1]
    y_scale = image_shape[0] / image.shape[0]

    return resizeAndScale(image), np.array([
        np.round(xmin * x_scale),
        np.round(ymin * y_scale),
        np.round(xmax * x_scale),
        np.round(ymax * y_scale)
    ])



def showImageWithAnnot(image, annot, title='Image'):
    '''
    Accepts image and annotations and annotations and shows image with the bounding box
    '''
    annot = list(annot.astype(int))
    image = cv2.rectangle(image, annot[:2], annot[2:], (0, 0, 1), 2)
    plt.imshow(image)
    plt.axis('off')
    plt.title(title)
    plt.show()
