#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'juanmanuel'

"""

Tarea 1
------------

Tarea de desarrollo de entornos y agentes.
==========================================

En esta tarea realiza las siguiente acciones:

1.- Desarrolla un entorno similar al de los dos cuartos,
    pero con tres cuartos en el primer piso,
    y tres cuartos en el segundo piso.

    Las acciones totales serán

    A = {"Derecha","Izquierda","Subir","Bajar","Limpiar" y "NoOperacion"}

    La acción de "subir" solo es legal en el piso de abajo (cualquier cuarto),
    y la acción de "bajar" solo es legal en el piso de arriba.

    Las acciones de subir y bajar son mas costosas en términos de energía
    que ir a la derecha y a la izquierda, por lo que la función de desempeño
    debe de tener limpios todos los cuartos, con el menor numero de
    acciones posibles, y minimizando subir y bajar en relación a ir a los lados.

2.- Diseña un Agente reactivo basado en modelo para este entorno y compara
    su desempeño con un agente aleatorio despues de 100 pasos de simulación.

"""

import Entornos
from random import choice

"""

Clase para un entorno de tres cuartos en el primer piso,
y tres cuartos en el segundo piso. Muy sencilla solo reagrupa métodos.

El estado se define como (robot,A,B,C,D,E,F).

donde robot puede tener los valores "A","B","C","D","E","F"
A,B,C,D,E,F pueden tener los valores "Limpio" o "Sucio".

Las acciones válidas en el entorno son
"Derecha","Izquierda","Subir","Bajar","Limpiar" y "NoOperacion"
Algunas acciones son válidas dependiendo del estado en que se encuentre.

-Modelo de los cuartos-

{A}---{B}---{C}
 |     |     |
{D}---{E}---{F}

Los Sensores es una tupla (robot,limpio)
con la ubicación del robot y el estado de limpieza.

"""

class Pisos(Entornos.Entorno):

    def Sensores(self,estado):

        robot,A,B,C,D,E,F = estado

        if robot == 'A':
            result = A

        if robot == 'B':
            result = B

        if robot == 'C':
            result = C

        if robot == 'D':
            result = D

        if robot == 'E':
            result = E

        if robot == 'F':
            result = F

        return robot,result

    def Accion_Legal(self,estado,accion):

        robot = estado[0]

        if robot == 'A':
            return accion in ('Derecha','Bajar','Limpiar','NoOperacion')

        if robot == 'B':
            return accion in ('Izquierda','Derecha','Bajar','Limpiar','NoOperacion')

        if robot == 'C':
            return accion in ('Izquierda','Bajar','Limpiar','NoOperacion')

        if robot == 'D':
            return accion in ('Derecha','Subir','Limpiar','NoOperacion')

        if robot == 'E':
            return accion in ('Izquierda','Derecha','Subir','Limpiar','NoOperacion')

        if robot == 'F':
            return accion in ('Izquierda','Subir','Limpiar','NoOperacion')

    def Transicion(self,estado,accion):

        if not self.Accion_Legal(estado,accion):
            raise ValueError("La accion no es legal para este estado")

        robot,A,B,C,D,E,F = estado

        if robot == 'A':
            return (('B', A, B, C, D, E, F) if accion == 'Derecha' else
                    ('D', A, B, C, D, E, F) if accion == 'Bajar' else
                    ('A', 'Limpio', B, C, D, E, F) if accion == 'Limpiar' else
                    (robot, A, B, C, D, E, F))

        if robot == 'B':
            return (('A', A, B, C, D, E, F) if accion == 'Izquierda' else
                    ('C', A, B, C, D, E, F) if accion == 'Derecha' else
                    ('E', A, B, C, D, E, F) if accion == 'Bajar' else
                    ('B', A, 'Limpio', C, D, E, F) if accion == 'Limpiar' else
                    (robot, A, B, C, D, E, F))

        if robot == 'C':
            return (('B', A, B, C, D, E, F) if accion == 'Izquierda' else
                    ('F', A, B, C, D, E, F) if accion == 'Bajar' else
                    ('C', A, B, 'Limpio', D, E, F) if accion == 'Limpiar' else
                    (robot, A, B, C, D, E, F))

        if robot == 'D':
            return (('E', A, B, C, D, E, F) if accion == 'Derecha' else
                    ('A', A, B, C, D, E, F) if accion == 'Subir' else
                    ('D', A, B, C, 'Limpio', E, F) if accion == 'Limpiar' else
                    (robot, A, B, C, D, E, F))

        if robot == 'E':
            return (('D', A, B, C, D, E, F) if accion == 'Izquierda' else
                    ('F', A, B, C, D, E, F) if accion == 'Derecha' else
                    ('B', A, B, C, D, E, F) if accion == 'Subir' else
                    ('E', A, B, C, D, 'Limpio', F) if accion == 'Limpiar' else
                    (robot, A, B, C, D, E, F))

        if robot == 'F':
            return (('E', A, B, C, D, E, F) if accion == 'Izquierda' else
                    ('C', A, B, C, D, E, F) if accion == 'Subir' else
                    ('F', A, B, C, D, E, 'Limpio') if accion == 'Limpiar' else
                    (robot, A, B, C, D, E, F))

    def Desempeno_Local(self,estado,accion):

        robot,A,B,C,D,E,F = estado

        if accion == 'Subir' or accion == 'Bajar':
            return -2

        if accion == 'NoOperacion' and A == B == C == D == E == F == 'Limpio':
            return 0

        else:
            return -1

