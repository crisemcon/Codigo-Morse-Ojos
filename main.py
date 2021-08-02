import cv2
import numpy as np
import dlib
from math import hypot
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import time
import array
import threading
from threading import Timer

font = cv2.FONT_HERSHEY_PLAIN

cap = cv2.VideoCapture(0)
text_disp = np.zeros((70,1143,3), np.uint8)
text_disp[:] = 255
ear_frame = np.zeros((88,503,3), np.uint8)
ear_frame[:] = 255
speed_frame = np.zeros((88,503,3), np.uint8)
speed_frame[:] = 255


detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

#umbral de cambio entre ojo abierto y ojo cerrado
#este valor cambia dependiendo de la persona
ear_threshold = 0.240 #se debe ajustar a la persona, podría ser userfriendly

#obtiene el punto medio entre dos puntos
def get_midpoint(p1,p2):
    return int((p1.x+p2.x)/2), int((p1.y+p2.y)/2)

def on_change_ear(value):
    return 

def on_change_speed(value):
    return

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

def morse2char(letra):
    if(letra==".-"): letra='a'
    elif(letra=="-..."): letra='b'
    elif(letra=="-.-."): letra='c'
    elif(letra=="-.."): letra='d'
    elif(letra=="."): letra='e'
    elif(letra=="..-."): letra='f'
    elif(letra=="--."): letra='g'
    elif(letra=="...."): letra='h'
    elif(letra==".."): letra='i'
    elif(letra==".---"): letra='j'
    elif(letra=="-.-"): letra='k'
    elif(letra==".-.."): letra='l'
    elif(letra=="--"): letra='m'
    elif(letra=="-."): letra='n'
    elif(letra=="--.--"): letra='ñ'
    elif(letra=="---"): letra='o'
    elif(letra==".--."): letra='p'
    elif(letra=="--.-"): letra='q'
    elif(letra=="._."): letra='r'
    elif(letra=="..."): letra='s'
    elif(letra=="-"): letra='t'
    elif(letra=="..-"): letra='u'
    elif(letra=="...-"): letra='v'
    elif(letra==".--"): letra='w'
    elif(letra=="-..-"): letra='x'
    elif(letra=="-.--"): letra='y'
    elif(letra=="--.."): letra='z'
    else: letra = -1
    return letra

start_b = 0.0
start_notb = time.perf_counter()
tiempo_blink = 0.0
tiempo_not_blink = 0.0
w_mode = False #write mode
blink = False
morse = ""
text = ""
end_l = False #termina letra
tiempo_beep = time.perf_counter()

while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #frame = cv2.resize(frame, (508, 381))
    #print(frame.shape)
    image = cv2.imread("recordar-codigo-morse.png")
    scale_percent = 40 #percent by which the image is resized
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dsize = (width, height)
    output = cv2.resize(image, dsize) #resize image
    if(w_mode):
        cv2.putText(frame, "MODO ESCRITURA", (50,50), font, 2, (255,0,0))
    cv2.putText(frame, "\"ESC\" PARA SALIR", (50,450), font, 2, (0,0,255))
    #cv2.imshow("Camara", frame)
    #cv2.imshow("Guia Morse", output)
    #cv2.imshow("Adjust EAR", ear_frame)
    #cv2.imshow("Adjust Speed", speed_frame)
    #cv2.imshow("Display de Texto", text_disp)
    vertical = np.vstack((output, ear_frame, speed_frame))
    horizontal = np.hstack((vertical, frame))
    final = np.vstack((horizontal, text_disp))
    #height, width, channels = numpy_horizontal.shape
    #print(height,width,channels)
    cv2.imshow("Blinking Morse", final)
    cv2.createTrackbar('EAR Threshold', 'Blinking Morse', 20, 80, on_change_ear)
    cv2.createTrackbar('Speed', 'Blinking Morse', 50, 100, on_change_speed)
    ear_threshold = cv2.getTrackbarPos('EAR Threshold', 'Blinking Morse') / 100
    speed = cv2.getTrackbarPos('Speed', 'Blinking Morse')
    #print(ear_threshold)
    if(w_mode):
        print(morse)

    faces = detector(gray)
    #Puede usar más de una cara, pero para propósitos de este programa, sólo un usuario debería aparecer en pantalla 
    for face in faces:
        landmarks = predictor(gray, face)

        left_eye_ear = get_EAR([36,37,38,39,40,41], landmarks)
        right_eye_ear = get_EAR([42,43,44,45,46,47], landmarks)

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
            
            if not w_mode and tiempo_blink > speed/10: #Entra en write mode
                w_mode = True 
                tiempo_blink = 0
                print("Write mode ON")
            elif w_mode and tiempo_blink > speed/10: #Sale de write mode
                w_mode = False
                morse=""
                tiempo_blink = 0 
                print("Write mode OFF")


    if(w_mode and not blink and tiempo_blink>0 and tiempo_blink<speed/100): #abrio los ojos
        morse=morse+"."
        tiempo_blink = 0
    elif(w_mode and not blink and tiempo_blink>=speed/33.3 and tiempo_blink<speed/16.6): #abrio los ojos
        morse=morse+"-"
        tiempo_blink = 0
    elif(w_mode and blink and tiempo_not_blink>=speed/16.6 and tiempo_not_blink<speed/8.3): #cerró los ojos
        end_l = True #separador de letra
        tiempo_not_blink=0
    elif(w_mode and blink and tiempo_not_blink>=speed/8.3): #cerró los ojos
        end_l = True #separador de palabra
        tiempo_not_blink=0

    if(end_l and len(morse)>0):
        palabra=""
        if(morse[-1]==" "):
            palabra=morse[:-1]
        letra=morse2char(morse)
        if(letra!=-1):
            text=text+letra
            if(morse[-1]==" "):
                text=text+" "
        morse=""
        end_l=False
    
    #print(round(time.perf_counter()-tiempo_beep))
    if(round(time.perf_counter()-tiempo_beep, 1) == round(speed/50, 1)):
        print('\a')
        tiempo_beep = time.perf_counter()

    #cerrar programa con tecla "ESC"
    key = cv2.waitKey(1)
    if key == 27:
        break


cap.release()
cv2.destroyAllWindows()