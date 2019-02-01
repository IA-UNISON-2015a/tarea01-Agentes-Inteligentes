#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Tarea de desarrollo de entornos y agentes
==========================================

1. Desarrolla un entorno similar al de los dos cuartos (el cual se encuentra en el módulo doscuartos_o.py), pero con
   tres cuartos en el primer piso, tres cuartos en el segundo piso y tres cuartos en el 3er piso.

   El entorno se llamará NueveCuartos.

   Las acciones totales serán

   ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]
   La acción de "subir" solo es legal en los primeros dos pisos, en los cuartos de la derecha, mientras que la acción 
   de "bajar" solo es legal en los dos pisos de arriba de arriba y en el cuarto de la izquierda.

   Las acciones de subir y bajar son mas costosas en término de energía que ir a la derecha y a la izquierda, por lo 
   que la función de desempeño debe de ser de tener limpios todos los cuartos, con el menor numero de acciones 
   posibles, y minimizando subir y bajar en relación a ir a los lados. El costo de limpiar es menor a los costos   
   de cualquier acción.

2. Diseña un Agente reactivo basado en modelo para este entorno y compara su desempeño con un agente aleatorio 
   despues de 200 pasos de simulación.

3. A este modelo de NueveCuartos, modificalo de manera que el agente solo pueda saber en que cuarto se encuentra pero
   no sabe si está limpio o sucio. Utiliza la herencia entre clases para no escribir código redundante.

   A este nuevo entorno llamalo NueveCuartosCiego.

   Diseña un agente racional para este problema, pruebalo y comparalo con el agente aleatorio.

4. Al modelo original de NueveCuartos modificalo para que cuando el agente decida aspirar, el 80% de las veces limpie
   pero el 20% (aleatorio) deje sucio el cuarto. Igualmente, cuando el agente decida cambiar de cuarto, se cambie 
   correctamente de cuarto el 80% de la veces, el 10% de la veces se queda en su lugar y el 10% de las veces realiza 
   una acción legal aleatoria. Diseña un agente racional para este problema, pruebalo y comparalo con el agente aleatorio.

   A este entorno llámalo NueveCuartosEstocástico.

Todos los incisos tienen un valor de 25 puntos sobre la calificación de la tarea.

"""
__author__ = 'Lizeth Soto Félix'

import entornos_o
from random import choice


class NueveCuartos(entornos_o.Entorno):
    """
    El estado se define como (robot, A, B, C, piso_actual, estado_piso_1, estado_piso_2, estado_piso_3)
    donde robot puede tener los valores "A", "B"
    A y B pueden tener los valores "limpio", "sucio"

    Las acciones válidas en el entorno son ("ir_A", "ir_B", "limpiar", "nada").
    Todas las acciones son válidas en todos los estados.

    Los sensores es una tupla (robot, limpio?, piso)
    con la ubicación del robot y el estado de limpieza

    """
    def __init__(self, x0=["1", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"],"sucio","sucio"):
        """
        Por default inicialmente el robot está en A y los dos cuartos
        están sucios

        """
        self.x = x0[:]
        self.desempeño = 0
        self.a_legal={1:["ir_Derecha"],
                      2:["ir_Derecha","ir_Izquierda"]
                      3:["ir_Izquierda","subir"],
                      4:["ir_Derecha","bajar"],
                      5:["ir_Izquierda","ir_Derecha"],
                      6:["ir_Izquierda","subir"],
                      7:["ir_Derecha"],
                      8:["ir_Izquierda","ir_Derecha"],
                      9:["ir_Izquierda"],
                      }

    def acción_legal(self, acción):
        
        return acción in ["limpiar", "nada"]+self.a_legal[self.x[0]]

    def transición(self, acción):
        if not self.acción_legal(acción):
            raise ValueError("La acción no es legal para este estado")

        robot, a, b, c, piso_actual, estado_piso_1, estado_piso_2, estado_piso_3 = self.x
        
        if acción is not "nada" or estado_piso_1 is "incompleto" or estado_piso_2 is "incompleto" or estado_piso_3 is "incompleto":
            self.desempeño -= 1
        if acción is "limpiar":
            self.x[" ABC".find(self.x[0])] = "limpio"
            if a is "limpio" and b is "limpio" and c is "limpio":
                self.x[4+self.x[4]] = "limpio"
        elif acción is "ir_Izquierda":
            if robot is "C":
                self.x[0] = "B"
            elif robot is "B":
                self.x[0] = "A"
        elif acción is "ir_Derecha":
            if robot is "B":
                self.x[0] = "C"
            elif robot is "A":
                self.x[0] = "B"
        elif acción is "subir":
            if piso_actual is "1":
                self.x[4] = 2
            elif piso_actual is "2":
                self.x[4] = 3
        elif acción is "bajar":
            if piso_actual is "3":
                self.x[4] = 2
            elif piso_actual is "2":
                self.x[4] = 1

    def percepción(self):
        return self.x[0], self.x[" ABC".find(self.x[0])], self.x[4]


class AgenteAleatorio(entornos_o.Agente,NueveCuartos):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales

    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, percepcion):
        robot,_,piso = percepcion
        self.x=[robot,"_","_","_",piso]
        lista_legales_nolegales= list(self.acciones)
        lista_legales=[ac for ac in lista_legales_nolegales if self.acción_legal(ac)]
        choice1 = choice(lista_legales)
        print("lista:",lista_legales)
        print("choice:", choice1)
        return (choice1)
        #return choice(self.acciones)


class AgenteReactivoDoscuartos(entornos_o.Agente):
    """
    Un agente reactivo simple

    """
    def programa(self, percepción):
        robot, situación = percepción
        return ('limpiar' if situación == 'sucio' else
                'ir_A' if robot == 'B' else 'ir_B')


class AgenteReactivoModeloDosCuartos(entornos_o.Agente):
    """
    Un agente reactivo basado en modelo

    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = ['A', 'sucio', 'sucio']

    def programa(self, percepción):
        robot, situación = percepción

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[' AB'.find(robot)] = situación

        # Decide sobre el modelo interno
        a, b = self.modelo[1], self.modelo[2]
        return ('nada' if a == b == 'limpio' else
                'limpiar' if situación == 'sucio' else
                'ir_A' if robot == 'B' else 'ir_B')


def test():
    """
    Prueba del entorno y los agentes

    """
    print("Prueba del entorno con un agente aleatorio")
    entornos_o.simulador(NueveCuartos(),
                         AgenteAleatorio(['ir_Izquierda', 'ir_Derecha', 'limpiar', 'nada', "subir", "bajar"]),
                         50)

    #print("Prueba del entorno con un agente reactivo")
    #entornos_o.simulador(DosCuartos(), AgenteReactivoDoscuartos(), 100)

    #print("Prueba del entorno con un agente reactivo con modelo")
    #entornos_o.simulador(DosCuartos(), AgenteReactivoModeloDosCuartos(), 100)


if __name__ == "__main__":
    test()