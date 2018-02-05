#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Tarea de desarrollo de entornos y agentes
==========================================

1. Desarrolla un entorno similar al de los dos cuartos (el cual se
   encuentra en el módulo doscuartos_o.py), pero con tres cuartos en
   el primer piso, y tres cuartos en el segundo piso.
   
   El entorno se llamará `SeisCuartos`.

   Las acciones totales serán
   
   ```
   ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]
   ``` 
    
   La acción de `"subir"` solo es legal en el piso de abajo, en los cuartos de los extremos, 
   mientras que la acción de `"bajar"` solo es legal en el piso de arriba y en el cuarto de el centro (dos
   escaleras para subir, una escalera para bajar).

   Las acciones de subir y bajar son mas costosas en término de
   energía que ir a la derecha y a la izquierda, por lo que la función
   de desempeño debe de ser de tener limpios todos los cuartos, con el
   menor numero de acciones posibles, y minimizando subir y bajar en
   relación a ir a los lados. El costo de limpiar es menor a los costos
   de cualquier acción.

2. Diseña un Agente reactivo basado en modelo para este entorno y
   compara su desempeño con un agente aleatorio despues de 100 pasos
   de simulación.

3. Al ejemplo original de los dos cuartos, modificalo de manera que el
   agente solo pueda saber en que cuarto se encuentra pero no sabe si
   está limpio o sucio.

   A este nuevo entorno llamalo `DosCuartosCiego`.

   Diseña un agente racional para este problema, pruebalo y comparalo
   con el agente aleatorio.

4. Reconsidera el problema original de los dos cuartos, pero ahora
   modificalo para que cuando el agente decida aspirar, el 80% de las
   veces limpie pero el 20% (aleatorio) deje sucio el cuarto. Igualmente, 
   cuando el agente decida cambiar de cuarto, se cambie correctamente de cuarto el 90% de la veces
   y el 10% se queda en su lugar. Diseña
   un agente racional para este problema, pruebalo y comparalo con el
   agente aleatorio.

   A este entorno llámalo `DosCuartosEstocástico`.

Todos los incisos tienen un valor de 25 puntos sobre la calificación de
la tarea.

"""
# Requiere el modulo entornos_o.py
# Usa el modulo doscuartos_o.py para reutilizar código
# Agrega los modulos que requieras de python

__author__ = "Jordan Joel Urias Paramo"

import entornos_o
import doscuartos_o 

import random
from collections import namedtuple

##NOTA: La tarea esta chila. Me parece que podria faltar 
##enfasis en el papel de la funcion simulador, como el
##entorno y el agente interactuan.


class SeisCuartos(entornos_o.Entorno):
    """
    Clase entorno definida en el inciso 1
    """
    acciones = {"ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"}
    
    def __init__(self, x0=["A", "sucio", "sucio","sucio", "sucio","sucio", "sucio"]):
        """
        Por default inicialmente el robot está en A y los cuartos
        están sucios

        """
        self.x = x0[:]
        self.desempeño = 0

    def acción_legal(self, acción):
        if acción is "nada" or "limpiar":
            return True
        elif self.x[0] is "A" and accion in ("ir_Derecha","subir"):
            return True
        elif self.x[0] is "B" and accion in ("ir_Derecha","ir_Izquierda"):
            return True
        elif self.x[0] is "C" and accion in ("ir_Izquierda","subir"):
            return True
        elif self.x[0] is "D" and accion is "ir_Derecha":
            return True
        elif self.x[0] is "E" and accion in ("ir_Derecha","ir_Izquierda","bajar"):
            return True
        elif self.x[0] is "F" and accion is "ir_Izquierda":
            return True
        else:
            return False

    def acciones_legales(self):
        posición, _ = self.percepción()
        if posición is "A" :
            return ("ir_Derecha","subir","nada","limpiar")
        elif posición is "B" :
            return ("ir_Derecha","ir_Izquierda","nada","limpiar")
        elif posición is "C":
            return ("ir_Izquierda","subir","nada","limpiar")
        elif posición is "D":
            return ("ir_Derecha","nada","limpiar")
        elif posición is "E" :
            return ("ir_Derecha","ir_Izquierda","bajar","nada","limpiar")
        else:
            return ("ir_Izquierda","nada","limpiar")

    
    def transición(self, acción):
        if not self.acción_legal(acción):
            raise ValueError("La acción no es legal para este estado")

        robot, a, b,c,d,e,f = self.x
        if acción is not "nada" or a is "sucio" or b is "sucio" or c is "sucio"or d is "sucio" or e is "sucio"or f is "sucio":
            if acción is "limpiar":
                self.desempeño -= 1
            elif acción in ("subir","bajar"):
                self.desempeño -= 3
            else:
                self.desempeño -= 2
            
        if acción is "limpiar":
            self.x[" ABCDEF".find(self.x[0])] = "limpio"
        elif acción is "ir_Derecha":
            if robot is "A":
                self.x[0] = "B"
            elif robot is "B":
                self.x[0] = "C"
            elif robot is "D":
                self.x[0] = "E"
            else:
                self.x[0] = "E"
        elif acción is "ir_Izquierda":
            if robot is "C":
                self.x[0] = "B"
            elif robot is "B":
                self.x[0] = "A"
            elif robot is "F":
                self.x[0] = "E"
            else:
                self.x[0] = "D"
        elif acción is "subir":
            if robot is "A":
                self.x[0] = "D"
            else:
                self.x[0] = "F"
        else:
            self.x[0] = "B"

    def percepción(self):
        return self.x[0], self.x[" ABCDEF".find(self.x[0])]

class AgenteReactivoModeloSeisCuartos(entornos_o.Agente):
    """
    Un agente reactivo basado en modelo definido en el inciso 2.

    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = ["A", "sucio", "sucio","sucio", "sucio","sucio", "sucio"]

    def programa(self, percepción):
        robot, situación = percepción

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[' ABCDEF'.find(robot)] = situación

        # Decide sobre el modelo interno
        a, b,c,d,e,f = self.modelo[1], self.modelo[2], self.modelo[3], self.modelo[4], self.modelo[5], self.modelo[6]
        if a == b == c == d == e == f == 'limpio':
            return 'nada'
        elif situación == 'sucio':
            return 'limpiar'
        elif robot == 'A':
            if b=='sucio' or c=='sucio':
                return 'ir_Derecha'
            else:
                return 'subir'
        elif robot == 'B':
            if a=='sucio':
                return 'ir_Izquierda'
            else:
                return 'ir_Derecha'
        elif robot == 'C':
            if a=='sucio' or b=='sucio':
                return 'ir_Izquierda'
            else:
                return 'subir'
        elif robot == 'D':
                return 'ir_Derecha'
        elif robot == 'E':
            if d=='sucio':
                return 'ir_Izquierda'
            elif f=='sucio':
                return 'ir_Derecha'
            else:
                return 'bajar'
        else:
            return 'ir_Izquierda'

