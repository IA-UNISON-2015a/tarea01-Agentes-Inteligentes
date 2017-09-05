#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
pt_1.py
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
   de desempeño debe de ser de tener limpios todos los cuartos, con el
   menor numero de acciones posibles, y minimizando subir y bajar en
   relación a ir a los lados.

"""

import entornos_o
from random import choice


__author__ = 'abmorenoc'


class SeisCuartos(entornos_o.Entorno):
    """
    
    Clase para un entorno de 6 cuartos. 

    """
    def __init__(self, ubicacion=[0,0], estados=[["sucio","sucio","sucio"],["sucio","sucio","sucio"]]):
        """
        Por default inicialmente el robot está en el primero cuarto de abajo y todos los cuartos 
        estan sucios

        """
        cuartos_abajo, cuartos_arriba = estados
        
        self.estado_cuartos = [cuartos_abajo, cuartos_arriba]
        self.ubicacion = ubicacion[:]
        self.desempeño = 0
        self.x = [self.ubicacion, self.estado_cuartos[self.ubicacion[0]][self.ubicacion[1]]]

    def acción_legal(self, acción):
        if self.ubicacion[0] == 0:
            return acción in ("ir_Derecha", "ir_Izquierda", "subir", "limpiar", "nada")
        elif self.ubicacion[0] == 1:
            return acción in ("ir_Derecha", "ir_Izquierda", "bajar", "limpiar", "nada")

    def transición(self, acción):
        if not self.acción_legal(acción):
            raise ValueError("La acción no es legal para este estado")

        a, b = self.ubicacion
        
        if acción is "nada" and ("sucio" in self.estado_cuartos[0] or "sucio" in self.estado_cuartos[1]):
            self.desempeño -= 1
        if acción is "limpiar":
            self.estado_cuartos[a][b] = "limpio"
        elif acción is "ir_Derecha" and b<2 :
            self.ubicacion[1] += 1
            self.desempeño -= 1
        elif acción is "ir_Izquierda" and b>0:
            self.ubicacion[1] -= 1
            self.desempeño -= 1
        elif acción is "bajar":
            self.ubicacion[0] -= 1
            self.desempeño -= 2
        elif acción is "subir":
            self.ubicacion[0] += 1
            self.desempeño -= 2
            
        self.x = [[self.ubicacion[0],self.ubicacion[1]], self.estado_cuartos[self.ubicacion[0]][self.ubicacion[1]]]

    def percepción(self):
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
        Inicializa el modelo interno en el peor de los casos

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
        


def test():
    """
    Prueba del entorno y los agentes

    """
    print("Prueba del entorno con un agente aleatorio")
    entornos_o.simulador(SeisCuartos(),
                         AgenteAleatorio(["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]),
                         100)

    print("Prueba del entorno con un agente reactivo con modelo")
    entornos_o.simulador(SeisCuartos([0,0],[["sucio","sucio","sucio"],["sucio","sucio","sucio"]]), AgenteReactivoModelo(), 100)


if __name__ == "__main__":
    test()
