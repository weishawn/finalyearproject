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
arduino = serial.Serial(port='COM6', baudrate=115200, timeout=.1)

start = 0
camerasteady = 0
PLready = 0
ELready = 0
rows = 3

count = 0
multiexposure_input = 9


mode = 1
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
            global mode
            if mode == 2:
                cv2.imwrite(str(EL) + "/frame%d.jpg" % number, img)
                print("EL_" + str(number))
                mode = 1
                if number % 3 == 0:
                    frequency = 1000
                    duration = 1000
                    winsound.beep(frequency, duration)
                    # reverse the motor and move the panel manually
                    write_thread('3')

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

#create serial connection############
def PSU(mode):
    #after switch then
    print("Switch to mode " + str(mode)+ " in power supply")


def serialwrite(x):
    arduino.write(bytes(x, 'utf-8'))

def readthread():
    global camerasteady
    global start
    global PLready
    global ELready
    while True:
        data = arduino.readline()
        if(data == b'\x01'):
            print('HOMING DONE')
            camerasteady = 1
            start = 0
        else:
            camerasteady = 0
        if(data == b'\x02'):
            print('CAMERA STEADY')
            camerasteady = 1
        else:
            camerasteady = 0

        if(data == b'\x03'):
            print('Reverse direction')

        if(data == b'\x04'):
            print('PL ready')
            PLready = 1
        else:
            PLready = 0

        if(data == b'\x05'):
            print('EL ready')
            ELready = 1
        else:
            ELready = 0
        


read_thread = threading.Thread(target=readthread)
read_thread.daemon = True
read_thread.start()

def waitUntil(condition, output):
    wait = True
    while wait == True:
        if condition:
            output
            wait = False
        time.sleep(0.5)

while True:
    start = input("Enter a number: ")
    time.sleep(3)

    rowscompleted = 0  
    while(start):
        if (rowscompleted == rows): #stop when all rows completed
            break          #break out of while loop
              #move to home position
        #multiexposure_input is the number of total pictures
        #rows it the number of rows of cells in the panel
        for x in range(multiexposure_input):
            PSU(1)                #Change PSU
            if(start == 0): break #check if stop button is pressed
            if x>0:
                serialwrite('2')   #move to next cell
            else:
                serialwrite('1')
            if(start == 0): break      
            waitUntil(camerasteady, serialwrite('4')) #if camerasteady switch to PL
            if(start == 0): break     
            waitUntil(PLready ==5, Imaging()) #take PL image
            if(start == 0): break 
            serialwrite('6')   #off
            if(start == 0): break 
            PSU(2)                #Change PSU
            if(start == 0): break 
            serialwrite('5') #switch to EL
            if(start == 0): break 
            waitUntil(ELready, Imaging())    #take EL image
            if(start == 0): break 
            serialwrite('6')   #off
            
            if x ==multiexposure_input-1:
                print("done ready for stitching")
                break