import cv2
import numpy as np
# print("Before importing autopy")
import autopy                     #For mouse controls
# print("After importing autopy")
import HandTrackingModule as htm
# print("hand")
import time
# print("time")
import math
# print("math")
from ctypes import cast, POINTER
# print("ctypes")
from comtypes import CLSCTX_ALL
# print("comtypes")
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
# print("pycaw")
import mouse as m
import pyautogui
# print("mouse")
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from tkinter import *
import os
# class GestureController:
#     gc_mode = False

#     @classmethod
#     def start_recognition(cls):
#         cls.gc_mode = True

#     @classmethod
#     def stop_recognition(cls):
#         cls.gc_mode = False
# Create the main window
root = Tk()
root.title("Hand Gesture Control")
# gesture_controller = GestureController()
def show_splash_screen():
    splash_img = cv2.imread("splashimage.jpg")  # Replace with the path to your splash image
    cv2.imshow("Splash Screen", splash_img)
    cv2.waitKey(1000)  # Display the splash screen for 3 seconds (adjust as needed)
    cv2.destroyWindow("Splash Screen") #close the program
# Show the splash screen when the program starts
show_splash_screen()
devices = AudioUtilities.GetSpeakers()
# print("device",devices)
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
# print("interfaces",interface)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# print("volume",volume)
volRange = volume.GetVolumeRange()
# print("volrange",volRange)
minVol = volRange[0]
maxVol = volRange[1]
wCam, hCam = 640, 480
frameR = 2
smoothening = 5
plocX, plocY = 0, 0
clocX, clocY = 0, 0
cap = cv2.VideoCapture(0)
print("Inside AiVirtualMouseProject.py")
if not cap.isOpened():
    print("Error: Unable to open the camera.")
    exit()
print("cap",cap)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
cTime = 0
try:
    detector = htm.HandDetector(maxHands=1, detectionCon=0.6)
    # print("detector",detector)
except Exception as e:
    print("Error initializing HandDetector:", e)
wScr, hScr = autopy.screen.size()
# Add the resizeWindow line here
cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Image", wCam, hCam)
#hScr -= 25
#print(wScr, hScr)
dragging = False
drag_start_position = (0, 0)
prev_tab_position = 0
tab_switch_threshold = 50
cooldown_time = 5  # Set the cooldown time in seconds
last_shutdown_time = time.time()
while True:
    # print("entered while block")
    success, img = cap.read()
    # print("after reading frame")
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    if len(lmList)!= 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        #print(x1, y1, x2, y2)
        fingers = detector.fingersUp()
       # print(fingers)
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
        mid_x = (x1 + x2) // 2
          # Detect a swipe by checking the horizontal movement
        # if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
        #     mid_x = (x1 + x2) // 2  # Calculate mid_x here
        #     if mid_x > prev_tab_position + tab_switch_threshold:
        # # Swipe to the right, switch to the next tab or application
        #         pyautogui.hotkey('ctrl', 'tab')  # This simulates pressing Ctrl + Tab
        #         print("Swipe Right - Switch to Next Tab/App")

        #     elif mid_x < prev_tab_position - tab_switch_threshold:
        #         pyautogui.hotkey('ctrl', 'shift', 'tab') 
        #         print("Swipe Left - Switch to Previous Tab/App")
        #     else:
        #         pyautogui.hotkey('alt','tab')
        #         print("next tab")

            # prev_tab_position = mid_x
        if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
            mid_x = (x1 + x2) // 2  
            delta_x = mid_x - prev_tab_position

            if delta_x > tab_switch_threshold:
               
                pyautogui.hotkey('alt', 'tab')  
                print("Swipe Right - Switch to Next App")

            elif delta_x < -tab_switch_threshold:
             
                pyautogui.hotkey('alt', 'shift', 'tab')  
                print("Swipe Left - Switch to Previous App")

            prev_tab_position = mid_x
        if fingers[1] == 0:
            current_time = time.time()

        # Check if the cooldown period has passed since the last shutdown
            if current_time - last_shutdown_time > cooldown_time:
                # Initiate shutdown using pyautogui
            
                # pyautogui.hotkey('winleft', 'd')  
                # pyautogui.hotkey('winleft', 'x')  
                # pyautogui.press('u')  
                # pyautogui.press('u')
                print("Initiating system sleep...")
                pyautogui.hotkey('winleft', 'x')  # This opens the Windows Mobility Center
                pyautogui.press('s')  
                
                last_shutdown_time = current_time  # Update the last shutdown time
        if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
            x3 = np.interp(x1, (frameR, wCam-frameR), (0,wScr))
            y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))
            clocX = ( plocX + (x3 - plocX) / smoothening )
            clocY = ( plocY + (y3 - plocY) / smoothening )
            try:
                autopy.mouse.move(wScr-clocX, clocY)
                print(wScr-clocX, clocY)
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                plocX, plocY = clocX, clocY
            except : pass
        
        if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
            length, img, lineInfo = detector.findDistance(8, 12, img)
            print(length)
            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()
                print("Click")
                cv2.putText(img, "Left Click", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        if fingers[0] == 1 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
            # autopy.mouse.toggle(True, None) 
             pyautogui.mouseDown(button='right')
             pyautogui.mouseUp(button='right')
             print("Right Click")
             cv2.putText(img, "Right Click", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        # if fingers[0] == 1 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
        #     # Start dragging when the thumb and pinky are extended
        #     dragging = True
        #     drag_start_position = (lmList[4][1], lmList[4][2])  # Use the pinky finger for drag start

        # elif dragging and fingers[0] == 1 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
        #     # Simulate dragging by moving the mouse based on hand movement
        #     drag_current_position = (lmList[4][1], lmList[4][2])  # Use the pinky finger for drag
        #     drag_dx = drag_current_position[0] - drag_start_position[0]
        #     drag_dy = drag_current_position[1] - drag_start_position[1]

        #     autopy.mouse.move(drag_dx, drag_dy)
        #     print("Dragging:", drag_dx, drag_dy)

        # elif dragging and fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
        #     # Release gesture to complete the drop when all fingers are down
        #     dragging = False
        #     print("Drop")

        # if (any(fingers[:2]) and any(fingers[2:])==False):
        #     print("Volume")
        # Add this inside the while loop
        # if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
        #     if plocX == clocX and plocY == clocY:
        #         autopy.mouse.click(autopy.mouse.Button.LEFT, 2)  # 2 clicks for a double click
        #         print("Double Click")

        if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
            indxpos, indypos = lmList[20][1], lmList[20][2]
            thumbxpos, thumbypos = lmList[4][1], lmList[4][2]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            length = math.hypot(x2 - x1, y2 - y1)
            print("length:", length)
            cv2.putText(img, "Move", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

            # Adjust volume range and smoothing factor
            vol = np.interp(length, [50, 250], [0, 1])
            vol = np.clip(vol, minVol, maxVol) 
            print("vol",vol)
            vol = vol * 0.7 + volume.GetMasterVolumeLevelScalar() * 0.3  # Smoothing

            # volume.SetMasterVolumeLevelScalar(vol, None)
            volBar = np.interp(length, [50, 250], [400, 150])
            volPer = np.interp(length, [50, 250], [0, 100])

            if length < 50:
                cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
            print("VOLUME:", vol)
            cv2.putText(img, "Volume", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)


    try:
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        # cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    except:
        pass
    cv2.imshow("Image", img)
    cv2.waitKey(1)
