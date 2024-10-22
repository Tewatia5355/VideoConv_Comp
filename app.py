import os
import cv2
import sys
import glob
import errno
import numpy as np
import filetype
import re
import shutil
from flask import Flask, render_template, request, redirect, url_for, abort, send_file
from werkzeug.utils import secure_filename
from os.path import isfile, join
from convert import conv_code
from compressVideo import comp_code

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024*1024*12
app.config['UPLOAD_EXTENSIONS'] = ['.mp4', '.m4v', '.mkv',
                                   '.webm', '.mov', '.avi', '.wmv', '.mpg', '.flv']
app.config['UPLOAD_PATH'] = 'uploads'
app.config['OUTPUT_PATH'] = 'output'


@app.errorhandler(404)
def not_found(e):
    return render_template('error.html')


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/compress")
def compress():
    return render_template("compress.html")


@app.route("/convert")
def convert():
    return render_template("convert.html")


@app.route("/process", methods=['POST'])
def process_file():
    uploaded_file = request.files['file']
    parent_url = request.referrer.split('/')
    req_process = parent_url[3]
    # app.logger.info(request.form)
    filename = secure_filename(uploaded_file.filename)
    emailId = request.form['emailaddress']
    output_file = filename
    currr_path = os.getcwd()
    temp = currr_path + "/output"
    if os.path.exists(temp):
        os.chdir(temp)
        files = glob.glob('*')
        for f in files:
            os.remove(f)
    else:
        os.mkdir(temp)
    os.chdir(currr_path)
    success_code = -1
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        if os.path.exists(join(app.config['UPLOAD_PATH'], filename)):
            os.remove(join(app.config['UPLOAD_PATH'], filename))
        uploaded_file.save(join(app.config['UPLOAD_PATH'], filename))
        if req_process == 'convert':
            output_file, out_name, success_code = conv_code(filename)
            # app.logger.info(str(req_process)+"  "+str(emailId)+" "+str(filename))
        else:
            scale_percent = int(request.form['scaling_factor'])
            output_file, out_name, success_code = comp_code(
                filename, scale_percent)
            # app.logger.info(str(req_process)+"  "+str(emailId)+"  "+str(scale_percent))
        if success_code == 0:
            return send_file(output_file, as_attachment=True, attachment_filename=out_name)
        else:
            app.logger.error(output_file)
            abort(400)


if __name__ == "__main__":
    app.run()
