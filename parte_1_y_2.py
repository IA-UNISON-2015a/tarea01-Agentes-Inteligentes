#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
parte_1_y_2.py
------------
   Desarrolla un entorno similar al de los dos cuartos (el cual se
   encuentra en el módulo doscuartos_o.py), pero con tres cuartos en
   el primer piso, y tres cuartos en el segundo piso.

   El entorno se llamará `SeisCuartos`.
   Las acciones totales serán

   ```
   ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]
   ```
   La acción de `"subir"` solo es legal en el piso de abajo (cualquier
   cuarto), y la acción de `"bajar"` solo es legal en el piso de arriba.
   Las acciones de subir y bajar son mas costosas en término de
   energía que ir a la derecha y a la izquierda, por lo que la función
   de desempenio debe de ser de tener limpios todos los cuartos, con el
   menor numero de acciones posibles, y minimizando subir y bajar en
   relación a ir a los lados.
"""

import entornos_o
from random import choice


__author__ = 'Diego Eugenio Bustamante Rendon'


class SeisCuartos(entornos_o.Entorno):
    """

    Clase para un entorno de 6 cuartos.
    """
    def __init__(self, ubicacion=[0,0], estados=[["sucio","sucio","sucio"],["sucio","sucio","sucio"]]):
        """
        Por default inicialmente el robot está en el primer cuarto de abajo y todos los cuartos
        estan sucios
        """
        cuartos_abajo, cuartos_arriba = estados

        self.estado_cuartos = [cuartos_abajo, cuartos_arriba]
        self.ubicacion = ubicacion[:]
        self.desempenio = 0
        self.x = [self.ubicacion, self.estado_cuartos[self.ubicacion[0]][self.ubicacion[1]]]

        """
        @param accion: Una accion en el entorno

        @return: True si la accion en el estado actual, False en caso contrario

        """

    def accion_legal(self, accion):
        if self.ubicacion[0] == 0:
            return accion in ("ir_Derecha", "ir_Izquierda", "subir", "limpiar", "nada")
        elif self.ubicacion[0] == 1:
            return accion in ("ir_Derecha", "ir_Izquierda", "bajar", "limpiar", "nada")

        """
        @param accion: Un elemento de accion_legal

        Modifica self.ubicacion y self.desempenio

        """

    def transicion(self, accion):
        if not self.accion_legal(accion):
            raise ValueError("La accion no es legal para este estado")

        a, b = self.ubicacion

        if accion is "nada" and ("sucio" in self.estado_cuartos[0] or "sucio" in self.estado_cuartos[1]):
            self.desempenio -= 1
        if accion is "limpiar":
            self.estado_cuartos[a][b] = "limpio"
        elif accion is "ir_Derecha" and b<2 :
            self.ubicacion[1] += 1
            self.desempenio -= 1
        elif accion is "ir_Izquierda" and b>0:
            self.ubicacion[1] -= 1
            self.desempenio -= 1
        elif accion is "bajar":
            self.ubicacion[0] -= 1
            self.desempenio -= 2
        elif accion is "subir":
            self.ubicacion[0] += 1
            self.desempenio -= 2

        self.x = [[self.ubicacion[0],self.ubicacion[1]], self.estado_cuartos[self.ubicacion[0]][self.ubicacion[1]]]


    """
    @return: Tupla con los valores que se perciben del entorno por
             default el estado completo
    """

    def percepcion(self):
        return self.ubicacion, self.estado_cuartos


class AgenteAleatorio(entornos_o.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales
    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, percepcion):
        ubicacion, estados = percepcion
        x, y = ubicacion

        if x == 0:
            aux = list(filter(lambda a: a != "bajar", self.acciones))
            return choice(aux)
        elif x == 1:
            aux = list(filter(lambda a: a != "subir", self.acciones))
            return choice(aux)


class AgenteReactivoModelo(entornos_o.Agente):
    """
    Un agente reactivo basado en modelo
    """
    def __init__(self):
        """
        Inicializa el modelo interno en el caso donde todos los cuartos están sucios
        y lo posiciona en el primer cuarto de abajo

        """
        self.ubicacion = [0,0]
        self.estados = [["sucio","sucio","sucio"],["sucio","sucio","sucio"]]

    def programa(self, percepcion):
        ubic, estados = percepcion
        cuartos_abajo = estados[0]
        cuartos_arriba = estados[1]

        # Actualiza el modelo interno
        self.ubicacion = ubic[:]
        self.estados = [cuartos_abajo, cuartos_arriba]

        # Decide sobre el modelo interno

        if estados[self.ubicacion[0]][self.ubicacion[1]] is "sucio":
            return "limpiar"
        elif not "sucio" in estados[0] and not "sucio" in estados[1]:
            return "nada"
        elif ubic[0] is 0:
            if "sucio" in estados[0]:
                return choice(["ir_Derecha", "ir_Izquierda"])
            else: return("subir")
        elif ubic[0] is 1:
            if "sucio" in estados[1]:
                return choice(["ir_Derecha", "ir_Izquierda"])
            else: return("bajar")



def prueba():
    """
    Prueba del entorno y los agentes
    """
    print("\nPrueba del entorno con un agente aleatorio")
    entornos_o.simulador(SeisCuartos(),
                         AgenteAleatorio(["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]),
                         100)

    print("Prueba del entorno con un agente reactivo con modelo")
    entornos_o.simulador(SeisCuartos([0,0],[["sucio","sucio","sucio"],["sucio","sucio","sucio"]]), AgenteReactivoModelo(), 100)


if __name__ == "__main__":
    prueba()
