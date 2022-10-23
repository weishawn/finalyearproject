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
import winsound
from datetime import datetime

row = 3
column = 3
count = 0
multiexposure_input = 9
start = 0
mode = 1
stop = False
arduino_signal = 0
EL = ''
PL = ''
EL_voltage = 30
PL_voltage = 22
EL_current = 2.05
PL_current = 2.7


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
    # return EL,PLgit remote add origin https://github.com/weishawn/finalyearproject.git


def Imaging():
    global count
    global EL
    global PL
    global stop
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
        while j >= 10 and stop == False:
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
                break
            elif mode == 1:
                cv2.imwrite(str(PL) + "/frame%d.jpg" % number, img)
                print("PL_" + str(number))
                mode = 2
                break

        if cv2.waitKey(25) & 0xFF == ord('q'):
            # force stop button
            break

    cap.release()
    cv2.destroyAllWindows()


def imageStitching():
    # image_paths = glob.glob('small-intersection/*.jpg')
    global EL
    global PL

    EL_paths = glob.glob(EL + '/*.jpg')
    PL_paths = glob.glob(PL + '/*.jpg')

    print(EL_paths)
    print(PL_paths)

    PL_images = []
    EL_images = []

    for image in EL_paths:
        img = cv2.imread(image)
        img = cv2.resize(img, (200, 200))
        EL_images.append(img)

    for image in PL_paths:
        img = cv2.imread(image)
        img = cv2.resize(img, (200, 200))
        PL_images.append(img)

    #limitations
    # 1. Area of overlap must be big enough to detect feature points
    # 2. Ensure the captured image is perpendicular to ensure better warping

    imageStitcher = cv2.Stitcher_create()

    error_PL, stitched_img_PL = imageStitcher.stitch(PL_images)

    if not error_PL:
        stitched_img_resized_PL = cv2.resize(stitched_img_PL, (1000, 1000))
        cv2.imwrite("stitchedOutput_PL.png", stitched_img_resized_PL)
        cv2.imshow("Stitched Img_PL", stitched_img_resized_PL)
        cv2.waitKey(0)
    else:
        print("Images could not be stitched!")
        print("Likely not enough keypoints being detected!")

    error_EL, stitched_img_EL = imageStitcher.stitch(EL_images)

    if not error_EL:
        stitched_img_resized_EL = cv2.resize(stitched_img_EL, (1000, 1000))
        cv2.imwrite("stitchedOutput_PL.png", stitched_img_resized_EL)
        cv2.imshow("Stitched Img_PL", stitched_img_resized_EL)
        cv2.waitKey(0)
    else:
        print("Images could not be stitched!")
        print("Likely not enough keypoints being detected!")


def Write_PSU(x):
    serpsu.write(bytes(x, 'utf-8'))


def write_thread(x):
    ser.write(bytes(x, 'utf-8'))


def PSU(mode):

    print("Switch to mode " + str(mode) + " in power supply")
    #mode 1 is PL mode 2 is EL
    if (mode == 2):
        Write_PSU("VSET1:" + str(EL_voltage))
        time.sleep(2)
        Write_PSU("ISET1" + str(EL_current))
        time.sleep(0.1)
        Write_PSU("OUT1")

    elif (mode == 1):
        Write_PSU("VSET1:" + str(PL_voltage))
        time.sleep(2)
        Write_PSU("ISET1" + str(PL_current))
        time.sleep(0.1)
        Write_PSU("OUT1")

    elif mode == 3:
        Write_PSU("OUT0")
        time.sleep(0.1)


def motor_handshake(data):
    global stop
    #while data != b'\x01':
    while data != b'1\r\n':
        #while data != 1:

        data = ser.readline()
        #data = data.decode("utf-8")
        #print(data)
        #if 'x07' in data:
        # if data == b'\x07':
        if data == b'7\r\n':
            #if data == 7:
            stop = True
            print('emergency stop')
    return stop


def ELPL_handshake(data):
    global stop
    while data != b'2\r\n':
        data = ser.readline()
        if data == b'7\r\n':
            stop = True
            print('emergency stop')
    return stop


def rest_handshake(data):
    global stop
    while data != b'3\r\n':
        data = ser.readline()
        if data == b'7\r\n':
            print('emergency stop')
            stop = True
    return stop


def two_way_communication(data):
    global stop
    while data != b'3\r\n':
        data = ser.readline()
        if data == b'7\r\n':
            print('emergency stop')
            stop = True
    return stop


