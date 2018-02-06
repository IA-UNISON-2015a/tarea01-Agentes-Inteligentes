#!/usr/bin/env python
# -*- coding: utf-8 -*-

from doscuartos_o import DosCuartos, AgenteReactivoModeloDosCuartos
import entornos_o
from random import choice, random
import traceback

__author__ = 'Diego Eugenio Bustamante Rendon'

"""

4. Reconsidera el problema original de los dos cuartos, pero ahora
   modificalo para que cuando el agente decida aspirar, el 80% de las
   veces limpie pero el 20% (aleatorio) deje sucio el cuarto. Igualmente,
   cuando el agente decida cambiar de cuarto, se cambie correctamente de cuarto el 90% de la veces
   y el 10% se queda en su lugar. Diseña un agente racional para este problema, pruebalo
   y comparalo con el agente aleatorio.

   A este entorno llámalo `DosCuartosEstocástico`.

"""

class DosCuartosEstocastico(DosCuartos):

    """
        Cambiaremos la función de transición para ahora meter porcentajes
        de probabilidad de acción

    """


    def transicion(self,accion):

        if not self.accion_legal(accion):
            raise ValueError("La accion no es legal para este estado")

        a, b = self.x[1], self.x[2]

        if (accion is not "nada") or ((a is "sucio") or (b is "sucio")):
            self.desempenio -= 1

        if (accion is "limpiar") and random() <= 0.8:
            self.x[" AB".find(self.x[0])] = "limpio"
        elif (accion is "ir_A") and random() <= 0.9:
            self.x[0] = "A"
        elif (accion is "ir_B") and random() <= 0.9:
            self.x[0] = "B"



class AgenteAleatorio(entornos_o.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales
    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, percepcion):
        return choice(self.acciones)

class AgenteReactivoModeloDosCuartosEstocastico(AgenteReactivoModeloDosCuartos):

    def __init__(self, modelo=['A', 'sucio', 'sucio']):
        """
        Inicializa el modelo interno en el peor de los casos
        """
        self.modelo = modelo[:]


def prueba():
    """
    Prueba del entorno y los agentes
    """
    print("\nPrueba del entorno con un agente aleatorio")
    entornos_o.simulador(DosCuartosEstocastico(),
                         AgenteAleatorio(['ir_A', 'ir_B', 'limpiar', 'nada']),
                         100)

    print("Prueba del entorno con un agente estocastico")
    entornos_o.simulador(DosCuartosEstocastico(), AgenteReactivoModeloDosCuartosEstocastico(), 100)


if __name__ == "__main__":
    prueba()
