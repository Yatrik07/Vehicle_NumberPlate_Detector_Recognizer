import tensorflow as tf
import os
from image_processing.preprocessing import resizeAndScale
import numpy as np
from data_ingestion.data_ingestion import getImage
import matplotlib.pyplot as plt
from utils.augmentations import letterbox
import cv2
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
from utils.dataloaders import IMG_FORMATS, VID_FORMATS, LoadImages
from utils.plots import Annotator, colors, save_one_box
from utils.general import (LOGGER, check_file, check_img_size, check_imshow, check_requirements, colorstr, cv2,
                           increment_path, non_max_suppression, print_args, scale_coords, strip_optimizer, xyxy2xywh)
from yolov5.One.detect import *

def load_model(filepath = os.path.join('models', 'DetectionModel2.h5')):
    model = tf.keras.models.load_model(filepath=filepath)
    return model

def prediction_on_single_image(imagePath, model, single=True):
    image = getImage(imagePath)
    image = resizeAndScale(image)
    image = np.array([image])
    predictions = model.predict(image)
    if single == False:
        predictions[0, 0] = predictions[0, 0] - 10
        predictions[0, 1] = predictions[0, 1] - 10
        predictions[0, 2] = predictions[0, 2] + 10
        predictions[0, 3] = predictions[0, 3] + 10
    
    return predictions


def using_contours(image):
    # image = imutils.resize(image, width=300)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_image = cv2.bilateralFilter(gray_image, 11, 17, 17)
    edged = cv2.Canny(gray_image, 30, 200)
    cnts, new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    image1 = image.copy()
    cv2.drawContours(image1, cnts, -1, (0, 255, 0), 3)

    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]
    screenCnt = None
    image2 = image.copy()
    cv2.drawContours(image2, cnts, -1, (0, 255, 0), 3)
    print('a')
    i = 7
    four = False
    for c in cnts:
        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * perimeter, True)
        if len(approx) == 4:
            screenCnt = approx
            x, y, w, h = cv2.boundingRect(c)
            new_img = image[y:y + h, x:x + w]
            cv2.imwrite(str(i) + '.png', new_img)
            i += 1
            four = True
            break
    print(screenCnt)

    cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 3)
    plt.imshow(image)
    plt.show()



def yolo_model(img_path, img_size = 640, save_path = "../output"):
    WEIGHTS_PATH = r"D:\PycharmProjects\dl1\yolov5\runs\train\yolov5s_results4\weights\best.pt"
    half = False
    DEVICE = "cpu"
    model = DetectMultiBackend(WEIGHTS_PATH, dnn=False) # , device=DEVICE

    img_path = img_path

    im= img0 = cv2.imread(img_path)

    stride = 32
    auto = True
    img = letterbox(im, img_size, stride=stride, auto=auto)[0]
    img = img.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
    img = np.ascontiguousarray(img)
    im = torch.from_numpy(img).to(DEVICE)
    im = im.float()
    im = im/255
    im = im[None]


    pred = model(im, augment=False, visualize=False)

    conf_thres=0.50  # confidence threshold
    iou_thres=0.45
    classes=None
    save_crop = False
    save_crop = True
    line_thickness = 3

    real_classes = ["license"]
    RESIZE = (720, 560)
    COLOR_BORDER = [0, 0, 255]
    COLOR_TEXT = [0, 255, 0]


    pred = non_max_suppression(pred, conf_thres, iou_thres, classes, False, max_det=1000)
    print("pred:",pred)

    max = pred[0][0][4]
    # print('max', max)
    max_element = 0
    for ind, i in enumerate(pred[0]):
        # print('ele:',i)
        # print('ele e', i[4])
        if int(i[4]) > max:
            max_element = ind

    print('max element',pred[0][max_element], "idx : ", max)
    # print(pred)

    pred[0] = pred[0][max_element:max_element + 1]
    print('sh',tf.shape(pred[0]))



    def transform(point, real, new):
        return int(point * new/real)

    for i, det in enumerate(pred):
        print(det.shape)
        p, im0 = img_path, img0.copy()
        gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
        imc = im0.copy() if save_crop else im0  # for save_crop
        real_width, real_height, _ = im0.shape
        new = cv2.resize(im0, (RESIZE[0], RESIZE[1]))
        print(new.shape)
        if len(det):
            det[:, :4] = scale_coords(im.shape[2:], det[:, :4], img0.shape).round()
            # print("det:",det)

            for j in det:

                x_start, y_start, x_end, y_end = (
                    transform(j[0], real_height, RESIZE[0]),
                    transform(j[1], real_width, RESIZE[1]),
                    transform(j[2], real_height, RESIZE[0]),
                    transform(j[3], real_width, RESIZE[1])
                )
                class_idx = int(j[-1])
                conf = j[-2]
                new = cv2.rectangle(new, (x_start, y_start), (x_end, y_end), COLOR_BORDER, 2)
                new = cv2.putText(new, real_classes[int(class_idx)]+" "+str(np.round(conf.numpy(),2)),(x_start, y_start-10),1,1.5,COLOR_TEXT,2)

                if y_start <50:
                    new = cv2.putText(new, real_classes[int(class_idx)]+" "+str(np.round(conf.numpy(),2)),(x_start, y_end+10),1,1.5,COLOR_TEXT,2)
                else :
                    new = cv2.putText(new, real_classes[int(class_idx)]+" "+str(np.round(conf.numpy(),2)),(x_start, y_start-10),1,1.5,COLOR_TEXT,2)


    file_name = 'img_with_bbox'
    file_name1 = 'cropped'
    cv2.imwrite(os.path.join(save_path,"detected_{}.jpeg".format(file_name)), new)

    cv2.imwrite(os.path.join(save_path,"detected_{}.jpeg".format(file_name1)), new[y_start:y_end, x_start:x_end])

    cv2.imwrite(os.path.join(r"static\files", "detected_img_with_bbox.jpeg"), new)
    cv2.imwrite(os.path.join(r"static\files", "detected_cropped_img.jpeg"), new[y_start:y_end, x_start:x_end])

    return new, new[y_start:y_end, x_start:x_end], os.path.join("/static/files", "detected_img_with_bbox.jpeg"), os.path.join("/static/files", "detected_cropped_img.jpeg")
