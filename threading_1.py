import cv2
import time
import os
import serial
import threading
import numpy as np
import cv2
import glob
import io
import math
from datetime import datetime

row = 3
column = 3
count = 0
multiexposure_input = 9
ser = serial.Serial(port='COM6', baudrate=115200, timeout=.1)
start = 0
mode = 1
arduino_signal = 0
stop_threads = False
EL = ''
PL = ''


#make directory#########
def directory():
    global EL
    global PL
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y_%H%M%S")
    EL = "EL_" + dt_string
    PL = "PL_" + dt_string
    os.makedirs('EL_%s' % dt_string)
    os.makedirs('PL_%s' % dt_string)
    # return EL,PL
###############################################


def Imaging():
    global count
    global EL
    global PL
    if count == 0:
        directory()
    cap = cv2.VideoCapture(1)
    # Multiprocess input from IMPEL

    ########################
    while True:
        # Read and display each frame
        ret, img = cap.read()
        cv2.imshow('a', img)
        k = cv2.waitKey(125)
        # Specify the countdown
        j = 50
        # set the key for the countdown to begin
        while j >= 10:
            ret, img = cap.read()
            # Display the countdown after 10 frames so that it is easily visible otherwise,
            # it will be fast. You can set it to anything or remove this condition and put
            # countdown on each frame
            if j % 10 == 0:
                # specify the font and draw the countdown using puttext
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img, str(j // 10), (250, 250), font, 7,
                            (255, 255, 255), 10, cv2.LINE_AA)
            cv2.imshow('a', img)
            cv2.waitKey(125)
            j = j - 1

        else:
            ret, img = cap.read()
            # Display the clicked frame for 1 sec.
            # You can increase time in waitKey also
            cv2.imshow('a', img)
            cv2.waitKey(1000)
            # Save the frame
            count += 1
            number = math.ceil(count / 2)
            global mode
            if mode == 2:
                cv2.imwrite(str(EL) + "/frame%d.jpg" % number, img)
                print("EL_" + str(number))
                mode = 1
                # if number % 3 == 0:
                    # frequency = 1000
                    # duration = 1000
                    # winsound.beep(frequency, duration)
                    # reverse the motor and move the panel manually
                    # write_thread('3')
                break
            elif mode == 1:
                cv2.imwrite(str(PL) + "/frame%d.jpg" % number, img)
                print("PL_" + str(number))
                mode =2
                break

        if cv2.waitKey(25) & 0xFF == ord('q'):
            # force stop button
            break

    cap.release()
    cv2.destroyAllWindows()


###########################


def imageStitching():
    # image_paths = glob.glob('small-intersection/*.jpg')
    EL_paths = glob.glob(EL + '.jpg')
    PL_paths = glob.glob(PL + '.jpg')

    PL_images = []
    EL_images = []

    for image in EL_paths:
        img = cv2.imread(image)
        EL_images.append(img)

    for image in PL_paths:
        img = cv2.imread(image)
        PL_images.append(img)

    #limitations
    # 1. Area of overlap must be big enough to detect feature points
    # 2. Ensure the captured image is perpendicular to ensure better warping

    imageStitcher = cv2.Stitcher_create()

    error_PL, stitched_img_PL = imageStitcher.stitch(PL_images)
    stitched_img_resized_PL = cv2.resize(stitched_img_PL, (1000, 1000))

    if not error_PL:
        cv2.imwrite("stitchedOutput_PL.png", stitched_img_resized_PL)
        cv2.imshow("Stitched Img_PL", stitched_img_resized_PL)
        cv2.waitKey(0)
    else:
        print("Images could not be stitched!")
        print("Likely not enough keypoints being detected!")

    error_EL, stitched_img_EL = imageStitcher.stitch(EL_images)
    stitched_img_resized_EL = cv2.resize(stitched_img_EL, (1000, 1000))

    if not error_EL:
        cv2.imwrite("stitchedOutput_PL.png", stitched_img_resized_EL)
        cv2.imshow("Stitched Img_PL", stitched_img_resized_EL)
        cv2.waitKey(0)
    else:
        print("Images could not be stitched!")
        print("Likely not enough keypoints being detected!")

# imageStitching()


#create serial connection############
def PSU(mode):
    #after switch then
    print("Switch to mode " + str(mode)+ " in power supply")

def write_thread(x):
    ser.write(bytes(x, 'utf-8'))

def read_thread():
    global arduino_signal
    internal_cnt = 0
    while True:
        data = ser.readline()      
        if internal_cnt % int(multiexposure_input/row) == 0 or internal_cnt == 0:
            while data != b'\x01':
                data = ser.readline()
                continue 
            print("Homing done - arduino")
            arduino_signal = 1
        while data != b'\x06':
            data = ser.readline()
            continue
        arduino_signal = 6
        print("shut down, doing PL next -arduino")

        while data != b'\x04':
            data = ser.readline()
            continue
        arduino_signal = 4
        print("Toggled to PL, motor move next - arduino")

        while data != b'\x06':
            data = ser.readline()
            continue
        arduino_signal = 6
        print("shut down, doing EL next -arduino")

        while data != b'\x05':
            data = ser.readline()
            continue
        arduino_signal = 5
        print("Toggled to EL, motor move next - arduino")

        if internal_cnt != 2 and internal_cnt !=5:
            while data != b'\x02':
                data = ser.readline()
                continue 
            print("Motor moved - arduino")
            arduino_signal = 2

        if internal_cnt == multiexposure_input-1:
            internal_cnt = 0
            break
            
        internal_cnt +=1
      
t1 = threading.Thread(target=read_thread)
t1.daemon = True
t1.start()

def action():
    global column
    while True:
        start = input("Enter a number:")
        time.sleep(3)
        while start:
            for x in range(multiexposure_input):
                if x % int(multiexposure_input/row) == 0 or x == 0:
                    write_thread('1')
                    print('Motor homing')
                    while arduino_signal !=1:
                        continue

                write_thread('6')
                print("shut down to ensure no high current residual during PL")
                while arduino_signal !=6:
                    continue

                PSU(1)
                write_thread('4')
                print("changing to PL")
                while arduino_signal !=4:
                    continue
                Imaging()

                write_thread('6')
                print("shut down to ensure no high current residual during EL")
                while arduino_signal !=6:
                    continue
                
                PSU(2)
                write_thread('5') 
                print("changing to EL")
                while arduino_signal !=5:
                    continue
                Imaging()

                if x == multiexposure_input-1:
                    print("done ready for stitching")
                    imageStitching()
                    start = 0
                    break

                if x != 2 and x !=5 :
                    write_thread('2')
                    print('Motor moving')
                    while arduino_signal !=2:
                        continue
        break

action()