from random import choice

#Se activa cuando presionas algún botón: True o False
global limpiando

#Es el arreglo general: Guarda la acción a realizar, la situación actual, y la cantidad de acciones o pasos que ha realizado
global fila

#Es el arreglo dentro del arreglo fila: Representa la situación :v 
#Guarda: (la posición del agente /A ó B/, el estado de A /limpio ó sucio/, el estado de B /limpio ó sucio/)
global situacion

#Es la cantidad de iteraciones a realizar
global num

#Cantidad de pasos totales: Si realiza una acción se incrementa en 1, sino se mantiene
global c

#Agente inteligente (Aleatorio, reactivo, reactivo basado en modelos)
global agente

#(Coordenadas de los botones)
global b1x, b2x, b3x, b1y, b2y, b3y

#Imagenes a cargar
global aspiradora, basura, cuarto


#Fúncion que se va ejecutar sólo una vez cuando inicie el juego
def setup():
    global b1x, b2x, b3x, b1y, b2y, b3y
    global limpiando, situacion, num, fila, c, basura, aspiradora
    
    #Tamaño de la ventana
    size(600,450)
    
    limpiando       = False
    situacion       = ['A', 'sucio', 'sucio']
    fila            = ["nada", situacion, '0']
    num             = 50
    c               = 0
    b1y = b2y = b3y = 370
    b1x             = width/4
    b2x             = width/2
    b3x             = width/2 + width/4
    aspiradora      = loadImage("assets/robot.png")
    basura          = loadImage("assets/suciedad.png")


#Funcion que se dibuja repetidamente, termina y se vuelve a dibujar
def draw():
    global limpiando, num, c, agente, situacion, fila
    
    #Dibujar los botones
    fill(255)
    textAlign(CENTER, CENTER)
    boton1()
    boton2()
    boton3()
    
    #Dibujar los cuartos
    for x in range(0,2):
        rect(x*300, 10, 300, 300)
    
    #Poner nombre a los cuartos
    textSize(40)
    fill(0)
    text("A", width/4, 30)
    text("B", width-width/4, 30)
    fill(255)
    
    #Iniciar el simulador
    if limpiando:
        if num>=1:
            if num == 50:
                print("\nSimulación, iniciando en el estado" + 
                      str(situacion) + "\n")
                print('Acción'.center(15) +
                    'Siguente estado'.center(25) +
                    'Costo'.center(15))
                print('_' * (15 + 25 + 15))
                delay(500)
            
            simulador(DosCuartos(), agente)
            
            a, s_n, costo = fila
            #Imprimir la fila
            print(str(a).center(15) +
                        str(s_n).center(25) +
                        str(costo).rjust(12))
            
            if num==1:
                print('_' * (15 + 25 + 15) + '\n\n')
            
            num = num-1
        else:
            limpiando = False
            num       = 50
            c         = 0
    else:
        #Dibujar el estado inicial
        escenario(fila)


#Abstractamente indica que cosa hacer con el cuarto.
class DosCuartos():
    def accion_legal(self, accion):
        return accion in ("ir_A", "ir_B", "limpiar", "nada")

    def transicion(self, estado, accion):
        robot, a, b = estado
        c_local = 0 if a == b == "limpio" and accion == "nada" else 1

        if a == "nada":
            return (estado, c_local)
        else:
            if accion == "ir_A":
                return (("A", a, b), c_local)
            else:
                if accion == "ir_B":
                    return (("B", a, b), c_local)
                else:
                    if robot == "A":
                        return ((robot, "limpio", b), c_local)
                    else:
                        return ((robot, a, "limpio"), c_local)

    def percepcion(self, estado):
        return estado[0], estado[" AB".find(estado[0])]


#AGENTE ALEATORIO
class AgenteAleatorio():
    #Constructor de la clase Agente Aleatorio
    def __init__(self, acciones):
        self.acciones = acciones

    #Escoje una accion aleatoriamente, no evalua si ya esta limpio o no
    def programa(self, _):
        return choice(self.acciones)


#AGENTE REACTIVO
class AgenteReactivoDoscuartos():
    def programa(self, percepcion):
        robot, situacion = percepcion
        return ('limpiar' if situacion == 'sucio' else # Si esta sucio va a retonar limpiar sino, compara si robot es B, va al A; si no va al  B;
                'ir_A' if robot == 'B' else 'ir_B')


