#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
doscuartos.py.py
------------

Ejemplo de un entorno muy simple y agentes idem

"""

import entornos_o
from random import choice


__author__ = 'juliowaissman'


class DosCuartos(entornos_o.Entorno):
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
        self.desempeno = 0

    def accion_legal(self, accion):
        return accion in ("ir_A", "ir_B", "limpiar", "nada")

    def transicion(self, accion):
        if not self.accion_legal(accion):
            raise ValueError("La acción no es legal para este estado")

        robot, a, b = self.x
        if accion is not "nada" or a is "sucio" or b is "sucio":
            self.desempeno -= 1
        if accion is "limpiar":
            self.x[" AB".find(self.x[0])] = "limpio"
        elif accion is "ir_A":
            self.x[0] = "A"
        elif accion is "ir_B":
            self.x[0] = "B"

    def percepcion(self):
        return self.x[0], self.x[" AB".find(self.x[0])]


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
    def programa(self, percepcion):
        robot, situacion = percepcion
        return ('limpiar' if situacion == 'sucio' else
                'ir_A' if robot == 'B' else 'ir_B')


class AgenteReactivoModeloDosCuartos(entornos_o.Agente):
    """
    Un agente reactivo basado en modelo

    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
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


def test():
    """
    Prueba del entorno y los agentes

    """
    print("Prueba del entorno con un agente aleatorio")
    entornos_o.simulador(DosCuartos(),
                         AgenteAleatorio(['ir_A', 'ir_B', 'limpiar', 'nada']),
                         100)

    print("Prueba del entorno con un agente reactivo")
    entornos_o.simulador(DosCuartos(), AgenteReactivoDoscuartos(), 100)

    print("Prueba del entorno con un agente reactivo con modelo")
    entornos_o.simulador(DosCuartos(), AgenteReactivoModeloDosCuartos(), 100)


if __name__ == "__main__":
    test()
