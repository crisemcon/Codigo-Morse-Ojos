import cv2
import numpy as np
import dlib
from math import hypot
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import time
import array

font = cv2.FONT_HERSHEY_PLAIN

cap = cv2.VideoCapture(0)
text_disp = np.zeros((50,700), np.uint8)
text_disp[:] = 255

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

start_b = 0.0
start_notb = time.perf_counter()
tiempo_blink = 0.0
tiempo_not_blink = 0.0
w_mode = False #write mode
blink = False
morse = ""
text = ""

while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)
    #Puede usar más de una cara, pero para propósitos de este programa, sólo un usuario debería aparecer en pantallas 
    for face in faces:
        landmarks = predictor(gray, face)

        left_eye_ear = get_EAR([36,37,38,39,40,41], landmarks)
        right_eye_ear = get_EAR([42,43,44,45,46,47], landmarks)
        
        #umbral de cambio entre ojo abierto y ojo cerrado
        #este valor cambia dependiendo de la persona
        ear_threshold = 0.240 #se debe ajustar a la persona, podría ser userfriendly

        #cierra
        if left_eye_ear < ear_threshold and right_eye_ear < ear_threshold: 
            if not blink:
                blink = True
                start_b = time.perf_counter()
                tiempo_blink = 0
                tiempo_not_blink = time.perf_counter() - start_notb
            else:
                continue


            #cv2.putText(frame, "BLINK", (50,50), font, 2, (255,0,0))

        #abre
        if left_eye_ear >= ear_threshold and right_eye_ear >= ear_threshold: 
            if blink:
                blink = False
                tiempo_blink = time.perf_counter() - start_b
                start_notb = time.perf_counter()
            
            if not w_mode and tiempo_blink > 5.0: #Entra en write mode
                w_mode = True 
                tiempo_blink = 0
                print("Write mode ON")
            elif w_mode and tiempo_blink > 5.0: #Sale de write mode
                w_mode = False
                tiempo_blink = 0 
                print("Write mode OFF")


    if(w_mode and not blink and tiempo_blink>0 and tiempo_blink<0.5): #abrio los ojos
        morse=morse+"."
        tiempo_blink = 0
    elif(w_mode and not blink and tiempo_blink>=1.5 and tiempo_blink<3): #abrio los ojos
        morse=morse+"-"
        tiempo_blink = 0
    elif(w_mode and blink and tiempo_not_blink>=3 and tiempo_not_blink<5): #cerró los ojos
        morse=morse+"/"
        tiempo_not_blink=0
    elif(w_mode and blink and tiempo_not_blink>=5): #cerró los ojos
        morse=morse+" "
        tiempo_not_blink=0

    cv2.putText(text_disp,text, (10,30), font, 2, 0, 1)
   
    image = cv2.imread("morse.jpg")
    cv2.imshow("Guía Morse", image)
    cv2.imshow("Camara", frame)
    cv2.imshow("Display de Texto", text_disp)
    print(morse)

    #cerrar programa con tecla "ESC"
    key = cv2.waitKey(1)
    if key == 27:
        break


cap.release()
cv2.destroyAllWindows()