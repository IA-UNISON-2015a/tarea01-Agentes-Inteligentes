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
__author__ = 'Victor Noriega'

import entornos_o
import doscuartos_o

class SeisCuartos(doscuartos_o.DosCuartos):
    def __init__(self, x0=["A","sucio","sucio",
                            "sucio","sucio", "sucio", "sucio"]):
        """
        El robot empieza en A y todos los cuartos estan sucios.

        """
        self.x = x0[:]
        self.desempeño = 0
    def percepción(self):
        return self.x[0], self.x[" ABCDEF".find(self.x[0])]


    def acción_legal(self, acción, percepción):
        lugar, condicion = percepción
        if lugar is "A":
            return acción in ("ir_der", "subir", "nada")
        elif lugar is "B":
            return acción in ("ir_izq", "ir_der","nada")
        elif lugar is "C":
            return acción in ("ir_der", "subir","nada")
        elif lugar is "D":
            return acción in ("ir_izq","nada")
        elif lugar is "E":
            return acción in ("bajar", "ir_izq", "ir_der","nada")
        elif lugar is "F":
            return acción in ("ir_der", "nada")

    def calcular_desempeño(self, acción, cond):
        if acción is "nada" and self.x[0:].find("sucio") is not -1:
            self.desempeño-=2
        if accion is "ir_izq" or acción is "ir_der":
            self.desempeño-=2
        if acción is "subir" or acción is "bajar":
            self.desempeño-=3
        if acción is "nada":
            # Como chingados no voy a poder poner decimales en mis costos??
            self.desempeño-=1.5
        else:
            self.desempeño-=1

    def transición(self, acción):
        if not self.acción_legal(acción):
            raise ValueError("La acción no es legal para este estado")

        robot = self.x[0]
        cond = sel.x[0:]

        self.calcular_desempeño(acción, robot, cond)


        if acción is "limpiar":
            self.x[" ABCDEF".find(self.x[0])] = "limpio"
        elif acción is "ir_izq":
            if robot is "B":
                robot="A"
            elif robot is "C":
                robot="B"
            elif robot is "D":
                robot="E"
            else:
                robot="F"
        elif acción is "ir_der":
            if robot is "B":
                robot="C"
            elif robot is "A":
                robot="B"
            elif robot is "F":
                robot="E"
            else:
                robot="D"
        elif acción is "subir":
            if robot is "A":
                robot = "F"
            else:
                robot = "D"
        else:
            robot = "E"


# Requiere el modulo entornos_o.py
# Usa el modulo doscuartos_o.py para reutilizar código
# Agrega los modulos que requieras de python
