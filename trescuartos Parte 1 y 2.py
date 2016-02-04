#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
trescuartos.py.py
------------
Ejemplo de un entorno muy simple y agentes idem
"""

__author__ = 'juliowaissman'

import entornos
from random import choice


class TresCuartos(entornos.Entorno):
    """
    Clase para un entorno de dos cuartos. Muy sencilla solo regrupa métodos.
    El estado se define como 
                (robot, A, B, C, X, Y, Z) 
    donde robot puede tener los valores "A", "B", "C", 
                                        "X", "Y", "Z"
    A, B, C,
    X, Y, Z pueden tener los valores "limpio", "sucio"
    Las acciones válidas en el entorno son 
            "irA", "irB", "irC" "limpiar" y "noOp". 
    Todas las acciones son válidas en todos los estados.
    Los sensores es una tupla 
                (robot, limpio?) 
    con la ubicación del robot y el estado de limieza
    """

    def transicion(self, estado, accion):
        if not self.accion_legal(estado, accion):
            raise ValueError("La accion no es legal para este estado")

        robot, A, B, C, X, Y, Z = estado

        return (('A', A, B, C, X, Y, Z) if accion == 'irA' else
                ('B', A, B, C, X, Y, Z) if accion == 'irB' else
                ('C', A, B, C, X, Y, Z) if accion == 'irC' else
                ('X', A, B, C, X, Y, Z) if accion == 'irX' else
                ('Y', A, B, C, X, Y, Z) if accion == 'irY' else
                ('Z', A, B, C, X, Y, Z) if accion == 'irZ' else
                (robot, A, B, C, X, Y, Z) if accion == 'noOp' else
                ('A', 'limpio', B, C, X, Y, Z) if accion == 'limpiar' and robot == 'A' else
                ('B', A, 'limpio', C, X, Y, Z) if accion == 'limpiar' and robot == 'B' else
                ('C', A, B, 'limpio', X, Y, Z) if accion == 'limpiar' and robot == 'C' else
                ('X', A, B, C, 'limpio', Y, Z) if accion == 'limpiar' and robot == 'X' else
                ('Y', A, B, C, X, 'limpio', Z) if accion == 'limpiar' and robot == 'Y' else
                ('Z', A, B, C, X, Y, 'limpio'))

    def sensores(self, estado):
        robot, A, B, C, X, Y, Z = estado
        return ((robot, A) if robot == 'A' else
                (robot, B) if robot == 'B' else
                (robot, C) if robot == 'C' else
                (robot, X) if robot == 'X' else
                (robot, Y) if robot == 'Y' else
                (robot, Z))

    def accion_legal(self, estado, accion):
        robot, A, B, C, X, Y, Z = estado
        return (accion in ('irA', 'irB', 'irX', 'limpiar', 'noOp') if robot == 'A' else
                accion in ('irA', 'irB', 'irC', 'irY', 'limpiar', 'noOp') if robot == 'B' else
                accion in ('irB', 'irC', 'irZ', 'limpiar', 'noOp') if robot == 'C' else
                accion in ('irX', 'irY', 'irA', 'limpiar', 'noOp') if robot == 'X' else
                accion in ('irX', 'irY', 'irZ', 'irB', 'limpiar', 'noOp') if robot == 'Y' else
                accion in ('irY', 'irZ', 'irC', 'limpiar', 'noOp'))

    def desempeno_local(self, estado, accion):
        robot, A, B, C, X, Y, Z = estado
        return (0 if accion == 'noOp' and A == B == C == X == Y == Z == 'limpio' else
                -2 if accion == 'irA' and robot == 'X' else
                -2 if accion == 'irB' and robot == 'Y' else
                -2 if accion == 'irC' and robot == 'Z' else
                -2 if accion == 'irX' and robot == 'A' else
                -2 if accion == 'irY' and robot == 'B' else
                -2 if accion == 'irZ' and robot == 'C' else -1)


class AgenteAleatorio(entornos.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales
    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, percepcion):
        robot, situacion = percepcion
        return (choice(['irA', 'irB', 'irX', 'limpiar', 'noOp']) if robot == 'A' else
                choice(['irA', 'irB', 'irC', 'irY', 'limpiar', 'noOp']) if robot == 'B' else
                choice(['irB', 'irC', 'irZ', 'limpiar', 'noOp']) if robot == 'C' else
                choice(['irX', 'irY', 'irA', 'limpiar', 'noOp']) if robot == 'X' else
                choice(['irX', 'irY', 'irZ', 'irB', 'limpiar', 'noOp']) if robot == 'Y' else
                choice(['irY', 'irZ', 'irC', 'limpiar', 'noOp']))


class AgenteReactivoTrescuartos(entornos.Agente):
    """
    Un agente reactivo simple
    """

    def programa(self, percepcion):
        robot, situacion = percepcion
        return ('limpiar' if situacion == 'sucio' else
                'irB' if robot == 'A' else
                'irC' if robot == 'B' else
                'irZ' if robot == 'C' else
                'irY' if robot == 'Z' else
                'irX' if robot == 'Y' else
                'irA')

class AgenteReactivoModeloTresCuartos(entornos.Agente):
    """
    Un agente reactivo basado en modelo
    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos
        """
        self.modelo = ['A', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio']
        self.lugar = {'A': 1, 'B': 2, 'C': 3, 'X': 4, 'Y': 5, 'Z': 6}

    def programa(self, percepcion):
        robot, situacion = percepcion

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[self.lugar[robot]] = situacion

        # Decide sobre el modelo interno
        A, B, C, X, Y, Z = self.modelo[1], self.modelo[2], self.modelo[3], self.modelo[4], self.modelo[5], self.modelo[6]
        return ('noOp' if A == B == C == X == Y == Z == 'limpio' else
                'limpiar' if situacion == 'sucio' else
                'irB' if robot == 'A' else
                'irC' if robot == 'B' else
                'irZ' if robot == 'C' else
                'irY' if robot == 'Z' else
                'irX' if robot == 'Y' else
                'irA')


def test():
    """
    Prueba del entorno y los agentes
    """
    print "Prueba del entorno de tres cuartos con un agente aleatorio"
    entornos.simulador(TresCuartos(),
                       AgenteAleatorio(['irA', 'irB','irC', 'irX', 'irY', 'irZ', 'limpiar', 'noOp']),
                       ('A', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio'), 100)
    
    
    print "Prueba del entorno de tres cuartos con un agente reactivo"
    entornos.simulador(TresCuartos(),
                       AgenteReactivoTrescuartos(),
                       ('A', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio'), 100)
    
    
    print "Prueba del entorno de tres cuartos con un agente reactivo"
    entornos.simulador(TresCuartos(),
                       AgenteReactivoModeloTresCuartos(),
                       ('A', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio'), 100)
    

if __name__ == '__main__':
    test()