"""

Un agente que solo regresa una accion al azar entre las acciones legales.

"""

class AgenteAleatorio(Entornos.Agente):

    def Programa(self,percepcion):

        robot = percepcion[0]

        if robot == 'A':
            return choice(['Derecha','Bajar','Limpiar','NoOperacion'])

        if robot == 'B':
            return choice(['Izquierda','Derecha','Bajar','Limpiar','NoOperacion'])

        if robot == 'C':
            return choice(['Izquierda','Bajar','Limpiar','NoOperacion'])

        if robot == 'D':
            return choice(['Derecha','Subir','Limpiar','NoOperacion'])

        if robot == 'E':
            return choice(['Izquierda','Derecha','Subir','Limpiar','NoOperacion'])

        if robot == 'F':
            return choice(['Izquierda','Subir','Limpiar','NoOperacion'])

"""

Un agente reactivo basado en modelo.

"""

class AgenteReactivoBasadoEnModelo(Entornos.Agente):

    def __init__(self):

        self.modelo = ['A','Sucio','Sucio','Sucio','Sucio','Sucio','Sucio']
        self.lugar = {'A':1,'B':2,'C':3,'D':4,'E':5,'F':6}

    def Programa(self,percepcion):

        robot,situacion = percepcion

        self.modelo[0] = robot
        self.modelo[self.lugar[robot]] = situacion

        A,B,C,D,E,F = self.modelo[1],self.modelo[2],self.modelo[3],self.modelo[4],self.modelo[5],self.modelo[6]

        if A == B == C == D == E == F == 'Limpio':
            return 'NoOperacion'

        if robot == 'A':

            if A == B == C == 'Limpio':
                return 'Bajar'

            if A == 'Limpio':
                return 'Derecha'

            if A == 'Sucio':
                return 'Limpiar'

        if robot == 'B':

            if A == B == C == 'Limpio':
                return 'Bajar'

            if B == 'Limpio' and A == 'Limpio':
                return 'Derecha'

            if B == 'Limpio' and C == 'Limpio':
                return 'Izquierda'

            if B == 'Limpio' and A == D == 'Sucio':
                return choice(['Derecha','Izquierda'])

            if B == 'Sucio':
                return 'Limpiar'

        if robot == 'C':

            if A == B == C == 'Limpio':
                return 'Bajar'

            if C == 'Limpio':
                return 'Izquierda'

            if C == 'Sucio':
                return 'Limpiar'

        if robot == 'D':

            if D == E == F == 'Limpio':
                return 'Subir'

            if D == 'Limpio':
                return 'Derecha'

            if D == 'Sucio':
                return 'Limpiar'

        if robot == 'E':

            if D == E == F == 'Limpio':
                return 'Subir'

            if E == 'Limpio' and D == 'Limpio':
                return 'Derecha'

            if E == 'Limpio' and F == 'Limpio':
                return 'Izquierda'

            if E == 'Limpio' and D == F == 'Sucio':
                return choice(['Derecha','Izquierda'])

            if E == 'Sucio':
                return 'Limpiar'

        if robot == 'F':

            if D == E == F == 'Limpio':
                return 'Subir'

            if F == 'Limpio':
                return 'Izquierda'

            if F == 'Sucio':
                return 'Limpiar'

def Test():

    """

    Prueba del entorno y los agentes.

    """

    print "Prueba del entorno de pisos con un agente aleatorio."
    Entornos.Simulador(Pisos(),AgenteAleatorio(),('A','Sucio','Sucio','Sucio','Sucio','Sucio','Sucio'),100)

    print "Prueba del entorno de pisos con un agente reactivo basado en modelo."
    Entornos.Simulador(Pisos(),AgenteReactivoBasadoEnModelo(),('A','Sucio','Sucio','Sucio','Sucio','Sucio','Sucio'),100)

if __name__ == '__main__':
    Test()
