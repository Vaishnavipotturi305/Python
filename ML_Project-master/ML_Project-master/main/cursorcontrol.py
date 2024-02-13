import mediapipe as mp
import cv2
import numpy as np
import uuid
import os
import pyautogui as pyaut
import math

class lap:
    def pos(self):
        return pyaut.position()
    def moveto(self,x,y):
        pyaut.moveTo(x,y)
    def click(self,x,y):
        pyaut.click(x,y)
    def doubleclick(self,x,y):
        pyaut.doubleClick()
    def write(self,data):
        pyaut.write(data)
    def press(self,key):
        pyaut.press(key)
    def drag(self,x,y,duration):
        pyaut.drag(x,y,duration=duration)
    def keydown(self,key):
        pyaut.keyDown(key)
    def keyup(self,key):
        pyaut.keyUp(key)
    def mousedown(self,x,y):
        pyaut.mouseDown(x=x, y=y, button='left')
    def mouseup(self,x,y):
        pyaut.mouseUp(x=x, y=y, button='left')
def dist(point, point1):
    x, y = point
    x1, y1 = point1
    distance = math.sqrt((x1 - x)**2 + (y1 - y)**2)
    return distance
def blinkRatio(landmarks, right_indices, left_indices):
    # Right eyes 
    # horizontal line 
    rh_right = landmarks[right_indices[0]]
    rh_left = landmarks[right_indices[8]]
    # vertical line 
    rv_top = landmarks[right_indices[12]]
    rv_bottom = landmarks[right_indices[4]]
    # draw lines on right eyes 
    # cv.line(img, rh_right, rh_left, utils.GREEN, 2)
    # cv.line(img, rv_top, rv_bottom, utils.WHITE, 2)
    # LEFT_EYE 
    # horizontal line 
    lh_right = landmarks[left_indices[0]]
    lh_left = landmarks[left_indices[8]]
    # vertical line 
    lv_top = landmarks[left_indices[12]]
    lv_bottom = landmarks[left_indices[4]]
    # Finding Distance Right Eye
    rhDistance = dist(rh_right, rh_left)
    rvDistance = dist(rv_top, rv_bottom)
    # Finding Distance Left Eye
    lvDistance = dist(lv_top, lv_bottom)
    lhDistance = dist(lh_right, lh_left)
    # Finding ratio of LEFT and Right Eyes
    reRatio = rhDistance/rvDistance
    leRatio = lhDistance/lvDistance
    ratio = (reRatio+leRatio)/2
    return ratio
mp_d=mp.solutions.drawing_utils
mp_h=mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh
lap=lap()

w=1920
h=1080


cap=cv2.VideoCapture(0)
print(lap.pos())
with mp_h.Hands(min_detection_confidence=.8,min_tracking_confidence=.5) as hands,mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as face_mesh:
    while cap.isOpened():
        r,frame=cap.read()
        image=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        image.flags.writeable=False
        results=hands.process(image)

        results1 = face_mesh.process(image)
        image.flags.writeable=True
        image=cv2.cvtColor(image,cv2.COLOR_RGB2BGR)


        if results.multi_hand_landmarks and results1.multi_face_landmarks:

            for face_landmarks in results1.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_tesselation_style())
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_contours_style())
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_IRISES,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_iris_connections_style())
                fl = []
                for landmarks in face_landmarks.landmark:
                    fl.append([landmarks.x, landmarks.y])
                print(dist(fl[44],fl[47]))

            fingerCount=0
            indexfinger=0
            for num,hand in enumerate(results.multi_hand_landmarks):
                mp_d.draw_landmarks(image,hand,mp_h.HAND_CONNECTIONS)
                handLandmarks = []
                for landmarks in hand.landmark:
                    handLandmarks.append([landmarks.x, landmarks.y])
                # if handLandmarks[4][0] > handLandmarks[3][0]:
                #     fingerCount = fingerCount+1
                if handLandmarks[8][1] < handLandmarks[6][1]:       #Index finger
                    indexfinger=1
                if handLandmarks[12][1] < handLandmarks[10][1]:     #Middle finger
                    fingerCount = fingerCount+1
                if handLandmarks[16][1] < handLandmarks[14][1]:     #Ring finger
                    fingerCount = fingerCount+1
                if handLandmarks[20][1] < handLandmarks[18][1]:     #Pinky
                    fingerCount = fingerCount+1
                if(indexfinger):
                    lap.moveto(1920-(hand.landmark[8].x)*w,(hand.landmark[8].y)*h)
                if(fingerCount==1):
                    lap.click(1920-(hand.landmark[8].x)*w,(hand.landmark[8].y)*h)
                if(fingerCount==2):
                    lap.mousedown(1920-(hand.landmark[8].x)*w,(hand.landmark[8].y)*h)
                else:
                    lap.mouseup(1920-(hand.landmark[8].x)*w,(hand.landmark[8].y)*h)
            print(fingerCount)
        cv2.imshow("video",image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()
