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
"""
import entornos
from random import choice
class TresCuartos(entornos.Entorno):

    def transicion(self, estado, accion):
        if not self.accion_legal(estado, accion):
            raise ValueError("La accion no es legal para este estado")

        robot, A, B, C, level = estado

        return (('A', A, B, C, level) if accion == 'irIzquierda' and robot == 'B' else
                ('B', A, B, C, level) if accion == 'irIzquierda' and robot == 'C' else
                ('B', A, B, C, level) if accion == 'irDerecha' and robot == 'A' else
                ('C', A, B, C, level) if accion == 'irDerecha' and robot == 'B' else
                (robot, A, B, C, 'abajo') if accion == 'bajar' and level == 'arriba' else
                (robot, A, B, C, 'arriba') if accion == 'subir' and level == 'abajo' else
                ('A', 'limpio', B, C, 'arriba') if accion == 'limpiar' and robot == 'A' and level == 'arriba' and A == 'limpio(v)' else
                ('A', 'limpio', B, C, 'abajo') if accion == 'limpiar' and robot == 'A' and level == 'abajo'  and A == 'limpio(^)' else
                ('A', 'limpio(v)', B, C, 'abajo') if accion == 'limpiar' and robot == 'A' and level == 'abajo'and A != 'limpio' else
                ('A', 'limpio(^)', B, C, 'arriba') if accion == 'limpiar' and robot == 'A' and level == 'arriba'and A != 'limpio' else
                ('B', A, 'limpio', C, 'arriba') if accion == 'limpiar' and robot == 'B' and level == 'arriba' and B == 'limpio(v)' else
                ('B', A, 'limpio', C, 'abajo') if accion == 'limpiar' and robot == 'B' and level == 'abajo'  and B == 'limpio(^)' else
                ('B', A, 'limpio(v)', C, 'abajo') if accion == 'limpiar' and robot == 'B' and level == 'abajo'and B != 'limpio' else
                ('B', A, 'limpio(^)', C, 'arriba') if accion == 'limpiar' and robot == 'B' and level == 'arriba'and B != 'limpio' else
                ('C', A, B, 'limpio', 'arriba') if accion == 'limpiar' and robot == 'C' and level == 'arriba' and C == 'limpio(v)' else
                ('C', A, B, 'limpio', 'abajo') if accion == 'limpiar' and robot == 'C' and level == 'abajo'  and C == 'limpio(^)' else
                ('C', A, B, 'limpio(v)', 'abajo') if accion == 'limpiar' and robot == 'C' and level == 'abajo'and C != 'limpio' else
                ('C', A, B, 'limpio(^)', 'arriba')if accion == 'limpiar' and robot == 'C' and level == 'arriba'and C != 'limpio' else
                (robot, A, B, C, level))
    def sensores(self, estado):
        robot, A, B, C, level = estado
        return (robot, A if robot == 'A' else
        B if robot == 'B' else C,level)


    def accion_legal(self, estado, accion):
        return accion in ("irDerecha", "irIzquierda", "subir", "bajar", "limpiar" , "noOp")

    def desempeno_local(self, estado, accion):
        robot, A, B, C , level= estado
        return (0 if accion == 'noOp' and A == B == C =='limpio' else
                -2 if accion == 'subir' or accion == 'bajar' else -1)

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
    print "Prueba del entorno de dos cuartos con un agente aleatorio"
    entornos.simulador(TresCuartos(),
                       AgenteAleatorio(["irDerecha", "irIzquierda", "subir", "bajar", "limpiar" , "noOp"]),
                       ('A', 'sucio', 'sucio','sucio','abajo'), 100)

__author__ = 'lcontiveros'

import entornos
# Requiere el modulo entornos.py
# El modulo doscuartos.py puede ser de utilidad para reutilizar código
# Agrega los modulos que requieras de python

if __name__ == '__main__':
    test()
