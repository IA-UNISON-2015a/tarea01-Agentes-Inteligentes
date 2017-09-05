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
    para que cuando el agente decida aspirar, el 80% de las veces limpie pero
    el 20% (aleatorio) deje sucio el cuarto. Diseña un agente racional
    para este problema, pruebalo y comparalo con el agente aleatorio.
o
    A este entorno llamalo DosCuartosEstocástico

Todos los incisos tienen un valor de 25 puntos sobre la calificación de
la tarea.

"""
__author__ = 'escribe_tu_nombre'

import entornos_o
from random import choice,random
class DosCuartosCiego(entornos_o.Entorno):
    """
    Clase para un entorno de dos cuartos. Muy sencilla solo regrupa métodos.

    El estado se define como (robot, A, B)
    donde robot puede tener los valores "A", "B"
    A y B pueden tener los valores "limpio", "sucio"

    Las acciones válidas en el entorno son ("ir_A", "ir_B", "limpiar", "nada").
    Todas las acciones son válidas en todos los estados.

    Los sensores es una tupla (robot, limpio?)
    con la ubicación del robot y el estado de limpieza

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
            self.limpiar(self.x[0])
        elif acción is "ir_A":
            self.x[0] = "A"
        elif acción is "ir_B":
            self.x[0] = "B"
    def limpiar(self,target):
        self.x[" AB".find(target)] = "limpio"
    def percepción(self):
        return self.x[0]
class DosCuartosEstocastico(DosCuartosCiego):
    def limpiar(self,target):
        if random() < 0.5:
            super().limpiar(target)
    def percepción(self):
        return self.x[0], self.x[" AB".find(self.x[0])]

class SeisCuartos(entornos_o.Entorno):
    """
    Clase para un entorno de dos cuartos. Muy sencilla solo regrupa métodos.
    A, B, C son cuartos superiores
    D, E, F son cuartos inferiores
    El estado se define como (robot, A, B, C, D, E, F)
    donde robot puede tener los valores "A", "B", "C", "D", "E", "F"
    "A1", "A2", "A3", "B1", "B2", "B3" pueden tener los valores "limpio", "sucio"

    Las acciones válidas en el entorno son ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"].
    Todas las acciones son válidas en todos los estados.

    Los sensores es una tupla (robot, limpio?)
    con la ubicación del robot y el estado de limpieza

    """
    def __init__(self, x0=["A", "A", "B", "C", "D", "E", "F"]):
        """
        Por default inicialmente el robot está en A1 y los seis cuartos
        están sucios

        """
        self.x = x0[:]
        self.desempeño = 0

    def acción_legal(self, acción):
        return acción in ("ir_Izquierda", "ir_Derecha", "subir", "bajar", "limpiar", "nada")

    def transición(self, acción):
        if not self.acción_legal(acción):
            raise ValueError("La acción no es legal para este estado")

        robot, a1, a2, a3, b1, b2, b3  = self.x
        if acción is not "nada" or a1 is "sucio" or a2 is "sucio" or a3 is "sucio" or b1 is "sucio" or b2 is "sucio" or b3 is "sucio":
            if acción is "subir" or "bajar":
                self.desempeño -=1
            self.desempeño -= 1
        if acción is "limpiar":
            self.x[" ABCDEF".find(self.x[0])] = "limpio"
        elif acción is "ir_Derecha":
            if robot == "A":
                self.x[0] = 'B'
            elif robot == "B":
                self.x[0] = 'C'
            elif robot == "D":
                self.x[0] = 'E'
            elif robot == "E":
                self.x[0] = 'F'
        elif acción is "ir_Izquierda":
            if robot == "B":
                self.x[0] = 'A'
            elif robot == "C":
                self.x[0] = 'B'
            elif robot == "E":
                self.x[0] = 'D'
            elif robot == "F":
                self.x[0] = 'E'
        elif acción is "subir":
            if robot == "A":
                self.x[0] = 'D'
            elif robot == "B":
                self.x[0] = 'E'
            elif robot == "C":
                self.x[0] = 'F'
        elif acción is "bajar":
            if robot == "D":
                self.x[0] = 'A'
            elif robot == "E":
                self.x[0] = 'B'
            elif robot == "F":
                self.x[0] = 'C'

    def percepción(self):
        return self.x[0], self.x[" ABCDEF".find(self.x[0])]


