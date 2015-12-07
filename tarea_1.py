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
    acciones posibles, y minimozando subir y bajar en relación a ir a los
    lados.

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

Todos los incisos tienen un valor de 25 puntos sobre la calificación de
la tarea.


"""
__author__ = 'Christian Ruink'

import entornos
import random
# Requiere el modulo entornos.py
# El modulo doscuartos.py puede ser de utilidad para reutilizar código
# Agrega los modulos que requieras de python
from random import choice


class tareaCuartos(entornos.Entorno):
    """
    Clase para un entorno de dos cuartos. Muy sencilla solo regrupa métodos.

    El estado se define como (robot, A, B) 
    donde robot puede tener los valores "A", "B"
    A y B pueden tener los valores "limpio", "sucio"

    Las acciones válidas en el entorno son 
            "irA", "irB", "limpiar" y "noOp". 
    Todas las acciones son válidas en todos los estados.

    Los sensores es una tupla 
                (robot, limpio?) 
    con la ubicación del robot y el estado de limieza
    
    `A = {"irDerecha", "irIzquierda", "subir", "bajar", "limpiar" y "noOp"}`

    """

    def transicion(self, estado, accion):
        print "ACCION: " + accion
        if not self.accion_legal(estado, accion):
            raise ValueError("La accion no es legal para este estado")
        
        print (estado)

        robot, A1, B1, C1, A2, B2 = estado
        if (robot == 'A1' or robot  == 'B1' or robot == 'C1'):
            if robot == 'A1':
                return (('B1', A1, B1, C1, A2, B2) if accion == 'irDerecha' else
                        ('A2', A1, B1, C1, A2, B2) if accion == 'subir' else 
                        ('A1', 'limpio', B1, C1, A2, B2) if accion == 'limpiar' else
                        ('A1', A1, B1, C1, A2, B2))
            if robot == 'B1':
                return (('C1', A1, B1, C1, A2, B2) if accion == 'irDerecha' else
                        ('A1', A1, B1, C1, A2, B2) if accion == 'irIzquierda' else
                        ('B2', A1, B1, C1, A2, B2) if accion == 'subir' else 
                        ('B1', A1, 'limpio', C1, A2, B2) if accion == 'limpiar' else
                        ('B1', A1, B1, C1, A2, B2))
            if robot == 'C1':
                return (('B1', A1, B1, C1, A2, B2) if accion == 'irIzquierda' else
                        ('A1', A1, B1, C1, A2, B2) if accion == 'subir' else 
                        ('C1', A1, B1, 'limpio', A2, B2) if accion == 'limpiar' else
                        ('A1', A1, B1, C1, A2, B2))
        else:
            if robot == 'A2':
                return (('B2', A1, B1, C1, A2, B2) if accion == 'irDerecha' else
                        ('A1', A1, B1, C1, A2, B2) if accion == 'bajar' else 
                        ('A2', A1, B1, C1, 'limpio', B2) if accion == 'limpiar' else
                        ('A2', A1, B1, C1, A2, B2))
            if robot == 'B2':
                return (('A2', A1, B1, C1, A2, B2) if accion == 'irIzquierda' else
                        ('B1', A1, B1, C1, A2, B2) if accion == 'bajar' else 
                        ('B2', A1, B1, C1, 'limpio', B2) if accion == 'limpiar' else
                        ('B2', A1, B1, C1, A2, B2))


    def sensores(self, estado):
        robot, A1, B1, C1, A2, B2 = estado
        if robot == 'A1': return robot, A1
        if robot == 'B1': return robot, B1
        if robot == 'C1': return robot, C1
        if robot == 'A2': return robot, A2
        if robot == 'B2': return robot, B2

            
        
    def accion_legal(self, estado, accion):
        return accion in ('irDerecha', 'irIzquierda', 'subir', 'bajar', 'limpiar', 'noOp')

    def desempeno_local(self, estado, accion):
        robot, A1, B1, C1, A2, B2 = estado
        if (accion == 'noOp' and A1 == B1 == C1== A2== B2== 'limpio'): return 0
        if (accion == 'subir' or accion == 'bajar'): return -2 
        return -1


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
    
class AgenteReactivoTarea(entornos.Agente):
    """
    Un agente reactivo simple

    """

    def programa(self, percepcion):
        robot, situacion = percepcion
        return ('limpiar' if situacion == 'sucio' else
                'irDerecha' if (robot == 'A1' or robot=='A2') else
                'irIzquierda')



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

class AgenteRacionalModeloDosCuartos(entornos.Agente):
    """
    Un agente que limpie 80% del tiempo.
    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = ['A1', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio']
        self.lugar = {'A1': 1, 'B1': 2, 'C1': 3, 'A2': 4, 'B2': 5 }

    def programa(self, percepcion):
        robot, situacion = percepcion

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[self.lugar[robot]] = situacion

        # Decide sobre el modelo interno
        A, B = self.modelo[1], self.modelo[2]
        limpia = (random.random() > .5 )
        
        return ('noOp' if A == B == 'limpio' else
                'limpiar' if situacion == 'sucio' else
                'irA' if robot == 'B' else
                'irB')
    
class AgenteReactivoModeloTarea(entornos.Agente):
    """
    Un agente reactivo basado en modelo

    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = ['A1', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio']
        self.lugar = {'A1': 1, 'B1': 2, 'C1': 3, 'A2': 4, 'B2': 5 }


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
    print "Prueba del entorno de tarea con un agente aleatorio"
    entornos.simulador(tareaCuartos(),
                       AgenteAleatorio(['irDerecha', 'irIzquierda', 'subir', 'bajar', 'limpiar', 'noOp']),
                       ('A1', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio'), 100)

    print "Prueba del entorno de tarea con un agente reactivo"
    entornos.simulador(tareaCuartos(),
                       AgenteReactivoTarea(),
                       ('A1', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio'), 100)

    print "Prueba del entorno de dos pisos con un agente racional"
    entornos.simulador(tareaCuartos(),
                       AgenteRacionalModeloDosCuartos(),
                       ('A1', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio'), 100)

if __name__ == '__main__':
    test()

