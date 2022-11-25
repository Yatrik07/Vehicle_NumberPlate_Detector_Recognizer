from flask import Flask, render_template, jsonify, request
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
import tensorflow as tf
import cv2
import numpy as np
import os
import datetime

from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired

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
    try:
        if request.method == 'POST':

            f = request.files['img1']
            f.save('static/files/'+secure_filename(f.filename))
            print('static/files/'+f.filename)
            # print(f)
            return ' new Form Submitted'

    except Exception as e:
        return 'There is some error : \n' + str(e)


@app.route('/retrain', methods=[ "GET", "POST"])
@cross_origin()
def retrain_model():
    pass


if __name__ == "__main__":
    app.run()

