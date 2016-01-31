#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Tarea de desarrollo de entornos y agentes
==========================================
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
        B if robot == 'B' else C,'arriba' if level == 'arriba' else 'abajo')


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

class AgenteReactivoModeloTresCuartos(entornos.Agente):
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = ['A', 'sucio', 'sucio','sucio','abajo']
        self.lugar = {'A': 1, 'B': 2,'C':3}

    def programa(self, percepcion):
        robot, situacion, level = percepcion

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[self.lugar[robot]] = situacion
        self.modelo[4] = level

        # Decide sobre el modelo interno
        A, B, C = self.modelo[1], self.modelo[2], self.modelo[3]
        return ('noOp' if A == B == C == 'limpio' else
                'limpiar' if (situacion == 'sucio' or situacion == 'limpio(^)' and level == 'abajo') else
                'limpiar' if (situacion == 'sucio' or situacion == 'limpio(v)' and level == 'arriba') else
                'irDerecha' if robot != 'C' and level == 'abajo' else
                'irIzquierda' if robot != 'A' and level == 'arriba'else
                'subir' if (robot == 'A' or robot == 'C') and level == 'abajo' else
                'bajar')
#Despues de probar este modelo, su funcion de desempeño termino en -12, mientras que con el agente aleatorio fue de -132

def test():
    """
    Prueba del entorno y los agentes

    """
    print ("Prueba del entorno de tres cuartos con un agente aleatorio" ,
    entornos.simulador(TresCuartos(),
                       AgenteAleatorio(["irDerecha", "irIzquierda", "subir", "bajar", "limpiar" , "noOp"]),
                       ('A', 'sucio', 'sucio','sucio','abajo'), 100))
    print ("Prueba del entorno de tres cuartos con un agente reactivo" ,
    entornos.simulador(TresCuartos(),
                       AgenteReactivoModeloTresCuartos(),
                       ('A', 'sucio', 'sucio','sucio', 'abajo'), 100))

__author__ = 'lcontiveros'
#
import entornos
# Requiere el modulo entornos.py
# El modulo doscuartos.py puede ser de utilidad para reutilizar código
# Agrega los modulos que requieras de python

if __name__ == '__main__':
    test()
