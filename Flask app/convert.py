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


def conv_code(file_name):
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

    # Storing Total Number of frames
    no_of_files = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    # Temporary Variable, will be used to name images in sorted manner!!
    digits_files = len(str(no_of_files))

    # Path where extracted frames will be stored
    new_path = curr_path+"\\raw"

    # If path exist it will ask to delete all files in it or exit, else if not exists it will create directory
    if(os.path.exists(new_path)):
        shutil.rmtree(new_path)
    else:
        os.mkdir(new_path)
        os.chdir(new_path)

    # Extraction of frames starts
    i = 1
    # print("Extracting Frames...")
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        tempName = ("0"*(digits_files - len(str(i)))) + str(i)
        cv2.imwrite('raw'+tempName+'.jpg', frame)
        i += 1
    # print("Frames Extracted Successfully.")

    # Black and white Images will be stored here in this path
    out_image_dir = curr_path + "\\output_images"

    # Checks if path exist will delete all files in it then starts conversion, else it will create the directory
    if(os.path.exists(out_image_dir)):
        shutil.rmtree(out_image_dir)
    else:
        os.mkdir(out_image_dir)

    # Conversion of color images starts
    os.chdir(new_path)
    # print("Converting Frames to Black&White frames...")
    i = 1
    for fil in glob.glob("*.jpg"):
        image = cv2.imread(fil)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        tempName = ("0"*(digits_files - len(str(i)))) + str(i)
        cv2.imwrite(os.path.join(out_image_dir,
                                 "out"+tempName+".jpg"), gray_image)
        i += 1
    # print("Conversion Successfully.")
    # Making video from black and white images
    os.chdir(out_image_dir)

    # Path of output video file
    pathOut = join(curr_path, videoName+"_output.mp4")

    # Checking if output file exists, if yes it will remove it
    if os.path.exists(pathOut):
        # print("Old output file Detected: removing it!!")
        os.remove(pathOut)

    # Process of making video starts
    # print("Output file is been generated...")
    img_array = []
    for filename in glob.glob('*.jpg'):
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)

    out = cv2.VideoWriter(pathOut, cv2.VideoWriter_fourcc(
        'm', 'p', '4', 'v'), fps, size, isColor=False)

    for i in range(len(img_array)):
        out.write(img_array[i])
    # print("Output File is generated.")

    # Releases all variable
    os.chdir(cur_path)
    out.release()
    cap.release()
    cv2.destroyAllWindows()

    # Deleting all the intermediate images (Comment lines below if you wanna see them)
    shutil.copy(pathOut, cur_path+"\\output")
    pathOutt = join(cur_path + "\\output", videoName+"_output.mp4")
    try:
        os.remove(pathOut)
        shutil.rmtree(new_path)
        os.remove(file_path)
    except OSError:
        print("Error in removing raw folder images")
    try:
        shutil.rmtree(out_image_dir)
    except OSError:
        print("Error in removing output folder images")

    # print("Code terminated successfully!!")
    return pathOutt, 0