class AgenteAleatorioGenerico(entornos_o.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales

    """
    def __init__(self, entorno):
        self.entorno = entorno

    def programa(self, _):
        return random.choice(self.entorno.acciones_legales())

def testEj2():
    """
    Prueba del entorno y los agentes de los incisos 1 y 2

    """
    print("Prueba del entorno con un agente aleatorio")
    entorno = SeisCuartos()
    entornos_o.simulador(entorno, AgenteAleatorioGenerico(entorno),100)

    print("Prueba del entorno con un agente reactivo con modelo")
    entornos_o.simulador(SeisCuartos(), AgenteReactivoModeloSeisCuartos(), 100)

###############################################################################

class DosCuartosCiego(doscuartos_o.DosCuartos):
    """
    Entorno definido en el inciso 3
    """
    def percepción(self):
        return self.x[0]  

class AgenteReactivoModeloDosCuartosCiego(doscuartos_o .AgenteReactivoModeloDosCuartos):
    """
    Un agente reactivo basado en modelo.
    Agente racional definido para el entorno DosCuartosCiego.
    Inciso 3
    """
    def programa(self, percepción):
        robot = percepción

        # Actualiza el modelo interno
        self.modelo[0] = robot

        # Decide sobre el modelo interno
        a, b = self.modelo[1], self.modelo[2]
        if a == b == 'limpio':
            return 'nada'
        elif robot=='A':
            if a =='sucio':
                self.modelo[1] = 'limpio'
                return 'limpiar'
            else:
                return 'ir_B'
        else:
            if b =='sucio':
                self.modelo[2] = 'limpio'
                return 'limpiar'
            else:
                return 'ir_A'

def testEj3():
    """
    Prueba del entorno y los agentes del inciso 3

    """
    print("Prueba del entorno con un agente aleatorio")
    entornos_o.simulador(doscuartos_o.DosCuartos(),
                         doscuartos_o.AgenteAleatorio(['ir_A', 'ir_B', 'limpiar', 'nada']),
                         100)


    print("Prueba del entorno CIEGO con un agente reactivo con modelo")
    entornos_o.simulador(DosCuartosCiego(), AgenteReactivoModeloDosCuartosCiego(), 100)
##########################################################################
class DosCuartosEstocástico(doscuartos_o.DosCuartos):
    """
    Entorno definido en el inciso 4
    """
    def transición(self, acción):
        if not self.acción_legal(acción):
            raise ValueError("La acción no es legal para este estado")

        robot, a, b = self.x
        if acción is not "nada" or a is "sucio" or b is "sucio":
            self.desempeño -= 1
        if acción is "limpiar" and random.random() <= 0.8:
            self.x[" AB".find(self.x[0])] = "limpio"
        elif acción is "ir_A" and random.random() <= 0.9:
            self.x[0] = "A"
        elif acción is "ir_B"and random.random() <= 0.9:
            self.x[0] = "B"
def testEj4():
    """
    Prueba del entorno y los agentes del inciso 4

    """
    print("Prueba del entorno con un agente aleatorio")
    entornos_o.simulador(doscuartos_o.DosCuartos(),
                         doscuartos_o.AgenteAleatorio(['ir_A', 'ir_B', 'limpiar', 'nada']),
                         100)

    print("Prueba del entorno Estocástico con un agente reactivo")
    entornos_o.simulador(DosCuartosEstocástico(), doscuartos_o.AgenteReactivoDoscuartos(), 100)
    
    print("Prueba del entorno Estocástico con un agente reactivo con modelo")
    entornos_o.simulador(DosCuartosEstocástico(), doscuartos_o.AgenteReactivoModeloDosCuartos(), 100)
    

#########################################################################  
  
if __name__ == "__main__":
    testEj2()
    testEj3()
    testEj4()


