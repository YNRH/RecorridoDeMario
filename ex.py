
import turtle, math, random
import numpy as np
import time, cv2

#oooooooooo 1. Inicializacion del sistema oooooooooooooo

#---------- Configuracion de la ventana---------
wn = turtle.Screen()                    #Inicializo la ventana para graficar el juego
wn.bgcolor("black")                     #Color de fondo inicial
wn.title("Space Legends")               #Titulo de juego se vizualiza en la ventana
wn.pgpic("fondo4.png")                  #se sobrepone la imagen usandola como fondo

#---------- Dibujo de las formas -------------
turtle.register_shape("enemigo1.gif")   #Icono de naves enemigas
turtle.register_shape("player.gif")     #Icono del jugador
turtle.register_shape("rocket.git")     #Icono para el misil

#---------- Dibujo de los bordes -----------------
border_pen = turtle.Turtle()            #Inicializa el lapiz para el dibujp
border_pen.speed(0)                     #La mayor velocidd de dibujo
border_pen.color("white")               #Seleccionar color de lapiz
border_pen.penup()                      #Sube el lapiz- no dibuja
border_pen.setposition(-300,-300)       #ubica lapiz en posicion inicial
border_pen.pendown()                    #baja el lapiz - dibuja
border_pen.pensize(3)                   #Tamaño del lapiz para el marco
for side in range(4):                   #side-lado=>4 bordes(marco cuadro)
    border_pen.fd(600)                  #dibuja hacia adelante 600px
    border_pen.lt(90)                   #Gira 90° a la izquierda el lapiz
border_pen.hideturtle()                 #oculta el lapiz a medida que dibuja

#----------Dibuja el puntaje en pantalla ---------
score = 0                   #Poner el puntaje inicial en cero
score_pen = turtle.Turtle() #Inicializa el dibujo para el marco
score_pen.speed = 0         #la mayor velocidad 
score_pen.color("white")
score_pen.pendown()
score_pen.setposition(-290,280)
scorestring = "Score: %s"%secore
score_pen.write(scorestring, False, align="left", font=("Arial",14,"normal"))
score_pen.hideturtle()      #Oculta el lapiz

#---------Crear el objeto del jugador ------------
player = turtle.Turtle()
player.color("blue")
player.shape("player.gif")
player.penup()
player.speed(0)
player.setposition(0, -250)             #Selecciona la posicion inicial
player.setheading(90)                   #Posiciona jugador segun angulo 90=norte

playerspeed = 20                        #velocidad de movimiento nave principal

#---------- Empesar a agregar los enemigos en pantalla -------
number_of_enemies = 5                   #Escoge numero de enemigos
enemies = []                            #crear una lista
for i in range(number_of_enemies):
    enemies.append(turtle.Turtle())
for enemy in enemies:
    enemy.color("red")
    enemy.shape("enemie1.gif")          #escoge la img de nave enemigas
    enemy.penup()
    enemy.speed(0)
    x = random.randint(-200, 200)       #
    y = random.randint(100, 250)
    enemy.setposition(x,y)              #selecciona una posicion inicial del enemigo

enemyspeed = 3

#---------crear el objeto del misil ----------
bullet = turtle.Turtle()                #iniciar objeto del misil
bullet.color("yellow")
bullet.shape("rocket.gif")          #escoge la img de nave enemigas
bullet.penup()
bullet.speed(0)
bullet.setheading(90)               #posicionar misill segun angulo 90Norte
bullet.hideturtle()

bulletstate = "ready"               #Estado del misil ready=listo para dispararr---- fire=misil en pantalla
bulletspeed = 20


#ooooooooooooo-- 2. Definicion de funciones --oooooooooooo

#------------Funcion para ajustar el tamaño de la imagen(en opencv) ------
def imge_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    dim = None

#-----------Funcion para cerrar correctamente el juego ------
def closeGame():
    cap.release()
    cv2.destroyAllWindows()
    wn.clear()
    turtle.write("GAME OVER", move=False, align="center", font=("Arial",24,"normal"))
    time.sleep(3)
    wn.delete("all")
    exit()

