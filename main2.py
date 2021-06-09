import cv2
import numpy as np
import dlib
from math import hypot
import time
import array

font = cv2.FONT_HERSHEY_PLAIN

cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

#obtiene el punto medio entre dos puntos
def get_midpoint(p1,p2):
    return int((p1.x+p2.x)/2), int((p1.y+p2.y)/2)

#obtiene el EAR(relacion de aspecto del ojo) de un ojo
def get_EAR(eye_points, facial_landmarks):
    left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
    right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
    top_point = get_midpoint(facial_landmarks.part(eye_points[1]),facial_landmarks.part(eye_points[2]))
    bottom_point = get_midpoint(facial_landmarks.part(eye_points[5]),facial_landmarks.part(eye_points[4]))

    hor_line = cv2.line(frame, left_point, right_point, (0,255,0), 1)
    ver_line = cv2.line(frame, top_point, bottom_point, (0,255,0), 1)

    ver_line_length = hypot((top_point[0] - bottom_point[0]), (top_point[1] - bottom_point[1]))
    hor_line_length = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
        
    ear = ver_line_length/hor_line_length
    return ear

start = time.perf_counter()
end = time.perf_counter()
arr = array.array('u')

#pestaeñeos iniciales

while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)
    for face in faces:
        landmarks = predictor(gray, face)

        left_eye_ear = get_EAR([36,37,38,39,40,41], landmarks)
        right_eye_ear = get_EAR([42,43,44,45,46,47], landmarks)
        
        #umbral de cambio entre ojo abierto y ojo cerrado
        #este valor cambia dependiendo de la persona
        ear_threshold = 0.240 #se debe ajustar a la persona 
        #podría ser userfriendly

        print(left_eye_ear)
        blink = False
        start = time.perf_counter()
        if left_eye_ear < ear_threshold and right_eye_ear < ear_threshold: #cierra ## DEBERÍA SER WHILE
            blink = True
            #cv2.putText(frame, "BLINK", (50,50), font, 2, (255,0,0))
            #cv2.putText(frame, "LEFT CLOSED", (50,50), font, 2, (0,255,0))
            #cv2.putText(frame, "RIGHT CLOSED", (350,50), font, 2, (0,255,0)) 
        end = time.perf_counter()
       
        if(end-start<0.5 and blink):
        	arr.append('.')
        elif(end-start<1.5 and blink):
        	arr.append('-')


            


    cv2.imshow("Frame", frame)

    #cerrar programa con tecla "ESC"
    key = cv2.waitKey(1)
    if key == 27:
        break

    print(arr)

cap.release()
cv2.destroyAllWindows()
