import cv2
import time
import os
import serial
import threading
from datetime import datetime


#  start by creating two folders
# mode 1 = PL
# mode 2 = EL
PSU_setting = True
now = datetime.now()
dt_string = now.strftime("%d%m%Y_%H%M%S")
print(dt_string)
EL = "EL_" + dt_string
PL = "PL_" + dt_string
print(EL)
print(PL)
os.makedirs('EL_%s' % dt_string)
os.makedirs('PL_%s' % dt_string)

cap = cv2.VideoCapture(0)
mode = 1
count = 0

# Multiprocess input from IMPEL
multiexposure_input = 3
########################

#serial communication port
serialcomm = serial.Serial('COM3', baudrate=9600, timeout=1)



#original algho
# def webcam_capture():
#     print("PL imaging")
#     while True:
#         # Read and display each frame
#         ret, img = cap.read()
#         cv2.imshow('a', img)
#         k = cv2.waitKey(125)
#         # Specify the countdown
#         j = 50
#         # set the key for the countdown to begin
#         while j >= 10:
#             ret, img = cap.read()
#             # Display the countdown after 10 frames so that it is easily visible otherwise,
#             # it will be fast. You can set it to anything or remove this condition and put
#             # countdown on each frame
#             if j % 10 == 0:
#                 # specify the font and draw the countdown using puttext
#                 font = cv2.FONT_HERSHEY_SIMPLEX
#                 cv2.putText(img, str(j // 10), (250, 250), font, 7,
#                             (255, 255, 255), 10, cv2.LINE_AA)
#             cv2.imshow('a', img)
#             cv2.waitKey(125)
#             j = j - 1

#         else:
#             ret, img = cap.read()
#             # Display the clicked frame for 1 sec.
#             # You can increase time in waitKey also
#             cv2.imshow('a', img)
#             cv2.waitKey(1000)

#             count += 1
#             print(count)
#             # Save the frame
#             if mode == 2:
#                 cv2.imwrite(str(EL)+ "/frame%d.jpg" % count, img)
#             elif mode ==1:
#                 cv2.imwrite(str(PL)+ "/frame%d.jpg" % count, img)
#         # Press Esc to exit

#         # if cv2.waitKey(0):
#         #     break

#         if count == multiexposure_input:
#             # 2 will be equal for two times, only exit after tkaing el and pl
#             if mode == 2:
#                 print("End of PL and EL imaging")
#                 break
#             print("EL imaging")
#             mode = 2
#             count = 0

#         # if cv2.waitKey(25) & 0xFF == ord('q'):
#         #     break

#     cap.release()
#     cv2.destroyAllWindows()
###########################


def PSU(mode):
    #function to change the PSU
    setting = True
    Imaging(mode, setting)


def Imaging(mode, setting):
    if setting:
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

            if mode == 2:
                ret, img = cap.read()
                # Display the clicked frame for 1 sec.
                cv2.waitKey(1000)
                # Save the frame
                cv2.imwrite(str(EL) + "/frame%d.jpg" % count, img)
                mode = 1
                PSU(mode)

            if mode == 1:
                ret, img = cap.read()
                # Display the clicked frame for 1 sec.
                cv2.waitKey(1000)
                # Save the frame
                cv2.imwrite(str(PL) + "/frame%d.jpg" % count, img)
                mode = 2
                PSU(mode)

            # Press Esc to exit

            # if cv2.waitKey(0):
            #     break

            if count == multiexposure_input:
                # 2 will be equal for two times, only exit after tkaing el and pl
                if mode == 2:
                    print("End of PL and EL imaging")
                    break
                print("EL imaging")
                mode = 2
                count = 0

            # if cv2.waitKey(25) & 0xFF == ord('q'):
            #     break

        cap.release()
        cv2.destroyAllWindows()

def read_arduino():
    while 1:
        arduinoData = serialcomm.readline().decode('ascii')
        print(arduinoData)
        #zeroing done
        # if arduinoData == 3:
        #     Imaging()


t1 = threading.Thread(target = read_arduino)
t2 = threading.Thread(target = Imaging)
t1.start()
t2.start()
t1.join
t2.join
#manually pressed button to take image
# while True:
#     ret, frame = cap.read()
#     cv2.imshow('webcam feed', frame)
#     if cv2.waitKey(1) & 0xFF == ord(' '):
#       cv2.imwrite("frame%d.jpg" % count, frame)
#       count +=1
#       if count == multiprocess_input:
#         break
