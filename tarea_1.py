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
   ["ir_derecha", "ir_izquierda", "subir", "bajar", "limpiar", "nada"]
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
from random import choice

from entornos_o import Entorno, Agente, simulador
from doscuartos_o import DosCuartos

__author__ = 'Ricardo E. Alvarado Mata'

class NueveCuartos(DosCuartos):
    """
    Clase que representa un entorno con nueve cuartos divididos
    en tres pisos donde los cuartos de la derecha permiten acceder
    a cuartos mas arriba, y los cuartos de la izquierda bajar. Los
    cuartos de enmedio solo pertiten moverse a los cuartos laterales.

    El estado se representa mediante (ren, col, matriz_de_cuartos)
    donde ren representa la posicion vertical en donde se encuentra el
    agente en los cuartos, y col la posicion horizontal, y matriz_de_cuartos
    es una matriz de 3x3 en la que se almacenan los estados de los cuartos,
    poniendo un 0 si el cuarto esta limpio y un 1 si esta sucio.

    Las acciones totales del entorno son:
    ["ir_derecha", "ir_izquierda", "subir", "bajar", "limpiar", "nada"]
    y depende del cuarto en donde se este algunas seran validas y otras no.
    Asi, solo se podra subir a un nivel mas alto, desde los cuartos de mas
    a la derecha y solo se podra bajar de los cuartos de mas a la izquierda
    y desde los cuartos de enmedio de cada nivel solo se podra mover a los
    cuartos laterales. Las acciones de limpiar y nada, seran validas en
    todos los cuartos.

    La persepcion es una tupla (ren, col, limpio?)
    donde ren y col dan la posicion del agente y limpio el estado del
    cuarto.
    """

    def __init__(self, x0 = [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1]):
        """
        Inicializa el entorno con el robot en la posicion 0,0
        y todos los cuartos sucios.
        """
        self.x = list(x0)
        self.desempeño = 0
    
    def acción_legal(self, acción):
        ren, col = self.x[0], self.x[1]
        try:
            return bool({
                'ir_izquierda': col,
                'ir_derecha': col<2,
                'subir': (col==2) * ren,
                'bajar': (col==0) * (ren<2),
                'limpiar': 1,
                'nada': 1
            }[acción])
        except:
            return False
    
    def transición(self, acción):
        if not self.acción_legal(acción):
            raise ValueError("La acción {} no es legal para el estado {}".format(acción, self.x))

        if acción == 'subir' or acción == 'bajar':
            self.desempeño -= 3
            self.x[0] += {'subir':-1, 'bajar':1}[acción]
        elif acción == 'ir_izquierda' or acción == 'ir_derecha':
            self.desempeño -= 2
            self.x[1] += {'ir_izquierda':-1, 'ir_derecha':1}[acción]
        elif acción == 'limpiar':
            self.desempeño -= 1
            self.x[2 + self.x[0]*3 + self.x[1]] = 0
        elif acción == 'nada' and 1 in self.x[2:]:
            self.desempeño -= 1
    
    def percepción(self):
        ren, col = self.x[0], self.x[1]
        matriz_de_cuartos = self.x[2:]
        print("ren: {}, col: {}".format(ren,col))
        return ren, col, matriz_de_cuartos[ren*3 + col]
    
class AgenteAleatorioNueveCuartos(Agente):
    def __init__(self):
        self.acciones = ["ir_derecha", "ir_izquierda", "subir", "bajar", "limpiar", "nada"]

    def programa(self, percepcion):
        c = choice(self.acciones)

        while not self.acción_legal(c, percepcion[0], percepcion[1]):
            c = choice(self.acciones)
        
        return c

    def acción_legal(self, acción, col, ren):
        try:
            return bool({
                'ir_izquierda': ren,
                'ir_derecha': ren<2,
                'subir': (ren==2) * col,
                'bajar': (ren==0) * (col<2),
                'limpiar': 1,
                'nada': 1
            }[acción])
        except:
            return False

class AgenteReactivoModeloNueveCuartos():
    def __init__(self):
        self.modelo = [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    def programa(self, percepción):
        self.ActualizarModelo(percepción)

        i, j = self.modelo[0], self.modelo[1]
        situacion = self.modelo[2 + i*3 + j]

        return ('nada' if not 1 in self.modelo[2:] else
                'limpiar' if situacion else
                'ir_derecha' if (i == 2 and (j == 0 or j == 1)) or
                (i == 1 and j == 1) else
                'ir_izquierda' if  (i == 0 and (j == 2 or j == 1)) or
                ((i == 1 and j == 2) and self.modelo[6]) else 
                'subir' if  j == 2 and (i == 2 or i == 1) else
                'bajar')


    def ActualizarModelo(self, percepción):
        i, j = percepción[0], percepción[1]
        self.modelo[0], self.modelo[1] = i, j
        self.modelo[2 + i*3 + j] = percepción[2]

if __name__ == "__main__":
    print("Prueba del entorno con un agente aleatorio")
    simulador(NueveCuartos(), AgenteAleatorioNueveCuartos(), 200)
    
    print("Prueba del entorno con un agente reactivo con modelo")
    simulador(NueveCuartos(), AgenteReactivoModeloNueveCuartos(), 100)

# Requiere el modulo entornos_o.py
# Usa el modulo doscuartos_o.py para reutilizar código
# Agrega los modulos que requieras de python
