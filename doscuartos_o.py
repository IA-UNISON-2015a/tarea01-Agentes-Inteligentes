#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tarea de desarrollo de entornos y agentes
==========================================

En esta tarea realiza las siguiente acciones:

3.- Al ejemplo original de los dos cuartos, modificalo de manera que el agente
    solo pueda saber en que cuarto se encuentra pero no sabe si está limpio
    o sucio.

    A este nuevo entorno llamalo DosCuartosCiego

    Diseña un agente racional para este problema, pruebalo y comparalo
    con el agente aleatorio.

4.- Reconsidera el problema original de los dos cuartos, pero ahora modificalo
    para que cuando el agente decida aspirar, el 80% de las veces limpie pero
    el 20% (aleatorio) deje sucio el cuarto. Diseña un agente racional
    para este problema, pruebalo y comparalo con el agente aleatorio.

    A este entorno llamalo DosCuartosEstocástico
"""

"""
doscuartos.py.py
------------
Ejemplo de un entorno muy simple y agentes idem

"""

import entornos_o
from random import choice

__author__ = 'patriciaquiroz'

import random

class DosCuartos(entornos_o.Entorno):
    """
    Clase para un entorno de dos cuartos. Muy sencilla solo regrupa métodos.

    El estado se define como (robot, A, B)
    donde robot puede tener los valores "A", "B"
    A y B pueden tener los valores "limpio", "sucio"

    Las acciones válidas en el entorno son ("ir_A", "ir_B", "limpiar", "nada").
    Todas las acciones son válidas en todos los estados.

    Los sensores es una tupla (robot, limpio?)
    con la ubicación del robot y el estado de limpieza (donde se encuentra el robot).
    """

    def __init__(self, x0=["A", "sucio", "sucio"]):
        """
        Por default inicialmente el robot está en A y los dos cuartos
        están sucios
        """
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


class AgenteAleatorio(entornos_o.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales

    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, percepcion):
        return choice(self.acciones)


class AgenteDoscuartosCiegos(entornos_o.Agente):
    """
    Un agente racional donde el robot no sabe si los cuartos estan limpios o sucios, pero en que cuarto se encuentra.
    Como este no sabe si esta un cuarto sucio, por default pensara que todos los cuartos estan sucios.
    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos
        """
        self.modelo = ['A', 'sucio', 'sucio']

    def programa(self, percepción):
        robot, situación = percepción

        # Actualiza el modelo interno
        self.modelo[0] = robot

        # Decide sobre el modelo interno
        a, b = self.modelo[1], self.modelo[2]

        if a == 'limpio' and b == 'limpio':
            aux = 'nada'
        elif robot == 'A':
            if a=='sucio':
                aux='limpiar'
                self.modelo[1]='limpio' #Se actualiza la situacion del modelo para el cuarto A
            else:
                aux='ir_B'
        elif robot == 'B':
            if b=='sucio':
                aux='limpiar'
                self.modelo[2]='limpio' #Se actualiza la situacion del modelo para el cuarto B
            else:
                aux='ir_A'
        return(aux)

class AgenteDosCuartosEstocastico:
    """
    El agente limpia el 80% de las veces, pero el 20% (aleatorio) deja sucio el cuarto.
    """

    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos
        """
        self.modelo = ['A', 'sucio', 'sucio']

    def programa(self, percepción):
        robot, situación = percepción

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[' AB'.find(robot)] = situación

        # Decide sobre el modelo interno
        a, b = self.modelo[1], self.modelo[2]

        if a==b=='limpio':
            aux='nada'
        elif situación=='sucio':
            aux=self.limpiezaEst()
        elif robot=='B':
            aux='ir_A'
        elif robot=='A':
            aux='ir_B'
        return aux

    def limpiezaEst(self):
        return ('limpiar' if random.random() <=0.8 else 'nada')


def test():
    """
    Prueba del entorno y los agentes

    """
    print("Prueba del entorno con un agente aleatorio")
    entornos_o.simulador(DosCuartos(), AgenteAleatorio(['ir_A', 'ir_B', 'limpiar', 'nada']), 20)

    print("Prueba del entorno con un agente ciego")
    entornos_o.simulador(DosCuartos(), AgenteDoscuartosCiegos(), 20)


if __name__ == "__main__":
    test()
    e = DosCuartos()