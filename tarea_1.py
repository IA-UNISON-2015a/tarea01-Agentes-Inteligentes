#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Tarea de desarrollo de entornos y agentes
==========================================

En esta tarea realiza las siguiente acciones:

1.- Desarrolla un entorno similar al de los dos cuartos, 
    pero con tres cuartos en el primer piso, 
    y tres cuartos en el segundo piso. 
    
    Las acciones totales serán

    A = {"irDerecha", "irIzquierda", "subir", "bajar", "limpiar" y "noOp"}

    La acción de "subir" solo es legal en el piso de abajo (cualquier cuarto), 
    y la acción de "bajar" solo es legal en el piso de arriba.

    Las acciones de subir y bajar son mas costosas en término de energía 
    que ir a la derecha y a la izquierda, por lo que la función de desempeño 
    debe de ser de tener limpios todos los cuartos, con el menor numero de 
    acciones posibles, y minimozando subir y bajar en relación a ir a los lados.

2.- Diseña un Agente reactivo basado en modelo para este entorno y compara 
    su desempeño con un agente aleatorio despues de 100 pasos de simulación.

3.- Al ejemplo original de los dos cuardos, modificalo de manera que el agente 
    sabe en que cuarto se encuentra pero no sabe si está limpio o sucio. 
    Diseña un agente racional para este problema, pruebalo y comparalo 
    con el agente aleatorio.

4.- Reconsidera el problema original de los dos cuartos, pero ahora modificalo 
    para que cuando el agente decida aspirar, el 80% de las veces limpie pero 
    el 20% (aleatorio) deje sucio el cuarto. Diseña un agente racional
    para este problema, pruebalo y comparalo con el agente aleatorio. 

Todos los incisos tienen un valor de 25 puntos sobre la calificación de la tarea.


"""
__author__ = 'Luis Roberto Alcazar Ortega'

import entornos
from random import choice
# Requiere el modulo entornos.py
# El modulo doscuartos.py puede ser de utilidad para reutilizar código
# Agrega los modulos que requieras de python

class Casa(entornos.Entorno):
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

        robot, A, B, C, D, E, F = estado

        return (('A', A, B, C, D, E, F) if accion == 'irIzquierda' and robot == 'B' else
                ('A', A, B, C, D, E, F) if accion == 'bajar' and robot == 'D' else
                ('B', A, B, C, D, E, F) if accion == 'irDerecha' and robot == 'A' else
                ('B', A, B, C, D, E, F) if accion == 'irIzquierda' and robot == 'C' else
                ('B', A, B, C, D, E, F) if accion == 'bajar' and robot == 'E' else
                ('C', A, B, C, D, E, F) if accion == 'irDerecha' and robot == 'B' else
                ('C', A, B, C, D, E, F) if accion == 'bajar' and robot == 'F' else
                ('D', A, B, C, D, E, F) if accion == 'irIzquierda' and robot == 'E' else
                ('D', A, B, C, D, E, F) if accion == 'subir' and robot == 'A' else
                ('E', A, B, C, D, E, F) if accion == 'irDerecha' and robot == 'D' else
                ('E', A, B, C, D, E, F) if accion == 'irIzquierda' and robot == 'F' else
                ('E', A, B, C, D, E, F) if accion == 'subir' and robot == 'B' else
                ('F', A, B, C, D, E, F) if accion == 'irDerecha' and robot == 'E' else
                ('F', A, B, C, D, E, F) if accion == 'subir' and robot == 'C' else
                (robot, A, B, C, D, E, F) if accion == 'noOp' else
                ('A', 'limpio', B, C, D, E, F) if accion == 'limpiar' and robot == 'A' else
                ('B', A, 'limpio', C, D, E, F) if accion == 'limpiar' and robot == 'B' else
                ('C', A, B, 'limpio', D, E, F) if accion == 'limpiar' and robot == 'C' else
                ('D', A, B, C, 'limpio', E, F) if accion == 'limpiar' and robot == 'D' else
                ('E', A, B, C, D, 'limpio', F) if accion == 'limpiar' and robot == 'E' else
                ('F', A, B, C, D, E, 'limpio') if accion == 'limpiar' and robot == 'F' else
                estado)

    def sensores(self, estado):
        robot, A, B, C, D, E, F = estado
        return robot,   \
               (A if robot == 'A' else
                B if robot == 'B' else
                C if robot == 'C' else
                D if robot == 'D' else
                E if robot == 'E' else
                F)

    def accion_legal(self, estado, accion):
        return accion in ('irDerecha', 'irIzquierda', 'subir', 'bajar', 'limpiar', 'noOp')

    def desempeno_local(self, estado, accion):
        robot, A, B, C, D, E, F = estado
        return  (0 if accion == 'noOp' and A == B == C == D == E == F == 'limpio' else
                -2 if accion == 'subir' or accion == 'bajar' else
                -1)


class AgenteAleatorio(entornos.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales

    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, percepcion):
        return choice(self.acciones)


class AgenteReactivoModeloDosCuartos(entornos.Agente):
    def __init__(self):
        self.modelo = ['A', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio']
        self.lugar = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6}

    def programa(self, percepcion):
        robot, situacion = percepcion

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[self.lugar[robot]] = situacion

        # Decide sobre el modelo interno
        A, B, C, D, E, F= self.modelo[1], self.modelo[2], self.modelo[3], self.modelo[4], self.modelo[5], self.modelo[6]
        return ('noOp' if A == B == C == D == E == F == 'limpio' else
                'limpiar' if situacion == 'sucio' else
                'irDerecha' if robot == 'A' and B == 'sucio' or robot == 'B' and C == 'sucio'
                            or robot == 'D' and E == 'sucio' or robot == 'E' and F == 'sucio' else
                'irIzquierda' if (robot == 'B' and A == 'sucio') or (robot == 'C' and B == 'sucio')
                              or (robot == 'E' and D == 'sucio') or (robot == 'F' and E == 'sucio')
                              or (robot == 'C' and B == 'limpio' and A == 'sucio')
                              or (robot == 'F' and E == 'limpio' and D == 'sucio') else
                'subir' if (robot == 'A' or robot == 'B' or robot == 'C') and A == B == C == 'limpio' and D == E == F == 'sucio' else
                'bajar')


def test():
    """
    Prueba del entorno y los agentes

    """
    print "Prueba del entorno de dos cuartos con un agente aleatorio"
    entornos.simulador(Casa(),
                       AgenteAleatorio(['irDerecha', 'irIzquierda', 'subir', 'bajar', 'limpiar', 'noOp']),
                       ('A', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio'), 100)

    print "Prueba del entorno de dos cuartos con un agente reactivo"
    entornos.simulador(Casa(),
                       AgenteReactivoModeloDosCuartos(),
                       ('A', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio'), 100)

if __name__ == '__main__':
    test()