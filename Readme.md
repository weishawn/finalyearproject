
1. directory() creates two diretories, one for EL and one for PL to store the captured images used for image stitching later on.

2. Imaging() is the webcam imaging function which has a timer for 5 seconds before taking the image. Will toggle between mode 1 and 2 with 1 being PL and 2 being EL.

3. imagestitching() reads the two created directories and stitch the 9 images up using OpenCV. (Still under testing)

4. Write_PSU(x) and write_thread(x) takes in argument x as the command to the Arduino and PSU. Both of them uses serial communication.

5. PSU(mode) mode 1 is PL, mode 2 is EL, mode 3 is shut off. Simplified PSU function to control Korad PSU. The PL current and voltage will be corrected once we get the lamp source.

6. motor_handshake(), ELPL_handshake(), rest_handshake(), all serves the same purpose of confirming the different signal from arduino.

7. read_thread() created a thread to read and write data into arduio parallelly. The timing and sequence will be controlled by while loops in action(). 

8. In the action(), a start signal of 1 will start the imaging process and the flow is..........

1st cell
Calibration by hitting the left limit switch -> Homing to the first cell -> shut down PSU momentarily before setting and outputting the PL voltage and current -> Arduino controlled relays closes to allow the flow of current into the lamp -> take image after 5 seconds -> shut down PSU momentarily before setting and outputting the EL voltage and current -> Arduino controlled relays closes to allow the flow of current into the panel -> take image after 5 seconds ->

2nd cell
Move the motor -> repeat the "shut down PSU momentarily before setting and outputting the PL voltage and current until the EL image on the second cell is taken.

4th cell
A beep sound to indicate users to move the pane upwards manually. Homing of the motor to the first cell postion but for second row now.

9th cell
FInish the imaging process, outcome would be 9 PL and 9 EL images. Image stitching function is called here and the images are stitched together.


9. The serial communication port and read thread are defined in the main function. When all the proess is completed it is gonna wait for another start signal from the users.

10. Emergency stop is checked after every action and when the stop signal is high, the program quits out of the while loop in the thread and action but still remains inside the main loop, this is to ensure the program does not shut down IMPEL software completely during integration.

#   f i n a l y e a r p r o j e c t  
 #   f i n a l y e a r p r o j e c t  
 #   f i n a l y e a r p r o j e c t  
 