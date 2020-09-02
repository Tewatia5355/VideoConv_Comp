import os
import cv2
import sys
import glob
import errno
import numpy as np
import filetype
import re
import shutil
from os.path import isfile, join

# If command Line arguments are less, code will exit


def comp_code(file_name, scale_percent):

  # Getting current path
    cur_path = os.getcwd()
    file_path = os.path.join(cur_path+"\\uploads", file_name)
    curr_path = cur_path + "\\processing"
    os.chdir(curr_path)

  # Checks if file is a video file or not
    kind = filetype.guess(file_path)
    if kind == None:
        # print("File Format is not video please try again")
        return "File Format is not video please try again", -1
    x = re.search("^video", kind.mime)
    if x == None:
        # print("File Format is not video please try again")
        return "File Format is not video please try again", -1

  # Storing video name and extension for naming output file
    videoName = (os.path.splitext(file_name))[0]
    videoExtension = (os.path.splitext(file_name))[1]
    cap = cv2.VideoCapture(file_path)

  # Storing Fps of video
    fps = cap.get(cv2.CAP_PROP_FPS)

   # Extraction of frames starts
    img_array = []
    # print("Extracting Frames...")
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized = cv2.resize(frame, dim)
        img_array.append(resized)

  # Path of output video file
    pathOut = join(curr_path, videoName+"_output"+videoExtension)

  # Checking if output file exists, if yes it will remove it
    if os.path.exists(pathOut):
        # print("Old output file Detected: removing it!!")
        os.remove(pathOut)

  # Process of making video starts
    out = cv2.VideoWriter(pathOut, cv2.VideoWriter_fourcc(
        'm', 'p', '4', 'v'), fps, dim)

    for i in range(len(img_array)):
        out.write(img_array[i])
    # print("Output File is generated.")

    # Releases all variable
    os.chdir(cur_path)
    out.release()
    cap.release()
    cv2.destroyAllWindows()

    out_name = videoName+"_output"+videoExtension
    pathOutt = join(cur_path + "\\output", out_name)
    if os.path.exists(pathOutt):
        # print("Old output file Detected: removing it!!")
        os.remove(pathOutt)
    shutil.copy(pathOut, cur_path+"\\output")
    try:
        os.remove(pathOut)
        os.remove(file_path)
    except OSError:
        print("Error in removing raw folder images")
    # print("Code terminated successfully!!")
    return pathOutt, out_name, 0
