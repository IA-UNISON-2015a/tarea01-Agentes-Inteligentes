#!/usr/bin/env python
# -*- coding: utf-8 -*-

from doscuartos_o import DosCuartos
import entornos_o
from random import choice

__author__ = 'Diego Eugenio Bustamante Rendon'

"""

3. Al ejemplo original de los dos cuartos, modificalo de manera que el
   agente solo pueda saber en que cuarto se encuentra pero no sabe si
   está limpio o sucio.

   A este nuevo entorno llamalo `DosCuartosCiego`.

   Diseña un agente racional para este problema, pruebalo y comparalo
   con el agente aleatorio.

"""

class DosCuartosCiego(DosCuartos):

    """
    Clase para un entorno de dos cuartos. Muy sencilla solo reagrupa métodos.
    El estado se define como (robot, A, B)
    donde robot puede tener los valores "A", "B"
    A y B pueden tener los valores "limpio", "sucio"
    Las acciones válidas en el entorno son ("ir_A", "ir_B", "limpiar", "nada").
    Todas las acciones son válidas en todos los estados.
    Los sensores es una tupla (robot, limpio)
    con la ubicación del robot y el estado de limpieza
    """

    def percepcion(self):
        """
        Solo percibe en que cuarto esta
        """
        return self.x[0]


class AgenteAleatorio(entornos_o.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales
    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, percepcion):
        return choice(self.acciones)


class AgenteReactivoModeloDosCuartosCiego():
    """
        Un agente reactivo basado en modelo para el entorno dos cuartos ciego
    """
    def __init__(self, modelo=['A', 'sucio', 'sucio']):
        """
        Inicializa el modelo interno en el peor de los casos
        """
        self.modelo = modelo[:]

    def programa(self, percepcion):
        robot = percepcion
        # Actualiza el modelo interno
        self.modelo[0] = robot
        # obtiene la situacion desde el modelo
        situacion = self.modelo[' AB'.find(robot)]
        # Decide sobre el modelo interno
        a, b = self.modelo[1], self.modelo[2]
        # si el cuarto en el que esta el robot esta 'sucio', entonces lo pone en 'limpio' sino lo deja en 'sucio'
        self.modelo[' AB'.find(robot)] = 'limpio' if situacion is 'sucio' else situacion

        return ('nada' if (a == b == 'limpio')
                else 'limpiar' if (situacion is 'sucio')
                else 'ir_A' if (robot is 'B')
                else 'ir_B')

def prueba():
    """
    Prueba del entorno y los agentes
    """
    print("\nPrueba del entorno con un agente aleatorio")
    entornos_o.simulador(DosCuartosCiego(),
                         AgenteAleatorio(['ir_A', 'ir_B', 'limpiar', 'nada']),
                         100)

    print("Prueba del entorno con un agente racional")
    entornos_o.simulador(DosCuartosCiego(), AgenteReactivoModeloDosCuartosCiego(), 100)


if __name__ == "__main__":
    prueba()
