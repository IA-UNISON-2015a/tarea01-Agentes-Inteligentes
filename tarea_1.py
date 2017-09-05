#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Tarea de desarrollo de entornos y agentes
==========================================

En esta tarea realiza las siguiente acciones:

1.- Desarrolla un entorno similar al de los dos cuartos (el cual se encuentra
    en el módulo doscuartos_o.py), pero con tres cuartos en el primer piso,
    y tres cuartos en el segundo piso.

    El entorno se llamará SeisCuartos

    Las acciones totales serán

    ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]

    La acción de "subir" solo es legal en el piso de abajo (cualquier cuarto),
    y la acción de "bajar" solo es legal en el piso de arriba.

    Las acciones de subir y bajar son mas costosas en término de energía
    que ir a la derecha y a la izquierda, por lo que la función de desempeño
    debe de ser de tener limpios todos los cuartos, con el menor numero de
    acciones posibles, y minimozando subir y bajar en relación a ir a los
    lados.

2.- Diseña un Agente reactivo basado en modelo para este entorno y compara
    su desempeño con un agente aleatorio despues de 100 pasos de simulación.

3.- Al ejemplo original de los dos cuartos, modificalo de manera que el agente
    solo pueda saber en que cuarto se encuentra pero no sabe si está limpio
    o sucio.

    A este nuevo entorno llamalo DosCuartosCiego

    Diseña un agente racional para este problema, pruebalo y comparalo
    con el agente aleatorio.

4.- Reconsidera el problema original de los dos cuartos, pero ahora modificalo
    para que cuando el agente decida aspirar, el 80% de las veces limpie pero
    el 20% (aleatorio) deje sucio el cuarto. Diseña un agente racional
    para este problema, pruebalo y comparalo con el agente aleatorio.

    A este entorno llamalo DosCuartosEstocástico

Todos los incisos tienen un valor de 25 puntos sobre la calificación de
la tarea.

"""
__author__ = 'Patricia Quiroz'

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from random import choice

import entornos_o

class SeisCuartos(entornos_o.Entorno):
    """
    Clase para un entorno de dos cuartos. Muy sencilla solo regrupa métodos.

    El estado se define como (robot, A, B)
    donde robot puede tener los valores "A", "B"
    A y B pueden tener los valores "limpio", "sucio"

    Las acciones válidas en el entorno son ("ir_A", "ir_B", "limpiar", "nada").
    Todas las acciones son válidas en todos los estados.

    Los sensores es una tupla (robot, limpio?)
    con la ubicación del robot y el estado de limpieza (donde se encuentra el robot).

    """

    def __init__(self, x0=["A", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]):
        """ El robot esta en el cuarto A y todos los cuartos estan sucios
            x=[robot,A,B,C,D,E,F]
            cuartos: D,E,F
                    A,B,C

        Por default, el robot inicia en A y los dos cuartos están sucios

        """
        self.x = x0[:]
        self.desempeno = 0

    def accion_legal(self, accion):
        return accion in ("ir_Der", "ir_Izq", "subir", "bajar", "limpiar", "nada")

    def transicion(self, accion):
        if not self.accion_legal(accion):
            raise ValueError("La acción no es legal para este estado")

        robot, a, b, c, d, e, f = self.x #Se asigna el lugar donde empezara el robot y las situaciones (sucio/limpio) de cada cuarto.

        if accion != "nada" or a is "sucio" or b is "sucio" or c is"sucio" or d is "sucio" or e is "sucio" or f is "sucio":
            if accion is "subir" or accion is "bajar":
                self.desempeno -= 2
            else:
                self.desempeno -= 1

        if accion is "limpiar":
            self.x[" ABCDEF".find(self.x[0])] = "limpio"
        # Posibles formas en que el robot se puede mover dependiendo de el cuarto en donde se encuentre.
        elif accion is "ir_Izq" and self.x[0] is "B" or accion is "bajar" and self.x[0] is "F":
            self.x[0] = "A"
        elif accion is "ir_Der" and self.x[0] is "A" or accion is "bajar" and self.x[0] is "E" or accion is "ir_Izq" and self.x[0] is "C":
            self.x[0] = "B"
        elif accion is "ir_Der" and self.x[0] is "B" or accion is "bajar" and self.x[0] is "D":
            self.x[0] = "C"
        elif accion is "subir" and self.x[0] is "C" or accion is "ir_Der" and self.x[0] is "E":
            self.x[0] = "D"
        elif accion is "subir" and self.x[0] is "B" or accion is "ir_Izq" and self.x[0] is "D" or accion is "ir_Der" and self.x[0] is "F":
            self.x[0] = "E"
        elif accion is "subir" and self.x[0] is "A" or accion is "ir_Izq" and self.x[0] is "E":
            self.x[0] = "F"

    def percepcion(self):
        return self.x[0], self.x[" ABCDEF".find(self.x[0])]


class DosCuartos(entornos_o.Entorno):
    """
    Clase para un entorno de dos cuartos. Muy sencilla solo regrupa métodos.

    El estado se define como (robot, A, B)
    donde robot puede tener los valores "A", "B"
    A y B pueden tener los valores "limpio", "sucio"

    Las acciones válidas en el entorno son ("ir_A", "ir_B", "limpiar", "nada").
    Todas las acciones son válidas en todos los estados.

    Los sensores es una tupla (robot, limpio?)
    con la ubicación del robot y el estado de limpieza (donde se encuentra el robot).
    """

    def __init__(self, x0=["A", "sucio", "sucio"]):
        """
        Por default inicialmente el robot está en A y los dos cuartos
        están sucios
        """
        self.x = x0[:]
        self.desempeno = 0

    def accion_legal(self, accion):
        return accion in ("ir_A", "ir_B", "limpiar", "nada")

    def transicion(self, accion):
        if not self.accion_legal(accion):
            raise ValueError("La acción no es legal para este estado")

        robot, a, b = self.x
        if accion is not "nada" or a is "sucio" or b is "sucio":
            self.desempeno -= 1
        if accion is "limpiar":
            self.x[" AB".find(self.x[0])] = "limpio"
        elif accion is "ir_A":
            self.x[0] = "A"
        elif accion is "ir_B":
            self.x[0] = "B"

    def percepcion(self):
        return self.x[0], self.x[" AB".find(self.x[0])]


class AgenteAleatorio(entornos_o.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales

    """

    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, percepcion):
        return choice(self.acciones)


