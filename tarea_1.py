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
__author__ = 'Celeste Garcia Espinoza'

import entorno_o

class NueveCuartos(entornos_o.Entorno):
    def __init__(self, x0=["A" + 9 * "sucio"]):
        super().__init__(x, desempeño)

    def acción_legal(self, acción):
        if self.x[0] == "A":
            return acción in ("limpiar", "nada", "subir", "ir_der")
        elif self.x[0] == "B":
            return accion in ("limpiar", "nada", "ir_izq", "ir_der")
        elif self.x[0] == "C":
            return accion in ("limpiar", "nada", "ir_izq")
        elif self.x[0] == "D":
            return accion in ("limpiar", "nada", "subir", "ir_der")
        elif self.x[0] == "E":
            return accion in ("limpiar", "nada", "ir_izq", "ir_der")
        elif self.x[0] == "F":
            return accion in ("limpiar", "nada", "ir_izq", "bajar")
        elif self.x[0] == "G":
            return accion in ("limpiar", "nada", "ir_der")
        elif self.x[0] == "H":
            return accion in ("limpiar", "nada", "ir_izq", "ir_der")
        elif self.x[0] == "I":
            return accion in ("limpiar", "nada", "ir_izq", "bajar")

    def transición(self, acción):
        if not self.acción_legal(acción):
            raise ValueError("Caracoles... La acción no es legal para este estado")

        if acción is "subir" or acción "bajar":
            self.desempeño -= 4
        elif acción is "ir_izq" or acción is "ir_der" or acción is "nada":
            self.desempeño -= 3
        elif accion is "nada":
            self.desempeño -= 2
        else:
            self.desempeño -= 1

        if acción is "limpiar":
            self.x[" ABCDEFGHI".find(self.x[0])] = "limpio"
        elif acción is "ir_izq":
            if self.x[0] == "B":
                self.x[0] = "A"
            elif self.x[0] == "C":
                self.x[0] = "B"
            elif self.x[0] == "E":
                self.x[0] = "D"
            elif self.x[0] == "F":
                self.x[0] = "E"
            elif self.x[0] == "H":
                self.x[0] = "G"
            elif self.x[0] == "I":
                self.x[0] = "H"
        elif acción is "ir_der":
            if self.x[0] == "A":
                self.x[0] = "B"
            elif self.x[0] == "B":
                self.x[0] = "C"
            elif self.x[0] == "D":
                self.x[0] = "E"
            elif self.x[0] == "E":
                self.x[0] = "F"
            elif self.x[0] == "G":
                self.x[0] = "H"
            elif self.x[0] == "H":
                self.x[0] = "I"
        elif acción is "subir":
            if self.x[0] == "A":
                self.x[0] = "D"
            elif self.x[0] == "D":
                self.x[0] = "G"
        elif acción is "bajar":
            if self.x[0] == "F":
                self.x[0] = "C"
            elif self.x[0] == "I":
                self.x[0] = "F"

    def percepción(self):
        return self.x[0], self.x[" ABCDEFGHI".find(self.x[0])]







# Requiere el modulo entornos_o.py
# Usa el modulo doscuartos_o.py para reutilizar código
# Agrega los modulos que requieras de python
