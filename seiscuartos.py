#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SeisCuartos.py.py
------------

Ejemplo de un entorno muy simple y agentes idem

"""

import entornos_o
from random import choice


__author__ = "athenavianney"


class SeisCuartos(entornos_o.Entorno):
    """
    Clase para un entorno de seis cuartos. Muy sencilla solo regrupa métodos.

    El estado se define como (robot, A, B, C, D, E, F)
    donde robot puede tener los valores "A", "B", "C", "D", "E", "F"
    Los cuartos pueden tener los valores "limpio", "sucio"

    Las acciónes válidas en el entorno son ("ir_Izq", "ir_Der", "subir", "bajar", "limpiar", "nada").
    Subir se puede solo cuando se encuentra en el piso de abajo, y bajar se puede solo cuando se encuentra arriba

    Los sensores es una tupla (robot, limpio?)
    con la ubicación del robot y el estado de limpieza

    """
    def __init__(self, x0=["A", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]):
        """
        Por default inicialmente el robot está en A y los dos cuartos
        están sucios

        """
        self.x = x0[:]
        self.desempeño = 0

   
    def acción_legal(self, acción):
        if acción in ("ir_Izq", "ir_Der", "subir", "bajar", "limpiar", "nada"):
            return (True if (acción == "bajar" and (self.x[0] == "A" or self.x[0] =="B" or self.x[0] == "C")) or
                            (acción == "subir" and (self.x[0] == "D" or self.x[0] == "E" or self.x[0] == "F")) or
                            (acción == "ir_Izq" and (self.x[0] != "A" and self.x[0] != "D")) or
                            (acción == "ir_Der" and (self.x[0] != "C" and self.x[0] != "F")) else False)


    def transición(self, acción):
       # if not self.acción_legal(acción):
        #    raise ValueError("La acción no es legal para este estado")

        robot, a, b, c, d, e, f = self.x
        if acción is not "nada" or a is "sucio" or b is "sucio" or c is "sucio" or d is "sucio" or e is "sucio" or f is "sucio":
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
            self.desempeño-=1
        elif acción is "bajar" and robot == "B":
            self.x[0] = "E"
            self.desempeño-=1
        elif acción is "bajar" and robot == "C":
            self.x[0] = "F"
            self.desempeño-=1


        #SUBIR
        elif acción is "subir" and robot == "D":
            self.x[0] = "A"
            self.desempeño-=1
        elif acción is "subir" and robot == "E":
            self.x[0] = "B"
            self.desempeño-=1
        elif acción is "subir" and robot == "F":
            self.x[0] = "C"
            self.desempeño-=1

    def percepción(self):
        return self.x[0], self.x[" ABCDEF".find(self.x[0])]


class AgenteAleatorio(entornos_o.Agente):
    """
    Un agente que solo regresa una acción al azar entre las acciónes legales

    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, percepcion):
        return choice(self.acciones)


"""class AgenteReactivoSeisCuartos(entornos_o.Agente):
    
   # Un agente reactivo simple

    
    def programa(self, percepción):
        robot, situación = percepción
        return ("limpiar" if situación == "sucio" else

                "ir_A" if robot == "B" else "ir_B")
"""

class AgenteReactivoModeloSeisCuartos(entornos_o.Agente):
    """
    Un agente reactivo basado en modelo

    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
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
    """
    Prueba del entorno y los agentes

    """
    print("Prueba del entorno con un agente aleatorio")
    entornos_o.simulador(SeisCuartos(),
                         AgenteAleatorio(["ir_Izq", "ir_Der", "subir", "bajar", "limpiar", "nada"]),
                         100)

    #print("Prueba del entorno con un agente reactivo")
    #entornos_o.simulador(SeisCuartos(), AgenteReactivoSeisCuartos(), 100)

    print("Prueba del entorno con un agente reactivo con modelo")
    entornos_o.simulador(SeisCuartos(), AgenteReactivoModeloSeisCuartos(), 100)


if __name__ == "__main__":
    test()