#--------Funcion para mover la nave a la izquirda -------
def move_left():
    x = player.xcor()
    x -= playerspeed
    if x < -280:
        x = -280
    player.setx(x)

# ---------Funcion para mover la nave a la derecha ---------
def move_right():
    x = player.xcor()
    x -= playerspeed
    if x > -280:
        x = 280
    player.setx(x)

#----------- Funcion para disparar el proyectil-----------
def fire_bullet():
    global bulletstate
    if bulletstate == "ready":
        bulletstate = "fire"
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x,y)
        bullet.showturtle()

def isCollosion(t1,t2):
    distance = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(),2))
    if distance < 25:
        return True
    else:
        return False

turtle.liste()
turtle.onkey(closeGame, "Escape")

#--oooooooooo-- Procesamiento de imagen --ooooooooooooo--
#Detecion de img
cap = cv2.VideoCapture(0)
kernel = np.ones((5,5),np.uint8)
xa = 0

#main game loop
while True:
    frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame3 = cv2.cvtcolor(frame, cv2.COLOR_BGR2YCrCb)

    fy1 = frame3[:,:.1]
    fy2 = frame3[:,:,2]

    ret,bfy1 = cv2.threshold(fy1, 155, 255, cv2, THRESH_BINARY)
    ret,bfy2 = cv2.threshold(fy2, 145, 255, cv2, THRESH_BINARY)
    
    bfy11 = cv2.morphologyEx(bfy1, cv2.MORPH_OPEN, kernel)
    bfy111 = cv2.morphologyEx(bfy1, cv2.MORPH_CLOSE, kernel)
    contoursRed, hierarchy = cv2.findContours(bfy111, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    bfy22 = cv2.morphologyEx(bfy2, cv2.MORPH_OPEN, kernel)
    bfy222 = cv2.morphologyEx(bfy2, cv2.MORPH_CLOSE, kernel)
    contoursRed, hierarchy = cv2.findContours(bfy222, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for c in contoursRed:
        if cv2.contourArea(c) <= 50:
            continue
        x, y, _, _ = cv2.boundingRect(c)
        if (xa-x) > 0:
            move_right()
        elif (xa-x) < 0:
            move_right()
        xa=x

    cv2.drawContours(frame, contoursRed, -1, (0,0,255), 3)
    cv2.drawContours(frame, contoursBlue, -1, (255,0,0), 3)

    if np.count_nonzero(np.sum(bfy2, axis=0)) > 10:
        fire_bullet()

    frame = image_resize(frame, width = 400)
    cv2.imshow("frame", frame)

    if cv2.waitkey(1 & 0xFF == ord('q')):
        break

#--ooooooooooControl de movimiento --oooooooooo
#----------Movimiento de naves enemigas ---------
for enemy in enemies:
    x = enemy.xcor()
    x += enemyspeed
    enemy.setx(x)

    #mover el enemy hacia abajo y de vuelta=cuando llega a paredes
    if((enemy.xcor() > 280) or (enemy.xcor() < -280)):
        for e in enemies:
            y = e.ycor()
            y -= 40
            e.sety(y)

        enemyspeed = -1                 #cambia de direccion de movimiento

    #mira si hay colision entre el enemigo y misill
    if isCollosion(bullet, enemy):
        bullet.hideturtle()
        bulletstate = "ready"
        bullet.setposition(0,-400)
        x = random.randint(-200, 200)
        y = random.randint(100, 250)
        enemy.setposition(x,y)
        score += 10
        scorestring = "Score: %s" %score
        score_pen.clear()
        #escribe el nuevo puntaje de manera con el mismo tamño y letra
        score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))

    #mirar si hay colisiones entre el enemigo y el jugador
    if isCollosion(player, enemy):
        player.hideturtle()
        enemy.hideturtle()
        closeGame()
        break

#------------Movimiento de misil -------------
#movimiento del misil hacia arriba
if bulletstate == "fire":
    y = bullet.ycor()
    y += bulletspeed
    bullet.sety(y)

#si el misil llega al limite superior
if bullet.ycor() > 275:
    bullet.hideturtle()
    bulletstate = "ready"


