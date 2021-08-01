Para hacer funcionar este programa se deben tener instaladas las librerías de python:
	matplotlib, opencv, dlib

También se debe considerar que en la carpeta en la que se encuentra el código DEBEN estar los siguientes archivos:
	recordar-codigo-morse.png
	shape_predictor_68_face_landmarks.dat

Para ejecutar el código simplemente ingrese en su terminal:
	python main.py

Se abrirán 3 ventanas:
	1. Cámara, donde se marca la identificación de los ojos
	2. Cuadro de texto, donde ira apareciendo la traducción a lenguaje natural de lo escrito en morse
	3. Imagen referencial con el código morse

En la terminal se irá escribiendo los "." y "-" reconocidos por los pestañeos

La traducción de pestañeos a código morse y espacios de separación se basa en tiempo.
Se consideran los tiempos de mantener el ojo abierto (t_open) y de mantener el ojo cerrado (t_close):
	- "." = 0<t_close<0.5
	- "-" = 1.5<t_blink<3
	- separador de letras: 3<t_open<5 
	- separador de palabras(" ") = t_open>5
Para comenzar a escribir, se debe ingresar a "Modo Escritura", para lo cual se deben mantener los ojos cerrados 
por al menos 5 segundos (t_close>=5). Para salir de "Modo Escritura" volver a mantener cerrados por 5 segundos.

Para escapar del programa, presione ESC.