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
from random import random


class DosCuartos(entornos.Entorno):
    """
    Modificación del problema de los 2 cuartos. El 80% de los intentos de limpiado de un cuarto
    lo dejan limpio, pero el otro 20% lo dejan sucio.
    """

    #El valor p en esta función es la probabilidad de dejar el cuarto sucio
    def transicion(self, estado, accion):
        if not self.accion_legal(estado, accion):
            raise ValueError("La accion no es legal para este estado")

        robot, A, B = estado


        p = 0.2
        return (('A', A, B) if accion == 'irA' else
                ('B', A, B) if accion == 'irB' else
                (robot, A, B) if accion == 'noOp' or random() < p else
                ('A', 'limpio', B) if accion == 'limpiar' and robot == 'A' else
                ('B', A, 'limpio'))

    def sensores(self, estado):
        robot, A, B = estado
        return robot, A if robot == 'A' else B

    def accion_legal(self, estado, accion):
        if estado[0] == 'A':
            return accion in ('irB', 'limpiar', 'noOp')
        else:
            return accion in ('irA', 'limpiar', 'noOp')

    def desempeno_local(self, estado, accion):
        robot, A, B = estado
        return 0 if accion == 'noOp' and A == B == 'limpio' else -1


class AgenteAleatorio(entornos.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales
    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, percepcion):
        return choice(self.acciones)


class AgenteReactivoDoscuartos(entornos.Agente):
    """
    Un agente reactivo simple
    """

    def programa(self, percepcion):
        robot, situacion = percepcion

        
        return ('limpiar' if situacion == 'sucio' else
                'irA' if robot == 'B' else
                'irB')


class AgenteReactivoModeloDosCuartos(entornos.Agente):
    """
    Un agente reactivo basado en modelo
    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos
        """
        self.modelo = ['A', 'sucio', 'sucio']
        self.lugar = {'A': 1, 'B': 2}

    def programa(self, percepcion):
        robot, situacion = percepcion

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[self.lugar[robot]] = situacion

        # Decide sobre el modelo interno
        A, B = self.modelo[1], self.modelo[2]
        return ('noOp' if A == B == 'limpio' else
                'limpiar' if situacion == 'sucio' else
                'irA' if robot == 'B' else
                'irB')


def test():
    """
    Prueba del entorno y los agentes
    """
    
    #Número de pruebas
    n = 50
    
    
    print "Prueba del entorno de dos cuartos con un agente aleatorio"
    entornos.simulador(DosCuartos(),
                       AgenteAleatorio(['irA', 'irB', 'limpiar', 'noOp']),
                       ('A', 'sucio', 'sucio'), n)

    print "Prueba del entorno de dos cuartos con un agente reactivo"
    entornos.simulador(DosCuartos(),
                       AgenteReactivoDoscuartos(),
                       ('A', 'sucio', 'sucio'), n)

    print "Prueba del entorno de dos cuartos con un agente reactivo"
    entornos.simulador(DosCuartos(),
                       AgenteReactivoModeloDosCuartos(),
                       ('A', 'sucio', 'sucio'), n)

if __name__ == '__main__':
    test()
