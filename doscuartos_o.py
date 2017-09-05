#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
doscuartos.py.py
------------

Ejemplo de un entorno muy simple y agentes idem

"""

import entornos_o
from random import choice, random


__author__ = 'Carlos_Huguez'


class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def find(self, item):
        return item in self.items

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)



class DosCuartosEstocástico(entornos_o.Entorno):
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
            if random() <= 0.80:
                self.x[" AB".find(self.x[0])] = "limpio"

        elif acción is "ir_A":
            self.x[0] = "A"

        elif acción is "ir_B":
            self.x[0] = "B"

    def percepción(self):
        return self.x[0]

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
            self.x[" AB".find(self.x[0])] = "limpio"

        elif acción is "ir_A":
            self.x[0] = "A"

        elif acción is "ir_B":
            self.x[0] = "B"

    def percepción(self):
        return self.x[0]

class AgenteAleatorio(entornos_o.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales

    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, percepcion):
        return choice(self.acciones)

class AgenteRacionalDoscuartos(entornos_o.Agente):
    """
    Un agente reactivo simple
    """
    pila = Stack()

    def programa(self, percepción):

        robot = percepción

        if not self.pila.find( robot ):
            self.pila.push(robot)
            return "limpiar"
        elif self.pila.peek() is 'A':
            return 'ir_B'
        elif self.pila.peek() is 'B':
            return  'ir_A'


def test():
    """
    Prueba del entorno y los agentes
    """

    print("Prueba del entorno con un agente aleatorio")
    entornos_o.simulador( DosCuartosCiego(), AgenteAleatorio(['ir_A', 'ir_B', 'limpiar', 'nada']), 100 )

    print("Prueba del entorno con un agente reactivo")
    entornos_o.simulador( DosCuartosEstocástico(), AgenteRacionalDoscuartos(), 100 )


if __name__ == "__main__":
    test()
    #e = DosCuartos()
    #e.transición('ir_B')
    #print(e.x)
    #e = DosCuartos()
    #print(e.x)
