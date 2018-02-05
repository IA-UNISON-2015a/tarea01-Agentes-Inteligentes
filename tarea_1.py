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

   Las acciónes totales serán

   ```
   ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]
   ```

   La acción de `"subir"` solo es legal en el piso de abajo, en los cuartos de los extremos,
   mientras que la acción de `"bajar"` solo es legal en el piso de arriba y en el cuarto de el centro (dos
   escaleras para subir, una escalera para bajar).

   Las acciónes de subir y bajar son mas costosas en término de
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
__author__ = 'Adrian Emilio Vazquez Icedo'

import entornos_o
import doscuartos_o
import random

class SeisCuartos(entornos_o.Entorno):
    """
    Clase entorno 6 SeisCuartos
    """
    def __init__(self, x0=["A", "sucio", "sucio","sucio", "sucio", "sucio", "sucio"]):
        """
        Por default esta en A(abajo izquierda) y los 6 cuartos estan sucios
        """
        self.x = x0[:]
        self.desempeño = 0
    def acción_legal(self, acción):
        if acción is "nada" or "limpiar":
            return True
        if self.x[0] is "A" and acción in ("ir_Derecha", "subir"):
           return True
        if self.x[0] is "B" and acción in ("ir_Derecha", "ir_Izquierda"):
           return True
        if self.x[0] is "C" and acción in ("ir_Izquierda", "subir"):
           return True
        if self.x[0] is "D" and acción is "ir_Derecha":
           return True
        if self.x[0] is "E" and acción in ("ir_Derecha", "ir_Izquierda", "bajar"):
           return True
        if self.x[0] is "F" and acción is "ir_Izquierda":
          return True

    def transición(self, acción):
        if not self.acción_legal(acción):
            raise ValueError("Esta acción no es legal en el estado actual")

        robot, a,b,c,d,e,f = self.x
        if acción is not "nada" or a is "sucio" or b is "sucio" or c is "sucio" or d is "sucio" or e is "sucio" or f is "sucio":
            if acción is "limpiar":
                self.desempeño -= 1

            elif acción in ("ir_Derecha", "ir_Izquierda"):
                self.desempeño -= 2
            else:
                self.desempeño -=3

        if acción is "limpiar":
            self.x[" ABCDEF".find(robot)] = "limpio"

        elif acción is "ir_Derecha":
            if robot is "A":
                self.x[0] = "B"
            elif robot is "B":
                self.x[0] = "C"
            elif robot is "D":
                self.x[0] = "E"
            else:
                self.x[0] = "F"
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

class DosCuartosCiego(doscuartos_o.DosCuartos):
    def percepción(self):
        return self.x[0]

class DosCuartosEstocástico(doscuartos_o.DosCuartos):

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

class AgenteReactivoModeloDosCuartosEstocástico(entornos_o.Agente):
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


class AgenteReactivoModeloSeisCuartos(entornos_o.Agente):
    """
    Un agente reactivo basado en modelo

    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = ['A', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio']

    def programa(self, percepción):
        robot, situación = percepción

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[' ABCDEF'.find(robot)] = situación

        # Decide sobre el modelo interno
        a, b, c, d, e, f = self.modelo[1], self.modelo[2], self.modelo[3], self.modelo[4], self.modelo[5], self.modelo[6]

        if not "sucio" in self.modelo:
            return "nada"
        if situación == "sucio":
            return "limpiar"

        if robot in ("A", "B", "C"):
            if not "sucio" in (a,b,c):

                if robot is "B":
                    #Revisar si es mas optimo subir por la izquierda o la derecha
                    return ("ir_Izquierda" if d is "sucio" else "ir_Derecha")
                else:

                    return "subir"
            else:

                return ("ir_Derecha" if robot is "A" or (robot is "B" and a is "limpio") else "ir_Izquierda")
        else:
            if not "sucio" in (d, e, f):
                return ("ir_Derecha" if robot is "D" else "ir_Izquierda" if robot is "F" else "bajar")
            else:
                return ("ir_Derecha" if robot is "D" or (robot is "E" and d is "limpio") else "ir_Izquierda")

class AgenteAleatorioSeisCuartos(entornos_o.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales

    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, percepción):
        robot = percepción[0]
        if robot is "A":
                return random.choice(["ir_Derecha", "subir", "nada", "limpiar"])
        if robot is "B":
                return random.choice(["ir_Derecha", "ir_Izquierda", "nada", "limpiar"])
        if robot is "C":
                return random.choice(["ir_Izquierda", "subir", "nada", "limpiar"])
        if robot is "D":
                return random.choice(["ir_Derecha", "nada", "limpiar"])
        if robot is "E":
                return random.choice(["ir_Derecha", "ir_Izquierda", "bajar", "nada", "limpiar"])

        return random.choice(["ir_Izquierda", "nada", "limpiar"])

class AgenteReactivoDosCuartosCiego(entornos_o.Agente):
     """
     Un agente reactivo basado en modelo

     """
     def __init__(self):
         """
         Inicializa el modelo interno en el peor de los casos

         """
         self.modelo = ['A', 'sucio', 'sucio']

     def programa(self, percepcion):
         robot = percepcion #ubicacion robot

         # Actualiza el modelo interno
         self.modelo[0] = robot

         status = self.modelo[' AB'.find(robot)]

         a, b, = self.modelo[1], self.modelo[2]

         if status is "sucio":
             self.modelo[' AB'.find(robot)] = "limpio"
             return "limpiar"
         if a == b == "limpio":
             return "nada"
         if robot == "A":
             return "ir_B"
         else:
             return "ir_A"


def test():
    """
    Prueba del entorno y los agentes
    """
    
    #inciso 2
    print("Prueba del entorno con un agente reactivo con modelo")
    entornos_o.simulador(SeisCuartos(), AgenteReactivoModeloSeisCuartos(), 100)

    print("Prueba del entorno con un agente aleatorio")
    entornos_o.simulador(SeisCuartos(), AgenteAleatorioSeisCuartos(["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]), 100)

    #inciso 3
    print("Prueba del entorno dos cuatos con agente racional ciego")
    entornos_o.simulador(DosCuartosCiego(), AgenteReactivoDosCuartosCiego(), 100)

    print("Prueba del entorno dos cuatos con agente aleatorio")
    entornos_o.simulador(DosCuartosCiego(), doscuartos_o.AgenteAleatorio(['ir_A', 'ir_B', 'limpiar', 'nada']), 100)

    #inciso 4
    print("Prueba del entorno estocástico con un agente reactivo con modelo")
    entornos_o.simulador(DosCuartosEstocástico(), AgenteReactivoModeloDosCuartosEstocástico(), 100)

    print("Prueba del entorno estocástico con un agente aleatorio")
    entornos_o.simulador(DosCuartosEstocástico(), doscuartos_o.AgenteAleatorio(['ir_A', 'ir_B', 'limpiar', 'nada']), 100)

if __name__ == "__main__":
    test()


# Requiere el modulo entornos_o.py
# Usa el modulo doscuartos_o.py para reutilizar código
# Agrega los modulos que requieras de python
