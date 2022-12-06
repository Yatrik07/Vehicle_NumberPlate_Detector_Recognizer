import pytesseract
import easyocr
import cv2
import matplotlib.pyplot as plt
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
def read_number(img):
    config = ('-l eng --oem 1 --psm 3')
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


    # sp = cv2.imread("download.jpeg", flags = 0)
    # sp = cv2.imread("test3.jpeg", flags = 0)
    # sp = cv2.imread("Capture2.JPG", flags = 0)
    # plt.imshow(sp)
    # print(sp.shape)
    # sp = sp[:60, :]
    # sp = cv2.threshold (cv2.cvtColor( cv2.erode(sp, kernel = np.ones((2,2)), iterations=1) , cv2.COLOR_BGR2GRAY ),thresh=127.5, maxval = 255, type = cv2.THRESH_BINARY )[1]
    # plt.imshow(sp, cmap='gray')
    # text = pytesseract.image_to_string(sp, config=config)
    text = pytesseract.image_to_string(img, config=config)

    # text = pytesseract.image_to_string(sp, config=config)
    return validation_update(text)

# img = cv2.imread('../static/files/detected_cropped_img.jpeg')
# plt.imshow(img)
# plt.show()
# txt = read_number(img)
# print(txt, type(txt))

def validation_update(string):
  special_characters =list("!@#$%^&*()-+?_=,<>/{}[].^'\\")
  pos = 0
  for ch,pos in zip(string , range(len(string))):
    if ch in special_characters:
      string = string.replace(ch, '')
  return string.strip()

def apply_easyocr(img):
    reader = easyocr.Reader(['en'])
    # cropped_image = cv2.imread("/content/detected_cropped_img.jpeg")
    result = reader.readtext(img)
    final = ''
    for i in result:
        # print(i[-2])
        final = final + i[-2]
    return validation_update(final)

