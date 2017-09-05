#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
doscuartos.py.py
------------

Ejemplo de un entorno muy simple y agentes idem

"""

import entornos_o
from random import choice


__author__ = 'Carlos_Huguez'


class SeisCuartos(entornos_o.Entorno):
    """
    El estado se define como (robot, A, B, C, D, E, F)
    donde robot puede tener los valores "A", "B","C", "D","E", "F"
    A ... F pueden tener los valores "limpio", "sucio"

    Las acciones válidas en el entorno son ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"].

    Los sensores es una tupla (robot, limpio?)
    con la ubicación del robot y el estado de limpieza

    """
    def __init__(self, x0=["A", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]):
        self.x = x0[:]
        self.desempeño = 0

    def acción_legal(self, acción):
        return acción in ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]

    def transición(self, acción):

        if not self.acción_legal(acción):
            raise ValueError("La acción no es legal para este estado")

        robot, a, b, c, d, e, f = self.x

        if acción is "nada" and "sucio" in self.x:
            self.desempeño -= 1

        if acción is "limpiar":
            self.desempeño -= 1
            self.x[ " ABCDEF".find( self.x[0] ) ] = "limpio"

        elif acción is "nada" and "sucio" not in self.x:
            pass

        elif acción is "ir_Izquierda":
            if robot is 'A' or robot is 'D':
                pass
            else:
                self.desempeño -= 1
                if robot is 'B' or robot is 'C':
                   self.x[0] =  list(" ABCDEF")[ " ABCDEF".find( self.x[0] ) - 1 ]

                elif robot is 'E' or robot is 'F':

                    self.x[0] = list(" ABCDEF")[ " ABCDEF".find( self.x[0] ) - 1 ]

        elif acción is "ir_Derecha":
            self.desempeño -= 1

            if robot is 'C' or robot is 'F':
                pass
            else:
                if robot is 'A' or robot is 'B':
                    self.x[0] = list(" ABCDEF")[ " ABCDEF".find( self.x[0] ) + 1 ]
                elif robot is 'D' or robot is 'E':
                    self.x[0] = list(" ABCDEF")[" ABCDEF".find(self.x[0]) + 1]

        elif acción is "subir":
            self.desempeño -= 2
            if robot is 'A' or robot is 'B' or robot is 'C' :
                self.x[0] = list(" ABCDEF")[" ABCDEF".find(self.x[0]) + 3]

        elif acción is "bajar":
            self.desempeño -= 2
            if robot is 'D' or robot is 'E' or robot is 'F':
                self.x[0] = list(" ABCDEF")[" ABCDEF".find(self.x[0]) - 3]

    def percepción(self):
        return self.x[0], self.x[ " ABCDEF".find( self.x[0] ) ]





class AgenteAleatorio(entornos_o.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales

    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, percepcion):
        return choice(self.acciones)


class AgenteReactivoSeiscuartos(entornos_o.Agente):
    """
    Un agente reactivo simple

    """
    def programa(self, percepción):
        robot, situación = percepción

        return ('limpiar' if situación is 'sucio' else
                'ir_Derecha' if robot is 'A' or robot is 'B' else
                'subir' if robot is 'C' and situación is 'limpio' else
                'ir_Izquierda' if robot is 'F' or robot is 'E' else
                'bajar' if robot is 'D' and situación is 'limpio' else
                'nada' )

def test():
    """
    Prueba del entorno y los agentes
    """

    #print("Prueba del entorno con un agente aleatorio")
    #entornos_o.simulador( SeisCuartos(), AgenteAleatorio(["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]), 100 )

    #print("Prueba del entorno con un agente reactivo")
    #entornos_o.simulador( SeisCuartos(), AgenteReactivoSeiscuartos(), 100 )

    print("Prueba del entorno con un agente reactivo con modelo")
    entornos_o.simulador( DosCuartos(), AgenteReactivoModeloDosCuartos(), 100)

if __name__ == "__main__":
    test()
    #e = DosCuartos()
    #e.transición('ir_B')
    #print(e.x)
    #e = DosCuartos()
    #print(e.x)