#AGENTE REACTIVO BASADO EN MODELOS
class AgenteReactivoModeloDosCuartos():
    def __init__(self):
        self.modelo = ['A', 'sucio', 'sucio']

    def programa(self, percepcion):
        robot, situacion = percepcion

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[' AB'.find(robot)] = situacion

        # Decide sobre el modelo interno
        a, b = self.modelo[1], self.modelo[2]
        return ('nada' if a == b == 'limpio' else
                'limpiar' if situacion == 'sucio' else
                'ir_A' if robot == 'B' else 'ir_B')


#Le manda el estado actual al agente
#Esta función es la que hace posbile nuestro programa.
def simulador(entorno, agente):
    global fila, situacion, c
    a = agente.programa(entorno.percepcion(situacion))
    if not entorno.accion_legal(a):
        raise ValueError("Error en el agente, ofrece una accion no legal")
    situacion, c_local = entorno.transicion(situacion, a) #Retonar la nueva situacion y el paso que ha dado
    
    c = c + c_local
    fila = [a, situacion, c]
    
    escenario(fila)


def escenario(estado):
    global basura, aspiradora
    redraw()
    imageMode(CENTER)
    acc, sit, c = estado
    robot, a, b = sit
    if acc == "limpiar":
        if robot == "A":
            image(aspiradora, width/4, 160, 100, 100)
        else:
            image(aspiradora, width/2+width/4, 160, 100, 100)
    else:
        if robot == "A":
            image(aspiradora, width/10, 160, 100, 100)
        else:
            image(aspiradora, width/2+width/10, 160, 100, 100)
    
    if a == "sucio":
        image(basura, width/4, 160, 100, 100)
    if b == "sucio":
        image(basura, width - width/4, 160, 100, 100)
    delay(50)
    
    imageMode(CORNER)


#Funcion propia del Processing que se activa cada vez que se presione un click.
def mousePressed():
    global b1x, b2x, b3x, b1y, b2y, b3y
    global limpiando, agente, situacion
    #Mousex, Mousey =Psicion del mouse
    if mouseX > b1x-70 and mouseY > b1y-25 and  mouseX < b1x+70 and mouseY < b1y+25:
        #Lo vuelve a dejar en Sucio,sucio para que el otro agente que quiera inicializarse reconozca que esta sucio, sucio.
        situacion = ['A', 'sucio', 'sucio']
        fill(100)
        boton1()
        print("Prueba del entorno con un agente aleatorio")
        agente    = AgenteAleatorio(['ir_A', 'ir_B', 'limpiar', 'nada'])
        limpiando = True
        
    if mouseX > b2x-70 and mouseY > b2y-25 and  mouseX < b2x+70 and mouseY < b2y+25:
        #Lo vuelve a dejar en Sucio,sucio para que el otro agente que quiera inicializarse reconozca que esta sucio, sucio.
        situacion = ['A', 'sucio', 'sucio']
        fill(100)
        boton2()
        print("Prueba del entorno con un agente reactivo")
        agente    = AgenteReactivoDoscuartos()
        limpiando = True
        
    if mouseX > b3x-70 and mouseY > b3y-25 and  mouseX < b3x+70 and mouseY < b3y+25:
        #Lo vuelve a dejar en Sucio,sucio para que el otro agente que quiera inicializarse reconozca que esta sucio, sucio.
        situacion = ['A', 'sucio', 'sucio']
        fill(100)
        boton3()
        print("Prueba del entorno con un agente reactivo con modelo")
        agente    = AgenteReactivoModeloDosCuartos()
        limpiando = True

def boton1():
    global b1x, b1y
    rectMode(CENTER)
    rect(b1x, b1y, 140, 50)
    delay(25)
    fill(0)
    textSize(10)
    text ("AGENTE ALEATORIO SIMPLE",b1x,b1y)
    fill(255)
    rectMode(CORNER)
    
def boton2():
    global b2x, b2y
    rectMode(CENTER)
    rect(b2x, b2y, 140, 50)
    delay(25)
    fill(0)
    textSize(10)
    text ("AGENTE REACTIVO SIMPLE",b2x,b2y)
    fill(255)
    rectMode(CORNER)

def boton3():
    global b3x, b3y
    rectMode(CENTER)
    rect(b3x, b3y, 140, 50)
    delay(25)
    fill(0)
    textSize(10)
    text ("AGENTE REACTIVO",b3x,b3y-5)
    text("BASADO EN MODELOS",b3x,b3y+5)
    fill(255)
    rectMode(CORNER)
