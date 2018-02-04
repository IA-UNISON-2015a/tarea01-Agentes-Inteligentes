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
__author__ = 'Giovanni_Lopez_Celaya'

import entornos_o
from random import choice

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
        self.desempeño = 0

    def acción_legal(self, acción):
        return acción in ("ir_Der", "ir_Izq", "subir", "bajar", "limpiar", "nada")

    def transición(self, acción):
        try: 
            if not self.acción_legal(acción):
                raise ValueError("La acción '{}' no es legal para este estado".format(acción))
        except ValueError as v:
            print(v)
            return
        
        robot, a, b, c, d, e, f = self.x #Se asigna el lugar donde empezara el robot y las situaciones (sucio/limpio) de cada cuarto.

        if acción != "nada" or a is "sucio" or b is "sucio" or c is"sucio" or d is "sucio" or e is "sucio" or f is "sucio":
            if acción is "subir" or acción is "bajar":
                self.desempeño -= 2
            else:
                self.desempeño -= 1

        if acción is "limpiar":
            self.x[" ABCDEF".find(self.x[0])] = "limpio"
        # Posibles formas en que el robot se puede mover dependiendo de el cuarto en donde se encuentre.
        elif acción is "ir_Izq" and self.x[0] is "B" or acción is "bajar" and self.x[0] is "D":
            self.x[0] = "A"
        elif acción is "ir_Der" and self.x[0] is "A" or acción is "bajar" and self.x[0] is "E" or acción is "ir_Izq" and self.x[0] is "C":
            self.x[0] = "B"
        elif acción is "ir_Der" and self.x[0] is "B" or acción is "bajar" and self.x[0] is "F":
            self.x[0] = "C"
        elif acción is "subir" and self.x[0] is "C" or acción is "ir_Der" and self.x[0] is "E":
            self.x[0] = "F"
        elif acción is "subir" and self.x[0] is "B" or acción is "ir_Izq" and self.x[0] is "F" or acción is "ir_Der" and self.x[0] is "D":
            self.x[0] = "E"
        elif acción is "subir" and self.x[0] is "A" or acción is "ir_Izq" and self.x[0] is "E":
            self.x[0] = "D"

    def percepción(self):
        return self.x[0], self.x[" ABCDEF".find(self.x[0])]
    
class AgenteAleatorio(entornos_o.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales
    """

    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, percepción):
        return choice(self.acciones)

class AgenteReactivoSeiscuartos(entornos_o.Agente):
    """
    Un agente reactivo simple

    """
    def programa(self, percepción):
        robot, situación = percepción
        return ('limpiar' if situación == 'sucio' else
                'ir_Der' if robot == 'A' else 'ir_Der' if robot == 'B' else 'subir' if robot == 'C' else 'ir_Izq' if robot == 'F' else 'ir_Izq' if robot == 'E' else 'bajar')

def test():
    """
    Prueba del entorno y los agentes
    """
    print("Prueba del entorno con un agente aleatorio en seis cuartos.")
    entornos_o.simulador(SeisCuartos(),
              AgenteAleatorio(('ir_Der', 'ir_Izq', 'subir', 'bajar', 'limpiar', 'nada')),
             100)
    
    print("Prueba del entorno con un agente reactivo")
    entornos_o.simulador(SeisCuartos(), AgenteReactivoSeiscuartos(), 100)

if __name__ == "__main__":
    test()
    e = SeisCuartos()
# Requiere el modulo entornos_o.py
# Usa el modulo doscuartos_o.py para reutilizar código
# Agrega los modulos que requieras de python