def read_thread():
    print("got in read thread")
    global arduino_signal
    global stop
    internal_cnt = 0
    data = 0
    while stop == False:
        data = ser.readline()
        # two_way_communication(data)
        # arduino_signal = 3
        # print("connection established")

        # homing to the first position
        if internal_cnt % int(
                multiexposure_input / row) == 0 or internal_cnt == 0:
            motor_handshake(data)
            print(stop)
            if stop == True: break
            print("Homing done - arduino")
            arduino_signal = 1

        # shut down the system momentarily to avoid high current from diff modes
        rest_handshake(data)
        print(stop)
        if stop == True: break
        arduino_signal = 6
        print("shut down, doing PL next - arduino")

        # toggle to PL
        ELPL_handshake(data)
        print(stop)
        if stop == True: break
        arduino_signal = 4
        print("Toggled to PL, imaging - arduino")

        # shut down the system momentarily to avoid high current from diff modes
        rest_handshake(data)
        print(stop)
        if stop == True: break
        arduino_signal = 6
        print("shut down, doing EL next -arduino")

        # toggle to EL
        ELPL_handshake(data)
        if stop == True: break
        arduino_signal = 5
        print("Toggled to EL, imaging and motor move next - arduino")

        # to detect row change
        if internal_cnt != 2 and internal_cnt != 5:
            motor_handshake(data)
            if stop == True: break
            print("Motor moved - arduino")
            arduino_signal = 2

        # to determine end of imaging
        if internal_cnt == multiexposure_input - 1:
            internal_cnt = 0

        internal_cnt += 1
    print("got out of read thread")


def action():
    global column
    global stop
    try:
        while True and stop == False:
            start = input("Enter a number:")
            time.sleep(3)
            while start == '3' and stop == False:
                # write_thread('3')
                # print("establishing connection")
                # while arduino_signal != 3:
                #     if stop is True:
                #         print('RETURN')
                #         return
                # number of images to be taken
                for x in range(multiexposure_input):
                    if x % int(multiexposure_input / row) == 0 or x == 0:
                        write_thread('1')
                        if x == 0:
                            print('Calibrating.........')
                        else:
                            print("Homing")
                        # calibration
                        while arduino_signal != 1:
                            if stop is True:
                                print('RETURN')
                                return

                    write_thread('6')
                    PSU(3)
                    print(
                        "shut down to ensure no high current residual during PL"
                    )
                    while arduino_signal != 6:
                        if stop is True:
                            print('RETURN')
                            return

                    PSU(1)
                    write_thread('4')
                    print("changing to PL")
                    while arduino_signal != 4:
                        if stop is True:
                            print('RETURN')
                            return
                    Imaging()
                    time.sleep(5)
                    write_thread('6')
                    PSU(3)
                    print(
                        "shut down to ensure no high current residual during EL"
                    )
                    while arduino_signal != 6:
                        if stop is True:
                            print('RETURN')
                            return

                    PSU(2)
                    write_thread('5')
                    print("changing to EL")
                    while arduino_signal != 5:
                        if stop is True:
                            print('RETURN')
                            return
                    Imaging()
                    PSU(3)
                    if x == multiexposure_input - 1:
                        print("done ready for stitching")
                        imageStitching()
                        start = 0
                        break

                    if x != 2 and x != 5:
                        write_thread('2')
                        print('Motor moving')
                        while arduino_signal != 2:
                            if stop is True:
                                print('RETURN')
                                return
                    else:
                        print("sliding the panel upwards")
                        frequency = 3000  # Set Frequency To 2500 Hertz
                        duration = 2000  # Set Duration To 1000 ms == 1 second
                        winsound.Beep(frequency, duration)

    except KeyboardInterrupt:
        PSU(3)
        print('Keyboard interrupt to stop program.')


def motor_calibration(cell_seperation, frame_to_center_of_first_cell):
    #1 rotation is 200 step. translates to 3.142cm of horizontal movement.
    #to get the distance moved by motor
    one_step_moved = (3.142 * 2 * 0.65) / 200  #in cm
    print(one_step_moved)
    motor_step = math.floor(cell_seperation / one_step_moved)
    print(motor_step)
    homing_distance = frame_to_center_of_first_cell - 2.5
    homing_step = math.floor(homing_distance / one_step_moved)
    print(homing_step)
    return motor_step, homing_step


if __name__ == "__main__":
    ser = serial.Serial(port='COM6', baudrate=115200, timeout=.1)
    # PSU serial connection
    serpsu = serial.Serial(port='COM3',
                           baudrate=9600,
                           bytesize=serial.EIGHTBITS,
                           parity=serial.PARITY_NONE,
                           stopbits=serial.STOPBITS_ONE,
                           timeout=1)
    #################################
    while True:
        ser.flushInput()
        time.sleep(2)

        write_thread('7')
        arduino_signal = 0
        start = 0
        row = 3
        column = 3
        count = 0
        multiexposure_input = 9
        start = 0
        mode = 1
        stop = False
        arduino_signal = 0
        EL = ''
        PL = ''
        x = 0
        motor_step = 0
        homing_step = 0

        t1 = threading.Thread(target=read_thread)
        t1.daemon = True
        t1.start()

        print('ACTION')
        PSU(3)

        cell_seperation = float(input("Enter cell seperation:"))
        frame_to_center_of_first_cell = float(
            input("Enter frame to center of first cell:"))
        motor_step, homing_step = motor_calibration(
            cell_seperation, frame_to_center_of_first_cell)
        print(motor_step, homing_step)
        write_thread(str(motor_step))
        time.sleep(1)
        write_thread(str(homing_step))

        action()
        PSU(3)
        # once it quit the action loop its gonna wait for input from software again
