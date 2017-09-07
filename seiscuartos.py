import entornos_o
from random import choice

__author__ = "athenavianney"

class SeisCuartos(entornos_o.Entorno):
    """
    Clase para un entorno de seis cuartos.
    El estado se define como (robot, A, B, C, D, E, F)
    donde robot puede tener los valores "A", "B", "C", "D", "E", "F"
    Los cuartos pueden tener los valores "limpio", "sucio"

    Las acciónes válidas en el entorno son ("ir_Izq", "ir_Der", "subir", "bajar", "limpiar", "nada").
    Subir se puede solo cuando se encuentra en el piso de abajo, y bajar se puede solo cuando se encuentra arriba

    Los sensores es una tupla (robot, limpio?)
    con la ubicación del robot y el estado de limpieza
    """
    def __init__(self, x0=["A", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]):
        #Por default inicialmente el robot está en A y los cuartos están sucios
        self.x = x0[:]
        self.desempeño = 0
   
    def acción_legal(self, acción):
        if acción in ("ir_Izq", "ir_Der", "subir", "bajar", "limpiar", "nada"):
            robot = self.x[0]
            return (True if (acción == "bajar" and (robot == "A" or robot =="B" or robot == "C")) or
                            (acción == "subir" and (robot == "D" or robot == "E" or robot == "F")) or
                            (acción == "ir_Izq" and (robot != "A" and robot != "D")) or
                            (acción == "ir_Der" and (robot != "C" and robot != "F")) else False)

    def transición(self, acción):
        robot, a, b, c, d, e, f = self.x
        
        if acción is not "nada" or a is "sucio" or b is "sucio" or c is "sucio" or d is "sucio" or e is "sucio" or f is "sucio":
            self.desempeño -= 1

        if acción is "bajar" or acción is "subir":
            self.desempeño -= 1

        if acción is "limpiar":
            self.x[" ABCDEF".find(self.x[0])] = "limpio"
        
        #IZQ
        elif acción is "ir_Izq" and robot == "A":
            self.x[0] = "A"
        elif acción is "ir_Izq" and robot == "B":
            self.x[0] = "A"
        elif acción is "ir_Izq" and robot == "C":
            self.x[0] = "B"
        elif acción is "ir_Izq" and robot == "D":
            self.x[0] = "D"
        elif acción is "ir_Izq" and robot == "E":
            self.x[0] = "D"
        elif acción is "ir_Izq" and robot == "F":
            self.x[0] = "E"

        #DER
        elif acción is "ir_Der" and robot == "A":
            self.x[0] = "B"
        elif acción is "ir_Der" and robot == "B":
            self.x[0] = "C"
        elif acción is "ir_Der" and robot == "C":
            self.x[0] = "C"
        elif acción is "ir_Der" and robot == "D":
            self.x[0] = "E"
        elif acción is "ir_Der" and robot == "E":
            self.x[0] = "F"
        elif acción is "ir_Der" and robot == "F":
            self.x[0] = "F"


        #BAJAR  
        elif acción is "bajar" and robot == "A":
            self.x[0] = "D"
        elif acción is "bajar" and robot == "B":
            self.x[0] = "E"
        elif acción is "bajar" and robot == "C":
            self.x[0] = "F"


        #SUBIR
        elif acción is "subir" and robot == "D":
            self.x[0] = "A"
        elif acción is "subir" and robot == "E":
            self.x[0] = "B"
        elif acción is "subir" and robot == "F":
            self.x[0] = "C"

    def percepción(self):
        return self.x[0], self.x[" ABCDEF".find(self.x[0])]


class AgenteAleatorio(entornos_o.Agente):
    # Un agente que solo regresa una acción al azar entre las acciones legales
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, percepcion):
        return choice(self.acciones)


class AgenteReactivoModeloSeisCuartos(entornos_o.Agente):
    # Un agente reactivo basado en modelo

    def __init__(self):
        # Inicializa el modelo interno en el peor de los casos
        self.modelo = ["A", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]

    def programa(self, percepción):
        robot, situación = percepción

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[" ABCDEF".find(robot)] = situación

        # Decide sobre el modelo interno
        a, b, c, d, e, f = self.modelo[1], self.modelo[2], self.modelo[3], self.modelo[4], self.modelo[5], self.modelo[6]
        return ("nada" if a == b == c == d == e == f == "limpio" else
                "limpiar" if situación == "sucio" else
                "ir_Der" if robot == "A" or robot == "B" else
                "bajar" if robot == "C" else
                "ir_Izq" if robot == "F" or robot == "E" else
                "subir")


def test():
    # Prueba del entorno y los agentes
    print("Prueba del entorno con un agente aleatorio")
    entornos_o.simulador(SeisCuartos(), AgenteAleatorio(["ir_Izq", "ir_Der", "subir", "bajar", "limpiar", "nada"]), 100)
    print("Prueba del entorno con un agente reactivo con modelo")
    entornos_o.simulador(SeisCuartos(), AgenteReactivoModeloSeisCuartos(), 100)


if __name__ == "__main__":
    test()
