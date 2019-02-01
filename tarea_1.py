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
__author__ = 'Ariana Sánchez.'

import entornos_o
from random import choice

class NueveCuartos(entornos_o.Entorno):
    """
    Clase para un entorno de dos cuartos. Muy sencilla solo regrupa métodos.

    El estado se define como (robot, piso, A, B, C, D, E, F, G, H, I)
    donde robot puede tener los valores "A", "B", "C", "D", "E", "F", "G", "H", "I"

    Las acciones válidas en el entorno son ("ir_izquierda", "ir_derecha", "subir", "bajar", "limpiar", "nada").
    Las restricciones son:
        Solo se puede subir de piso del lado derecho
        Solo se puede bajar de piso del lado izquierdo
        No se puede subir otro piso estando en el tercero
        No se puede bajar otro piso estando en el primero

    Los sensores es una tupla (robot, limpio?)
    con la ubicación del robot y el estado de limpieza

    """
    def __init__(self, x0=["A", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]):
        self.x = x0[:]
        self.desempeño = 0
        
    def acción_legal(self, acción):
        if self.x[0] == "A":
            return acción in ("ir_Derecha", "limpiar", "nada")
        elif self.x[0] == "C" or self.x[0] == "F":
            return acción in ("ir_Izquierda", "subir", "limpiar", "nada")
        elif self.x[0] == "D":
            return acción in ("ir_Derecha", "bajar", "limpiar", "nada")
        elif self.x[0] == "G":
            return acción in ("ir_Derecha", "bajar", "limpiar", "nada")
        elif self.x[0] == "I":
            return acción in ("ir_Izquierda", "limpiar", "nada")
        elif self.x[0] == "B" or self.x[0] == "E" or self.x[0] == "H":
            return acción in ("ir_Derecha", "ir_Izquierda", "limpiar", "nada")

    def transición(self, acción):
        if not self.acción_legal(acción):
            raise ValueError("La acción no es legal para este estado")

        robot, a, b, c, d, e, f, g, h, i = self.x
        if acción is not "nada" or a is "sucio" or b is "sucio" or c is "sucio" or d is "sucio" or e is "sucio" or f is "sucio" or g is "sucio" or h is "sucio" or i is "sucio":
            self.desempeño -= 1
            
        if acción is "limpiar":
            self.x[" ABCDEFGHI".find(self.x[0])] = "limpio"
            
        elif acción is "ir_Derecha":
            if self.x[0] == "A":
                self.x[0] = "B"
                self.desempeño-=1
            elif self.x[0] == "B":
                self.x[0] = "C"
                self.desempeño-=1
            elif self.x[0] == "D":
                self.x[0] = "E"
                self.desempeño-=1
            elif self.x[0] == "E":
                self.x[0] = "F"
                self.desempeño-=1
            elif self.x[0] == "G":
                self.x[0] = "H"
                self.desempeño-=1
            elif self.x[0] == "H":
                self.x[0] = "I"
                self.desempeño-=1
                
        elif acción is "ir_Izquierda":
            
            if self.x[0] == "C":
                self.x[0] = "B"
                self.desempeño-=1
            elif self.x[0] == "B":
                self.x[0] = "A"
                self.desempeño-=1
            elif self.x[0] == "F":
                self.x[0] = "E"
                self.desempeño-=1
            elif self.x[0] == "E":
                self.x[0] = "D"
                self.desempeño-=1
            elif self.x[0] == "I":
                self.x[0] = "H"
                self.desempeño-=1
            elif self.x[0] == "H":
                self.x[0] = "G"
                self.desempeño-=1
            
        elif acción is "subir":
            if self.x[0] == "C":
                self.x[0] = "F"
                self.desempeño-=2
            elif self.x[0] == "F":
                self.x[0] == "I"
                self.desempeño-=2
                
        elif acción is "bajar":
            if self.x[0] == "G":
                self.x[0] = "D"
                self.desempeño-=2
            elif self.x[0] == "D":
                self.x[0] == "A"
                self.desempeño-=2

    def percepción(self):
        return self.x[0], self.x[" ABCDEFGHI".find(self.x[0])]


class AgenteAleatorio(entornos_o.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales

    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, percepcion):
        return choice(self.acciones)


class AgenteReactivoModeloNueveCuartos(entornos_o.Agente):
    """
    Un agente reactivo basado en modelo

    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = ['A', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio']

    def programa(self, percepción):
        robot, situación = percepción

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[' ABCDEFGHI'.find(robot)] = situación

        # Decide sobre el modelo interno
        a, b, c, d, e, f, g, h, i = self.modelo[1], self.modelo[2], self.modelo[3], self.modelo[4], self.modelo[5], self.modelo[6], self.modelo[7], self.modelo[8], self.modelo[9]
        return ('nada' if a == b == c == d == e == f == g == h == i == 'limpio' else
                'limpiar' if situación == 'sucio' else
                'ir_Derecha' if robot == 'B' or robot == 'A' else 
                'ir_Izquierda' if robot == 'E' or robot == 'F' else
                'ir_Derecha' if self.modelo[' ABCDEFGHI'.find(3)] == 'limpio' or self.modelo[' ABCDEFGHI'.find(4)] == 'limpio' else
                'subir' if robot == 'C' or robot == 'F' else
                'bajar' if robot == 'G' or robot == 'D' else
                'nada')

class NueveCuartosCiego():
    def __init__(self, x0=["A", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]):
        self.x = x0[:]
        self.desempeño = 0
        
    def acción_legal(self, acción):
        return acción in ("", )
    
    
def test():
    """
    Prueba del entorno y los agentes
    
    """
    print("Prueba del entorno con un agente aleatorio")
    entornos_o.simulador(NueveCuartos(), AgenteAleatorio(["ir_Izquierda", "ir_Derecha", "limpiar", "nada", "subir", "bajar"]), 10)
    
    print("Prueba del entorno con un agente reactivo con modelo")
    entornos_o.simulador(NueveCuartos(), AgenteReactivoModeloNueveCuartos(), 100)


if __name__ == "__main__":
    test()

# Requiere el modulo entornos_o.py
# Usa el modulo doscuartos_o.py para reutilizar código
# Agrega los modulos que requieras de python
