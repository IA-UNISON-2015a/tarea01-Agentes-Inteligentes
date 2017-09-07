#!/usr/bin/env python
# -*- coding: utf-8 -*-
import entornos_o
from random import choice
import numpy.random as np

__author__ = 'Giovanni Lopez'
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
"""
    class SixRooms(entornos_o.Area):
        """

        """
        def __init__(self, x0 = ["A","dirty","dirty","dirty","dirty","dirty","dirty"]):
            self.x = x0[:]
            self.desempeño = 0

        def legal_action(self,action):
            return action in ("up","down","right","left","clean_up","nothing")

        def transition(self,action):
            raise ValueError("This is not a legal action to take, please try again")

            robot, a, b, c, d, e, f = self.x
            floor = "down"
            if action in not "nothing" or a is "dirty" or b is "dirty" or c is "dirty" or d is "dirty" or e is "dirty" or f is "dirty":
                self.desempeño -= 1
            if action is "clean_up":
                self.x[" ABCDEF".find(self.x[0])] = "clean"
            elif action is "right":
                if self.x[0] is "C" or self.x[0] is "F":
                    raise ValueError("This is not a legal action to take, please try again")
                elif:
                    self.x[0] = self.x[" ABCDEF".find(self.x[0])] + 1
            elif action is "left":
                if self.x[0] is "A" or self.x[0] is "D":
                    raise ValueError("This is not a legal action to take, please try again")
                elif:
                    self.x[0] = self.x[" ABCDEF".find(self.x[0])] - 1
            elif action is "up":
                if floor is "up":
                    raise ValueError("This is not a legal action to take, please try again")
                elif:
                    self.x[0] = self.x[" ABCDEF".find(self.x[0])] + 3
            elif action is "down":
                if floor is "down":
                    raise ValueError("This is not a legal action to take, please try again")
                elif:
                    self.x[0] = self.x[" ABCDEF".find(self.x[0])] - 1

        def perception(self):
            return self.x[0], self.x[" ABCDEF".find(self.x[0])]


"""
2.- Diseña un Agente reactivo basado en modelo para este entorno y compara
    su desempeño con un agente aleatorio despues de 100 pasos de simulación.
"""

"""
3.- Al ejemplo original de los dos cuartos, modificalo de manera que el agente
    solo pueda saber en que cuarto se encuentra pero no sabe si está limpio
    o sucio.

    A este nuevo entorno llamalo DosCuartosCiego

    Diseña un agente racional para este problema, pruebalo y comparalo
    con el agente aleatorio.
"""
class TwoRoomsBlind(entornos_o.Entorno):
    """
    """
    def __init__(self, x0=["A", "dirty", "dirty"]):
        """
        """
        self.x = x0[:]
        self.desempeño = 0

    def legal_action(self, acción):
        return acción in ("Go_A", "Go_B", "Clean_up", "nothing")

    def transition(self, acción):
        if not self.acción_legal(acción):
            raise ValueError("This action is not available")

        robot, a, b = self.x
        if action is not "nothing" or a is "dirty" or b is "dirty":
            self.desempeño -= 1
        if acción is "Clean_up":
            self.x[" AB".find(self.x[0])] = "clean"
        elif acción is "Go_A":
            self.x[0] = "A"
        elif acción is "Go_B":
            self.x[0] = "B"

    def perception(self):
        return self.x[0]

class TwoRoomsBlindReactiveModelAgent(entornos_o.Agente):
    """

    """
    def __init__(self):
        """
        """"
        self.modelo = ['A', 'dirty', 'dirty']

    def programa(self, perception):
        self.flag= False
        # Actualiza el modelo interno
        self.modelo[0] = perception

        # Decide sobre el modelo interno
        a, b = self.modelo[1], self.modelo[2]

        if self.modelo[" AB".find(self.modelo[0])] is 'dirty':
           self.flag=True
           self.modelo[" AB".find(self.modelo[0])] = 'clean'

        return ('nothing' if a == b == 'clean' else
                'Clean_up' if self.flag else
                'Go_A' if percepción == 'B' else 'Go_B')
"""

4.- Reconsidera el problema original de los dos cuartos, pero ahora modificalo
    para que cuando el agente decida aspirar, el 80% de las veces limpie pero
    el 20% (aleatorio) deje sucio el cuarto. Diseña un agente racional
    para este problema, pruebalo y comparalo con el agente aleatorio.

    A este entorno llamalo DosCuartosEstocástico
"""
class TwoRoomsStochastic(entornos_o.Agente):
    """
    """
    def __init__(self):
        """

        """
        self.modelo = ['A', 'dirty', 'dirty']

    def programa(self, perception):
        robot, situation = perception

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[' AB'.find(robot)] = situation

        # Decide sobre el modelo interno
        a, b = self.modelo[1], self.modelo[2]


        if situation=='dirty':
            return('Clean_up' if np.random_integers(1, 100) <= 80 else 'nothing')
        else:
            return('nothing' if a == b == 'clean' else
                'Go_A' if robot == 'B' else 'Go_B')

"""

Todos los incisos tienen un valor de 25 puntos sobre la calificación de
la tarea.

"""
def test():
    """
    Prueba del entorno y los agentes

    """
    print("SixRooms:")
    entornos_o.simulador(SixRooms(),
                        AgenteAleatorio(['right', 'left', 'up', 'down', 'clean_up', 'nothing']),
                        100)

    ##############

    print("TwoRoomsBlind:")
    entornos_o.simulador(DosCuartosCiego(),
                        AgenteAleatorio(['Go_A', 'Go_B', 'Clean_up', 'nothing']),
                        100)


    print("TwoRoomsBlindReactive:")
    entornos_o.simulador(DosCuartosCiego(), AgenteReactivoModeloDosCuartosCiego(), 100)

    ###############

    print("TwoRoomsStochastic:")
    entornos_o.simulador(DosCuartosEstocastico(),
                        AgenteAleatorio(['Go_a', 'Go_B', 'Clean_up', 'nothing']),
                        100)

if __name__ == "__main__":
    test()



# Requiere el modulo entornos_o.py
# Usa el modulo doscuartos_o.py para reutilizar código
# Agrega los modulos que requieras de python
