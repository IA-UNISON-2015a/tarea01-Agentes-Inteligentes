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
__author__ = 'ricardoholguin'

import entorno_o

###1
class SeisCuartos(entornos_o.Entorno):
    """
    Los nombres de las habitaciones son de la A a la F, donde A-C son las habitaciones
    del primer piso y D-F son las habitaciones del segundo piso. Ejemplo: A, B, C, D,
    E, F. Siendo A y C las habitaciones que tienen escaleras para subir, y E la
    habitacion que tiene escaleras para bajar

    Por default inicialmente el robot esta en A y todos los cuartos estan sucios
    """
    def __init__(self, x0=["A","sucio","sucio","sucio","sucio","sucio","sucio"]):
        self.x = x0[:]
        self.desempeño = 0

    def acción_legal(self, acción):
        if self.x[0] == "A":
            esLegal = accion in ("ir_D", "ir_B", "limpiar", "nada")
        elif self.x[0] == "B":
            esLegal = accion in ("ir_A", "ir_C", "limpiar", "nada")
        elif self.x[0] == "C":
            esLegal = accion in ("ir_B", "ir_F", "limpiar", "nada")
        elif self.x[0] == "D":
            esLegal = accion in ("ir_E", "limpiar", "nada")
        elif self.x[0] == "E":
            esLegal = accion in ("ir_B", "ir_D", "ir_F", "limpiar", "nada")
        else:   #Supones que el robot esta en F
            esLegal = accion in ("ir_E", "limpiar", "nada")

        return esLegal

    def transición(self, acción):
        if not self.acción_legal(acción):
            raise ValueError("La acción no es legal para este estado")

        robot, a, b = self.x
        if acción is not "nada" or a is "sucio" or b is "sucio":
            self.desempeño -= 1
        if acción is "limpiar":
            self.x[" ABCDEF".find(self.x[0])] = "limpio"
        elif acción is "ir_A":
            self.x[0] = "A"
        elif: acción is "ir_B":
            if self.x[0] == "E":
                self.desempeño -= 2
            self.x[0] = "B"
        elif: acción is "ir_C":
            self.x[0] = "C"
        elif: acción is "ir_D":
            if self.x[0] == "A":
                self.desempeño -= 2
            self.x[0] = "D"
        elif: acción is "ir_E":
            self.x[0] = "E"
        elif: acción is "ir_F":
            if self.x[0] == "C":
                self.desempeño -= 2
            self.x[0] = "F"

    def percepción(self):
        return self.x[0], self.x[" ABCDEF".find(self.x[0])]

###2
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
        a, b = self.modelo[1], self.modelo[2]
        c, d, e, f = self.modelo[3], self.modelo[4], self.modelo[5], self.modelo[6]

        if a==b==c==d==e==f == 'limpio':
            acción = 'nada'
        elif situación == 'sucio':
            acción = 'limpiar'

        #return ('nada' if a == b == 'limpio' else
        #        'limpiar' if situación == 'sucio' else
        #        'ir_A' if robot == 'B' else 'ir_B')


# Requiere el modulo entornos_o.py
# Usa el modulo doscuartos_o.py para reutilizar código
# Agrega los modulos que requieras de python