class AgenteReactivoModeloSeisCuartos(entornos_o.Agente):
    """
    Un agente reactivo basado en modelo
        El modelo empieza desde A y sigue la siguiente forma:
            F <- E <- D
            A -> B -> C ↑

    """

    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = ['A', 'sucio', 'limpio', 'sucio', 'limpio', 'sucio', 'sucio']

    def programa(self, percepcion):
        robot, situacion = percepcion

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[' ABCDEF'.find(robot)] = situacion #Sutuacion donde se encuentra el robot actualmente.

        # Decide sobre el modelo interno
        a, b, c, d, e, f = self.modelo[1], self.modelo[2], self.modelo[3], self.modelo[4], self.modelo[5], self.modelo[6]
        # Cambia dependiendo de situacion
        if a==b==c==d==e==f=='limpio':
            aux='nada'
        elif situacion is 'sucio':
            aux='limpiar'
        elif robot == 'A' or robot == 'B':
            aux='ir_Der'
        elif robot == 'C':
            aux='subir'
        elif robot == 'D' or robot == 'E':
            aux='ir_Izq'

        return (aux)


class AgenteDoscuartosCiegos(entornos_o.Agente):
    """
    Un agente racional donde el robot no sabe si los cuartos estan limpios o sucios, pero en que cuarto se encuentra.
    Como este no sabe si esta un cuarto sucio, por default pensara que todos los cuartos estan sucios.
    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos
        """
        self.modelo = ['A', 'sucio', 'sucio']

    def programa(self, percepcion):
        robot, situacion = percepcion

        # Actualiza el modelo interno
        self.modelo[0] = robot

        # Decide sobre el modelo interno
        a, b = self.modelo[1], self.modelo[2]

        if a == 'limpio' and b == 'limpio':
            aux = 'nada'
        elif robot == 'A':
            if a=='sucio':
                aux='limpiar'
                self.modelo[1]='limpio' #Se actualiza la situacion del modelo para el cuarto A
            else:
                aux='ir_B'
        elif robot == 'B':
            if b=='sucio':
                aux='limpiar'
                self.modelo[2]='limpio' #Se actualiza la situacion del modelo para el cuarto B
            else:
                aux='ir_A'
        return(aux)

class AgenteDosCuartosEstocastico(entornos_o.Agente):
    """
    El agente limpia el 80% de las veces, pero el 20% (aleatorio) deja sucio el cuarto.
    """

    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos
        """
        self.modelo = ['A', 'sucio', 'sucio']

    def programa(self, percepcion):
        robot, situacion = percepcion

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[' AB'.find(robot)] = situacion

        # Decide sobre el modelo interno
        a, b = self.modelo[1], self.modelo[2]

        if a==b=='limpio':
            aux='nada'
        elif situación=='sucio':
            aux=self.limpiezaEst()
        elif robot=='B':
            aux='ir_A'
        elif robot=='A':
            aux='ir_B'
        return aux

    def limpiezaEst(self):
        return ('limpiar' if random.random() <=0.8 else 'nada')


def test():
    """
    Prueba del entorno y los agentes
    """
    print("Prueba del entorno con un agente aleatorio en seis cuartos.")
    entornos_o.simulador(SeisCuartos(),
              AgenteAleatorio(('ir_Der', 'ir_Izq', 'subir', 'bajar', 'limpiar', 'nada')),
             100)

    print("Prueba del entorno con un agente reactivo con modelo de seis cuartos.")
    entornos_o.simulador(SeisCuartos(), AgenteReactivoModeloSeisCuartos(), 100)

    print("Prueba del entorno con un agente aleatorio en dos cuartos.")
    entornos_o.simulador(DosCuartos(), AgenteAleatorio(['ir_A', 'ir_B', 'limpiar', 'nada']), 100)

    print("Prueba del entorno con un agente ciego en dos cuartos.")
    entornos_o.simulador(DosCuartos(), AgenteDoscuartosCiegos(), 100)


if __name__ == "__main__":
    test()
    e = SeisCuartos()
    f = DosCuartos()