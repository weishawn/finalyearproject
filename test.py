import cv2
import time
import os
import serial
import threading
import winsound
import numpy as np
import cv2
import glob
import io
import math
from datetime import datetime

#list of signals
# 0 - Start signal once the take image button was pressed
# 1 - EL
# 2 - PL
# 3 - moving to the next cell
# 4 - PSU_ready
# 5 - Force stop
# 6 - off

#-1 - EL done
#-2 - PL done
#-3 - reversing the direction

EL = ""
PL = ""
count = 0
state = 0
multiexposure_input = 9

ser = None
#ser = serial.Serial(port='COM6', baudrate=115200, timeout=.1)
############################################################


#make directory#########
def directory():
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y_%H%M%S")
    EL = "EL_" + dt_string
    PL = "PL_" + dt_string
    os.makedirs('EL_%s' % dt_string)
    os.makedirs('PL_%s' % dt_string)
    return EL, PL


###############################################


def Imaging(mode, count):
    if count == 0:
        directory()
    cap = cv2.VideoCapture(0)
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
            print(count)
            number = math.ceil(count / 2)
            if mode == 2:
                cv2.imwrite(str(EL) + "/frame%d.jpg" % number, img)
                print("EL_" + str(number))

                if number % 3 == 0:
                    frequency = 1000
                    duration = 1000
                    winsound.beep(frequency, duration)
                    # reverse the motor and move the panel manually
                    write_read('-3')

                break
            elif mode == 1:
                cv2.imwrite(str(PL) + "/frame%d.jpg" % number, img)
                print("PL_" + str(number))
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

#create serial connection############
def PSU(mode):
    #after switch then
    print("switched to mode " + str(mode))

class SerialReaderThread(threading.Thread):
    def run(self):
        global ser
        serial.Serial(port='COM6', baudrate=115200, timeout=.1)
        while True:
            data = ser.readline().decode('utf-8')
            if data == 8:
                print("PL mode done - program")
            if data == 9:
                print("EL mode done - program")

class FileWriting(threading.Thread):
   def run(self):
        while True:
            print("hello")
serial_thread = SerialReaderThread()
file_thread = FileWriting()
serial_thread.start()
file_thread.start()
serial_thread.join()
file_thread.join()

# def write_read(x):
#     ser.write(bytes(x, 'utf-8'))
#     time.sleep(0.05)
#     data = ser.readline().decode('utf-8').rstrip()
#     # data = ser.read()
#     print("write read data")
#     print(data)
#     if data == 4:
#         print("PL")
#     if data == 5:
#         print("EL")   
    # if value == b'\x04':
    #     print("PSU set to PL")
    # if(data == b'\x01'):
    #     print('EMERGENCY STOP')

    # if(data == b'\x02' and count%2 != 0):
    #     print('Camera steady and ready to take EL image')
    #     Imaging(2,count)
    #     # imaging(mode, count)
    # if(data == b'\x02' and count%2 == 0):
    #     print('Camera steady and ready to take PL image')
    #     Imaging(1,count)

    # return data

# while True:
#     #num = input("Enter a number: ") # Taking input from user
#     #keep running this while loop for input and functions to call
#     print("Ready for imaging")
#     # start = input("Enter a number: ")
#     for x in range(3):
#         write_read('4')
#         time.sleep(2)
#         write_read('5')
#         time.sleep(2)
#         if x ==2 :
#             print("imaging done")
#             break
    
    #     PSU(1)
    #     value = write_read("-4")
    #     time.sleep(1)
    #     if value == b'\x04':
    #         print("PSU set to PL")
    #     value = write_read('-1')
    #     time.sleep(3)
    #     # zeroing is required
    #     # give an initial state, start with PL
    #     if value == 1:
    #         print("homing done, ready to take first PL image")
    #         Imaging(1, count)
    #         PSU(2)

            
    #     value =write_read("-5")
    #     time.sleep(1)
    #     if value == 5:
    #         print("PSU set to EL")
    #     value = write_read("-2")
    #     print("motor moved, ready for imaging")
    #     if value == 2:
    #         Imaging(2, count)

        # if x>0:
        #     PSU(1)
        #     write_read("-4")
        #     if write_read == 4:
        #         print("PSU set to PL")
        #     write_read('-2')
        #     # zeroing is required
        #     # give an initial state, start with PL
        #     time.sleep(5)
        #     if write_read == 2:
        #         print("motor moved, ready for imaging")
        #         Imaging(1,count)
        #         PSU(2)
        #     write_read("-5")
        #     if write_read == 5:
        #         print("PSU set to EL")
        #     write_read("-2")
        #     print("motor moved, ready for imaging")
        #     if write_read == 2:
        #         Imaging(2,count)

# while True:
#     if state == 0:
#         #Pull down to zero if idle
#         state = ser.readline().decode('ascii')
#     elif state == 1:
#         #todo toggle to PL mode
#         mode = 'PL'
#         print("PL")
#     elif state == 2:
#         mode = 'EL'
#         #todo toggle to EL mode
#         print("EL")
#     elif state == 3:
#         Imaging(mode,count)
#     elif state == 5:
#         count = 0
#         mode =  1

# t1 = threading.Thread(target = read_arduino)
# t2 = threading.Thread(target = Imaging)
# t1.start()
# t2.start()
# t1.join
# t2.join
#manually pressed button to take image
# while True:
#     ret, frame = cap.read()
#     cv2.imshow('webcam feed', frame)
#     if cv2.waitKey(1) & 0xFF == ord(' '):
#       cv2.imwrite("frame%d.jpg" % count, frame)
#       count +=1
#       if count == multiprocess_input:
#         break
