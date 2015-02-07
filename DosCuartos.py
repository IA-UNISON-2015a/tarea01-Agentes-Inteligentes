#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'juanmanuel'

"""

Tarea 1
------------

Tarea de desarrollo de entornos y agentes.
==========================================

En esta tarea realiza las siguiente acciones:

3.  Al ejemplo original de los dos cuartos, modificalo de manera que el agente
    sabe en que cuarto se encuentra pero no sabe si está limpio o sucio.
    Diseña un agente racional para este problema, pruebalo y comparalo
    con el agente aleatorio.

4.  Reconsidera el problema original de los dos cuartos, pero ahora modificalo
    para que cuando el agente decida aspirar, el 80% de las veces limpie pero
    el 20% (aleatorio) deje sucio el cuarto. Diseña un agente racional
    para este problema, pruebalo y comparalo con el agente aleatorio.

"""

import Entornos
from random import choice
from random import randint

"""
Clase para un entorno de dos cuartos. Muy sencilla solo regrupa métodos.

El estado se define como (robot, A, B).

donde robot puede tener los valores "A","B"
A y B pueden tener los valores "Limpio" o "Sucio"

Las acciones válidas en el entorno son
"IrA","IrB","Limpiar" y "NoOperacion".
Todas las acciones son válidas en todos los estados.

Los sensores es una tupla
(robot, limpio?)
con la ubicación del robot y el estado de limpieza.

"""

class DosCuartos(Entornos.Entorno):

    def Sensores(self,estado):

        robot,A,B = estado

        return robot,A if robot == 'A' else B

    def Accion_Legal(self,estado,accion):

        return accion in ('IrA','IrB','Limpiar','NoOperacion')

    def Transicion(self,estado,accion):

        if not self.Accion_Legal(estado,accion):
            raise ValueError("La accion no es legal para este estado")

        robot,A,B = estado

        return (('A', A, B) if accion == 'IrA' else
                ('B', A, B) if accion == 'IrB' else
                (robot, A, B) if accion == 'NoOperacion' else
                ('A', 'Limpio', B) if accion == 'Limpiar' and robot == 'A' else
                ('B', A, 'Limpio'))

    def Desempeno_Local(self,estado,accion):

        robot,A,B = estado

        return 0 if accion == 'NoOperacion' and A == B == 'Limpio' else -1

"""

Un agente que solo regresa una accion al azar entre las acciones legales.

"""

class AgenteAleatorio(Entornos.Agente):

    def __init__(self,acciones):

        self.acciones = acciones

    def Programa(self,percepcion):

        return choice(self.acciones)

"""

    Un agente reactivo simple.

"""

class AgenteReactivoDoscuartos(Entornos.Agente):

    def Programa(self,percepcion):

        robot,situacion = percepcion

        return ('Limpiar' if situacion == 'Sucio' else
                'IrA' if robot == 'B' else
                'IrB')

"""

    Un agente reactivo basado en modelo.

"""

class AgenteReactivoModeloDosCuartos(Entornos.Agente):

    def __init__(self):

        """

        Inicializa el modelo interno en el peor de los casos.


        """

        self.modelo = ['A','Sucio','Sucio']

        self.lugar = {'A':1,'B':2}

    def Programa(self, percepcion):

        robot,situacion = percepcion

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[self.lugar[robot]] = situacion

        # Decide sobre el modelo interno
        A,B = self.modelo[1],self.modelo[2]
        return ('NoOperacion' if A == B == 'Limpio' else
                'Limpiar' if situacion == 'Sucio' else
                'IrA' if robot == 'B' else
                'IrB')

"""

    Un agente racional que no conoce la situacion del cuarto.

"""

class AgenteRacionalP3(Entornos.Agente):

    def __init__(self):

        self.lugar = [0,0]

    def Programa(self,percepcion):

        situacion = percepcion[0]

        if self.lugar[0] == 1 and self.lugar[1] == 1:
            return 'NoOperacion'

        if situacion == 'A' and self.lugar[0] == 0:
            self.lugar[0] = 1
            return 'Limpiar'

        if situacion == 'A' and self.lugar[0] == 1:
            return 'IrB'

        if situacion == 'B' and self.lugar[1] == 0:
            self.lugar[1] = 1
            return 'Limpiar'

        if situacion == 'B' and self.lugar[1] == 1:
            return 'IrA'

"""

    Un agente racional que limpia el cuarto el 80% de las veces.

"""

class AgenteRacionalP4(Entornos.Agente):

    def __init__(self):

        self.modelo = ['A','Sucio','Sucio']

        self.lugar = {'A':1,'B':2}

    def Programa(self, percepcion):

        robot,situacion = percepcion

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[self.lugar[robot]] = situacion

        # Decide sobre el modelo interno
        A,B = self.modelo[1], self.modelo[2]

        # Generamos un numero aleatorio entre (1,8)
        aleatorio = randint(1,10)

        #print aleatorio

        if A == B == 'Limpio':
            return 'NoOperacion'

        if robot == 'A' and situacion == 'Limpio':
            return 'IrB'

        if robot == 'B' and situacion == 'Limpio':
            return 'IrA'

        if situacion == 'Sucio' and aleatorio <= 8:
            return 'Limpiar'
        else:
            return 'NoOperacion'

def Test():
    """

    Prueba del entorno y los agentes.


    """

    """

    print "Prueba del entorno de dos cuartos con un agente aleatorio."
    Entornos.Simulador(DosCuartos(),AgenteAleatorio(['IrA','IrB','Limpiar','NoOperacion']),('A','Sucio','Sucio'),10)

    """

    """

    print "Prueba del entorno de dos cuartos con un agente reactivo."
    Entornos.Simulador(DosCuartos(),AgenteReactivoDoscuartos(),('A','Sucio','Sucio'),100)

    """

    """

    print "Prueba del entorno de dos cuartos con un agente reactivo."
    Entornos.Simulador(DosCuartos(),AgenteReactivoModeloDosCuartos(),('B', 'Sucio', 'Sucio'), 100)

    """

    #"""

    print "Prueba del entorno de dos cuartos con un agente racional que no conoce la situacion del cuarto."
    Entornos.Simulador(DosCuartos(),AgenteRacionalP3(),('B','Sucio','Sucio'), 100)

    print "VS"

    print "Prueba del entorno de dos cuartos con un agente aleatorio."
    Entornos.Simulador(DosCuartos(),AgenteAleatorio(['IrA','IrB','Limpiar','NoOperacion']),('A','Sucio','Sucio'),100)

    #"""

    #"""
    print "Prueba del entorno de dos cuartos con un agente racional que limpia el cuarto el 80% de las veces"
    Entornos.Simulador(DosCuartos(),AgenteRacionalP4(),('B','Sucio','Sucio'), 100)

    print "VS"

    print "Prueba del entorno de dos cuartos con un agente aleatorio."
    Entornos.Simulador(DosCuartos(),AgenteAleatorio(['IrA','IrB','Limpiar','NoOperacion']),('A','Sucio','Sucio'),100)
    #"""

if __name__ == '__main__':
    Test()
