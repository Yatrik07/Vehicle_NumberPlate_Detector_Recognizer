import cv2
import bs4
import numpy as np

def getImage(filePath):
    '''
    FUnction accpets the image filePath and returns the image, conveting the color BGR2RGB
    '''
    # # imagePath = os.path.join("dataset", "images", fileName)
    # img = tf.io.read_file(filePath)
    # img = tf.io.decode_image(img, expand_animations=False)
    img = cv2.cvtColor(cv2.imread(filePath), cv2.COLOR_BGR2RGB)
    return img

def getBoundingBox(filePath, image_shape=(225,225)):
    '''
    Function takes filePath of annot file and returns xmin, ymin, xmax, ymax
    '''
    # data = tf.io.read_file(filePath).numpy().decode()
    with open(filePath, 'r') as f:
      data = f.read()

    bs = bs4.BeautifulSoup(data)

    xmin = int(bs.find("xmin").get_text())
    ymin = int(bs.find("ymin").get_text())
    xmax=  int(bs.find("xmax").get_text())
    ymax = int(bs.find("ymax").get_text())

    return np.array([xmin, ymin, xmax, ymax])


def get_transformed_data(images_path = "dataset/scaled/images2.npy", annot_path = "dataset/scaled/annotations2.npy"):
    with open(images_path, 'rb') as file:
        images = np.load(file)

    with open(annot_path, 'rb') as file:
        annotations = np.load(file)

    return images, annotations

