from flask import Flask, render_template, jsonify, request, send_file
from flask_cors import CORS, cross_origin
import tensorflow as tf
import cv2
import numpy as np
import os, shutil
import datetime
from werkzeug.utils import secure_filename
import os
from prediction.make_predictions import *
from image_processing.preprocessing import showImageWithAnnot, resize
from OCR.ocr import read_number, apply_easyocr
from database_operations.DB_operstions import DBOperations
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
from pathlib import Path

app =Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/files'
app.config['SECRET_KEY'] = 'supersecretkey'

database = db = DBOperations()
@app.route('/', methods=['GET', "POST"])
@cross_origin()
def home_page():
    # logger.write_logs("Someone Entered Homepage, Rendering Homepage!")
    database.create_Database_Table()
    return render_template("index2.html")


@app.route('/submit', methods=[ "GET", "POST"])
@cross_origin()
def prediction_page():
    try:
        if request.method == 'POST':

            Imgfile = request.files['img1']
            print('name',Imgfile, Imgfile.filename, type(Imgfile), sep='/n')
            # print(Imgfile.filename, type(Imgfile.filename))
            # Imgfile.save('static/files/'+secure_filename(Imgfile.filename))
            imageFilePath = 'static/files/inputImage.'+str(secure_filename(Imgfile.filename).split('.')[-1])
            Imgfile.save( imageFilePath )
            print(imageFilePath)
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
            database.enter_recordTo_Table(str(easyocr_text))

            return render_template("img.html", input = r'static\files\resized_input_img.jpg', detected = detected_path, cropped = cropped_path, text=text, easyocr_text= easyocr_text) # , img_path_final = final_path
        
    except Exception as e:
        if "error: (-215:Assertion failed) !buf.empty() in function 'cv::imdecode_" in str(e):
            return render_template("error.html", message = "No File Selected.")
        else:
            return render_template("error.html", message = "No Number Plate detected in image.")
            


@app.route('/retrain', methods=[ "GET", "POST"])
@cross_origin()
def retrain_model():
    pass

@app.route('/database', methods=[ "GET", "POST"])
@cross_origin()
def display_data():
    _, rows = database.showTable()
    # print("start", rows, dir(rows), "end")
    return render_template('db.html', data=rows)

@app.route('/reset_session', methods=[ "GET", "POST"])
@cross_origin()
def reset():
    database = DBOperations()
    database.dropTabel()
    database.create_Database_Table()
    print("dropped.....")
    return render_template('error.html', message = "Reset Session Successful")
    # return  flask.url_for("home_page")

@app.route('/downnload_data', methods=[ "GET", "POST"])
@cross_origin()
def download():
    database = DBOperations()
    data = database.getDatafromDatabase()
    output_path = "output/Number_plate_data.csv"
    data.to_csv(output_path)
    downloads_path = str(Path.home() / "Downloads")
    shutil.copy(output_path, downloads_path)
    print(downloads_path)
    return render_template('error.html', message = "Data has started downloading.")




if __name__ == "__main__":
    app.run(port=8000)

