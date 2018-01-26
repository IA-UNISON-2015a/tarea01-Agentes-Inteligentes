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
__author__ = 'IvanAlejandroMorenoSoto'

import entornos_o
from doscuartos_o import DosCuartos, AgenteReactivoModeloDosCuartos, AgenteAleatorio

##############################################################

# Ejercicio 3.

class DosCuartosCiego(DosCuartos):
    """
    Entorno basado en DosCuartos donde el robot solo tiene
    acceso a su posición actual.
    """

    def percepción(self):
        """
        @return Únicamente la posición actual del robot.
        """
        return self.x[0]

class AgenteDosCuartosCiego(AgenteReactivoModeloDosCuartos):
    """
    Agente para el entorno DosCuartosCiego.
    """

    def programa(self, percepción):
        """
        Aquí, el robot decide que acción realizará según su memoria de la
        situación del cuarto donde está.

        @return Una de cuatro acciones de ['ir_A', 'ir_B', 'limpiar', 'nada'].
        """

        # Se actualiza el lugar actual del robot.
        self.modelo[0] = percepción

        # Revisa lo que recuerda sobre el cuarto en el que se encuentra.
        situación = self.modelo[' AB'.find(percepción)]

        a, b = self.modelo[1], self.modelo[2]

        if a == b == 'limpio':
            return 'nada'
        elif situación == 'sucio':
            # Antes de regresar la acción, se actualiza la memoria sobre
            # el cuarto actual.
            self.modelo[' AB'.find(percepción)] = 'limpio'
            return 'limpiar'
        elif percepción == 'B':
            return 'ir_A'
        else:
            return 'ir_B'

def hacerPruebaEjercicio3(pasos):
    """
    Prueba el AgenteDosCuartosCiego y el AgenteAleatorio (de doscuartos_o)
    en el entorno DosCuartosCiego.

    @param pasos: Número de pasos de la simulación.
    """

    print("Prueba en DosCuartosCiego con un agente aleatorio.")
    entornos_o.simulador(DosCuartosCiego(), AgenteAleatorio(['ir_A', 'ir_B', 'limpiar', 'nada']), pasos)

    print("Prueba en DosCuartosCiego con un agente racional.")
    entornos_o.simulador(DosCuartosCiego(), AgenteDosCuartosCiego(), pasos)

##############################################################

if __name__ == "__main__":
    hacerPruebaEjercicio3(100)
