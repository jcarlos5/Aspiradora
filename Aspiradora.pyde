from random import choice

global play
global recorrido
global fila
global situacion
global num
global c
global agente

global b1x, b2x, b3x, b1y, b2y, b3y

def setup():
    global b1x, b2x, b3x, b1y, b2y, b3y
    global play, situacion, num, fila, c
    size(600,450)
    play = False
    situacion = ['A', 'sucio', 'sucio']
    fila = ['-', "Inicio", situacion, '-']
    num = 100
    c = 0
    b1y = b2y = b3y = 350
    b1x = 50
    b2x = 200
    b3x = 350

def draw():
    global b1x, b2x, b3x, b1y, b2y, b3y
    global play, recorrido, num, c, agente, situacion
    rect(b1x, b1y, 100, 50)
    rect(b2x, b2y, 100, 50)
    rect(b3x, b3y, 100, 50)
    for x in range(0,2):
        rect(x*300, 10, 300, 300)
    if play:
        if num>=1:
            simulador(DosCuartos(), agente)
            print fila
            num = num-1
        else:
            play = False
            num = 100
            c=0
            situacion = ['A', 'sucio', 'sucio']
    
    

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


class AgenteAleatorio():
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, _):
        return choice(self.acciones)


class AgenteReactivoDoscuartos():
    def programa(self, percepcion):
        robot, situacion = percepcion
        return ('limpiar' if situacion == 'sucio' else
                'ir_A' if robot == 'B' else 'ir_B')


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

def prueba_agente(agente):
    global recorrido
    recorrido = simulador(
            DosCuartos(),
            agente
        )

def simulador(entorno, agente):
    global recorrido, fila, situacion, c
    a = agente.programa(entorno.percepcion(situacion))
    if not entorno.accion_legal(a):
        raise ValueError("Error en el agente, ofrece una accion no legal")
    situacion, c_local = entorno.transicion(situacion, a)
    
    c = c + c_local
    
    fila = [(a, situacion, c)]


def mousePressed():
    global b1x, b2x, b3x, b1y, b2y, b3y
    global play, agente
    if mouseX > b1x and mouseY > b1y and  mouseX < b1x+100 and mouseY < b1y+50:
        print("Prueba del entorno con un agente aleatorio")
        agente = AgenteAleatorio(['ir_A', 'ir_B', 'limpiar', 'nada'])
        play = True
    if mouseX > b2x and mouseY > b2y and  mouseX < b2x+100 and mouseY < b2y+50:
        print("Prueba del entorno con un agente reactivo")
        agente = AgenteReactivoDoscuartos()
        play = True
    if mouseX > b3x and mouseY > b3y and  mouseX < b3x+100 and mouseY < b3y+50:
        print("Prueba del entorno con un agente reactivo con modelo")
        agente = AgenteReactivoModeloDosCuartos()
        play = True
    

    
