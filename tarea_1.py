#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Tarea de desarrollo de entornos y agentes
==========================================

En esta tarea realiza las siguiente acciones:

1.- Desarrolla un entorno similar al de los dos cuartos (el cual se encuentra
    en el módulo doscuartos_o.py), pero con tres cuartos en el primer piso,
    y tres cuartos en el segundo piso.

    El entorno se llamará SeisCuartos

    Las acciones totales serán

    ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]

    La acción de "subir" solo es legal en el piso de abajo (cualquier cuarto),
    y la acción de "bajar" solo es legal en el piso de arriba.

    Las acciones de subir y bajar son mas costosas en término de energía
    que ir a la derecha y a la izquierda, por lo que la función de desempeño
    debe de ser de tener limpios todos los cuartos, con el menor numero de
    acciones posibles, y minimozando subir y bajar en relación a ir a los
    lados.

2.- Diseña un Agente reactivo basado en modelo para este entorno y compara
    su desempeño con un agente aleatorio despues de 100 pasos de simulación.

3.- Al ejemplo original de los dos cuartos, modificalo de manera que el agente
    solo pueda saber en que cuarto se encuentra pero no sabe si está limpio
    o sucio. 

    A este nuevo entorno llamalo DosCuartosCiego

    Diseña un agente racional para este problema, pruebalo y comparalo
    con el agente aleatorio.

4.- Reconsidera el problema original de los dos cuartos, pero ahora modificalo
    para que cuando el agente decida aspirar, el 80% de las veces limpie pero8/
    el 20% (aleatorio) deje sucio el cuarto. Diseña un agente racional
    para este problema, pruebalo y comparalo con el agente aleatorio.

    A este entorno llamalo DosCuartosEstocástico

Todos los incisos tienen un valor de 25 puntos sobre la calificación de
la tarea.

"""
__author__ = "AthenaVianney"

import entornos_o
from random import choice

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


class DosCuartosCiego(entornos_o.Entorno):
    def __init__(self, x0=["A", "sucio", "sucio"]):
        # Por default inicialmente el robot está en A y los dos cuartos están sucios
        self.x = x0[:]
        self.desempeño = 0

    def acción_legal(self, acción):
        return acción in ("ir_A", "ir_B", "limpiar", "nada")

    def transición(self, acción):
        if not self.acción_legal(acción):
            raise ValueError("La acción no es legal para este estado")

        robot, a, b = self.x
        if acción is not "nada" or a is "sucio" or b is "sucio":
            self.desempeño -= 1
        if acción is "limpiar":
            self.x[" AB".find(self.x[0])] = "limpio"
        elif acción is "ir_A":
            self.x[0] = "A"
        elif acción is "ir_B":
            self.x[0] = "B"

    def percepción(self):
        return self.x[0], self.x[" AB".find(self.x[0])]


class AgenteRacionalDoscuartos(entornos_o.Agente):
    # Un agente Racional simple
    def __init__(self):
        self.modelo = ["A", "sucio", "sucio"]

    def programa(self, percepción):
        robot, situación = percepción

        if not "sucio" in self.modelo:
            return "nada"

        situación = self.modelo[" AB".find(robot)]
        self.modelo[" AB".find(robot)] = "limpio"

        return ("limpiar" if situación == "sucio" else
                "ir_A" if robot == "B" else "ir_B")


class DosCuartosEstocastico(entornos_o.Entorno):

    def __init__(self, x0=["A", "sucio", "sucio"]):
        # Por default inicialmente el robot está en A y los dos cuartos están sucios
        self.x = x0[:]
        self.desempeño = 0

    def acción_legal(self, acción):
        return acción in ("ir_A", "ir_B", "limpiar", "nada")

    def transición(self, acción):
        if not self.acción_legal(acción):
            raise ValueError("La acción no es legal para este estado")

        proba = choice(range(100))
        robot, a, b = self.x

        if acción is not "nada" or a is "sucio" or b is "sucio":
            self.desempeño -= 1
        if acción is "limpiar" and proba > 80:
            self.x[" AB".find(self.x[0])] = "limpio" 
        elif acción is "ir_A":
            self.x[0] = "A"
        elif acción is "ir_B":
            self.x[0] = "B"

    def percepción(self):
        return self.x[0], self.x[" AB".find(self.x[0])]


class AgenteRacionalDosCuartosEstocastico(entornos_o.Agente):
    # Un agente Racional simple
    def __init__(self):
    # Inicializa el modelo interno en el peor de los casos
      self.modelo = ["A", "sucio", "sucio"]
    
    def programa(self, percepción):
        robot, situación = percepción

        self.modelo[0] = robot
        self.modelo[" AB".find(robot)] = situación

        a, b = self.modelo[1], self.modelo[2]
        return ("nada" if a == b == "limpio" else
                "limpiar" if situación == "sucio" else
                "ir_A" if robot == "B" else "ir_B")


def test_seiscuartos():
    # Prueba del entorno y los agentes
    print("Prueba del entorno con un agente aleatorio")
    entornos_o.simulador(SeisCuartos(), AgenteAleatorio(["ir_Izq", "ir_Der", "subir", "bajar", "limpiar", "nada"]), 100)
    print("Prueba del entorno con un agente reactivo con modelo")
    entornos_o.simulador(SeisCuartos(), AgenteReactivoModeloSeisCuartos(), 100)


def test_cuartociego():
    # Prueba del entorno y los agentes
    print ("Prueba ciegas")
    entornos_o.simulador(DosCuartosCiego(), AgenteRacionalDoscuartos(), 100)


def test_doscuartosestocastico():
    # Prueba del entorno y los agentes
    print("Prueba del entorno con un agente aleatorio")
    entornos_o.simulador(DosCuartosEstocastico(), AgenteAleatorio(["ir_A", "ir_B", "limpiar", "nada"]), 100)

    print("Prueba del entorno con un agente Racional")
    entornos_o.simulador(DosCuartosEstocastico(), AgenteRacionalDosCuartosEstocastico(), 100)
 

if __name__ == "__main__":
    test_seiscuartos()
    test_cuartociego()
    test_doscuartosestocastico()

