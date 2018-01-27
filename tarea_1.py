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
__author__ = "Jordan Joel Urias Paramo"

import entorno_o

class SeisCuartos(entornos_o.Entorno):
    """
    Clase entorno definida en el inciso 1
    """
    def __init__(self, x0=["A", "sucio", "sucio","sucio", "sucio","sucio", "sucio"]):
        """
        Por default inicialmente el robot está en A y los cuartos
        están sucios

        """
        self.x = x0[:]
        self.desempeño = 0

    def acción_legal(self, acción):
        if accion is "nada":
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
        else return False

    def transición(self, acción):
        if not self.acción_legal(acción):
            raise ValueError("La acción no es legal para este estado")

        robot, a, b,c,d,e,f = self.x
        if acción is not "nada" or a is "sucio" or b is "sucio" or c is "sucio"or d is "sucio" or e is "sucio"or f is "sucio":
            if accion is "limpiar":
                self.desempeño -= 1
            elif accion in ("subir","bajar"):
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

# Requiere el modulo entornos_o.py
# Usa el modulo doscuartos_o.py para reutilizar código
# Agrega los modulos que requieras de python