class AgenteAleatorio(entornos_o.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales

    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, percepcion):
        return choice(self.acciones)


class AgenteReactivoDoscuartos(entornos_o.Agente):
    """
    Un agente reactivo simple

    """
    def programa(self, percepción):
        robot, situación = percepción

        return ('limpiar' if situación == 'sucio' else
                'ir_A' if robot == 'B' else 'ir_B')


class AgenteReactivoModeloSeisCuartos(entornos_o.Agente):
    """
    Un agente reactivo basado en modelo

    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = ['A', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio']

    def programa(self, percepción):
        robot, situación = percepción
        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[' ABCDEF'.find(robot)] = situación

        # Decide sobre el modelo interno
        _, a, b, c, d, e, f = self.modelo
        return ('nada' if a == b == c == d == e == f == 'limpio' in self.modelo else
                'limpiar' if situación != 'limpio' else
                'ir_Derecha' if robot == 'A' or robot == 'B' else
                'ir_Izquierda' if robot == 'F' or robot == 'E' else
                'subir' if robot == 'C' else 'bajar')
class AgenteReactivoModeloDosCuartosCiego(entornos_o.Agente):
    def __init__(self):
        self.modelo = ['A', 'sucio', 'sucio']

    def programa(self, percepción):
        robot = percepción
        # Actualiza el modelo interno
        self.modelo[0] = robot
        place = 1 if robot =='A' else 2

        # Decide sobre el modelo interno
        a, b = self.modelo[1], self.modelo[2]

        if a==b=='limpio':
            return 'nada'
        elif self.modelo[place] == 'sucio':
            self.modelo[place] = 'limpio'
            return 'limpiar'
        elif robot == 'B':
            return 'ir_A'
        else:
            return 'ir_B'
class AgenteReactivoModeloDosCuartos(entornos_o.Agente):
    def __init__(self):
        self.modelo = ['A', 'sucio', 'sucio']

    def programa(self, percepción):
        robot, situación = percepción
        print(percepción)
        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[' AB'.find(robot)] = situación

        # Decide sobre el modelo interno
        a, b = self.modelo[1], self.modelo[2]
        return ('nada' if a == b == 'limpio' else
                'limpiar' if situación == 'sucio' else
                'ir_A' if robot == 'B' else 'ir_B')

def test():
    entornos_o.simulador(SeisCuartos(),
                         AgenteAleatorio(["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]),
                         100)
    entornos_o.simulador(SeisCuartos(), AgenteReactivoModeloSeisCuartos(), 100)
    entornos_o.simulador(DosCuartosEstocastico(),
                         AgenteAleatorio(['ir_A', 'ir_B', 'limpiar', 'nada']),
                         100)
    entornos_o.simulador(DosCuartosCiego(), AgenteReactivoModeloDosCuartosCiego(), 100)
    entornos_o.simulador(DosCuartosCiego(), AgenteReactivoModeloDosCuartosCiego(), 100)

if __name__ == "__main__":
    test()
'''
1.- el desempeño que tiene el agente de modelo para el entorno de seis cuartos
    al igual que el que es para dos cuartos es mucho mejor que el agente aleatorio
    ambos llegan a limpiar los dos cuartos, pero el basado en modelos es mucho mas
    veloz y eficaz, hay veces donde 100 iteraciones no bastan para limpiar todos
    los cuartos del modelo con el agente aleatorio
2.- el agente aleatorio se comporta igual para el ejemplo de los dos cuartos ciegos
    el de modelo se asemeja mucho al de dos cuartos con la capacidad de Ver
3.- el agente probabilistico de 20% de probabildiad de no limpiar no es tan diferente
    al de original, ya que es muy baja la probabilidad de que no lo limpie, de igual manera
    el que sea estocastico lo vuelve un tanto mas lento en algunas ocasiones
'''
