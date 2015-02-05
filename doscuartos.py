#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
doscuartos.py.py
------------

Ejemplo de un entorno muy simple y agentes idem

"""

__author__ = 'juliowaissman'

import entornos
from random import choice


class DosCuartos(entornos.Entorno):
    """
    Clase para un entorno de dos cuartos. Muy sencilla solo regrupa métodos.

    El estado se define como 
                (robot, A, B) 
    donde robot puede tener los valores "A", "B"
    A y B pueden tener los valores "limpio", "sucio"

    Las acciones válidas en el entorno son 
            "irA", "irB", "limpiar" y "noOp". 
    Todas las acciones son válidas en todos los estados.

    Los sensores es una tupla 
                (robot, limpio?) 
    con la ubicación del robot y el estado de limieza

    """

    def transicion(self, estado, accion):
        if not self.accion_legal(estado, accion):
            raise ValueError("La accion no es legal para este estado")

        robot,A,B= estado

        return (('A', A, B) if accion == 'irA' else
                ('B', A, B) if accion == 'irB' else
                (robot, A, B) if accion == 'noOp' else
                ('A', 'limpio', B) if accion == 'limpiar' and robot == 'A' else
                ('B', A, 'limpio'))
#El agente solo regresa el cuarto en el que esta
    def sensores(self, estado):
        robot,A,B= estado
        return robot

    def accion_legal(self, estado, accion):
        return accion in ('irA', 'irB', 'limpiar', 'noOp')

    def desempeno_local(self, estado, accion):
        robot, A, B = estado
        return 0 if accion == 'noOp' and A == B == 'limpio' else -1

class AgenteReactivoModeloDosCuartos(entornos.Agente):
    """
    Un agente reactivo basado en modelo

    """
    def __init__(self):
        """
        Consideramos los dos cuartos sucios en principio al no conocer la situacion actual
        """
        self.modelo = ['A', 'sucio', 'sucio']
        self.lugar = {'A': 1, 'B': 2}

    def programa(self, percepcion):
        robot = percepcion

        # Actualiza el modelo interno
        self.modelo[0] = robot


        # Decide sobre el modelo interno
        A, B = self.modelo[1], self.modelo[2]
        if (A == B == 'limpio'):
            return('noOp')
        elif (self.modelo[self.lugar[robot]] == 'sucio'): #revisamos si ya limpiamos este cuarto
                self.modelo[self.lugar[robot]] = 'limpio' #Guardamos en el modelo interno que ya se limpio este cuarto y limpiamos
                return('limpiar')
        elif (robot == 'B'):
                return('irA')
        else:
                return('irB')
#El desempeño del agente racional con modelo fue de -3 y el del agente aleatorio de -85
class AgenteAleatorio(entornos.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales

    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, percepcion):
        return choice(self.acciones)
def test():
    """
    Prueba del entorno y los agentes

    """
    print "Prueba del entorno de tres cuartos con un agente aleatorio"
    entornos.simulador(DosCuartos(),
                       AgenteAleatorio(['irA', 'irB', 'limpiar', 'noOp']),
                       ('A','sucio','sucio'), 100)
    print "Prueba del entorno de dos cuartos con un agente reactivo"
    entornos.simulador(DosCuartos(),
                       AgenteReactivoModeloDosCuartos(),
                       ('A','sucio','sucio'), 100)

if __name__ == '__main__':
    test()
