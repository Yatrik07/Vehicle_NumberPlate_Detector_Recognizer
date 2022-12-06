from flask import Flask, render_template, jsonify, request, send_file
from flask_cors import CORS, cross_origin
import tensorflow as tf
import cv2
import numpy as np
import os
import datetime
from werkzeug.utils import secure_filename
import os
from prediction.make_predictions import *
from image_processing.preprocessing import showImageWithAnnot, resize
from OCR.ocr import read_number, apply_easyocr
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

app =Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/files'
app.config['SECRET_KEY'] = 'supersecretkey'


@app.route('/', methods=['GET', "POST"])
@cross_origin()
def home_page():
    # logger.write_logs("Someone Entered Homepage, Rendering Homepage!")

    return render_template("index2.html")


@app.route('/submit', methods=[ "GET", "POST"])
@cross_origin()
def prediction_page():
    # try:
        if request.method == 'POST':

            Imgfile = request.files['img1']
            # Imgfile.save('static/files/'+secure_filename(Imgfile.filename))
            imageFilePath = 'static/files/inputImage.'+str(secure_filename(Imgfile.filename).split('.')[-1])
            Imgfile.save( imageFilePath )
            # print('static/files/'+Imgfile.filename)
            
            # model = load_model()
            # pred = prediction_on_single_image( imageFilePath , model , single=True )
            # path = showImageWithAnnot(imageFilePath, pred, save=True, path = 'static/files', title='single prediction', show=False)

            resized = resize(imageFilePath)
            detected, cropped, detected_path, cropped_path = yolo_model(img_path=imageFilePath)
            


            # return ' new Form Submitted'
            # return send_file(path , mimetype='image/gif')
            # print(path)
            print(detected_path, cropped_path)

            text = read_number(cropped)
            easyocr_text = apply_easyocr((cropped))

            return render_template("img.html", input = r'static\files\resized_input_img.jpg', detected = detected_path, cropped = cropped_path, text=text, easyocr_text= easyocr_text) # , img_path_final = final_path

    # except Exception as e:
    #     return 'There is some error : \n' + str(e)
        # return send_file(path , mimetype='image/gif')


@app.route('/retrain', methods=[ "GET", "POST"])
@cross_origin()
def retrain_model():
    pass


if __name__ == "__main__":
    app.run()

