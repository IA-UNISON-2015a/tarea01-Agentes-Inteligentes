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
__author__ = 'Raúl Pérez'

import doscuartos_o
import entornos_o
from random import choice

# Requiere el modulo entornos_o.py
# Usa el modulo doscuartos_o.py para reutilizar código
# Agrega los modulos que requieras de python

class SeisCuartos(doscuartos_o.DosCuartos):
    """
    Clase para un entorno de seis cuartos.

    El estado se define como (robot, A, B, C, D, E, F)
    donde A, B y C son los pisos de abajo y D, E, y F son los de arriba,
    robot puede tener los valores de "A", "B", "C", "D", "E", "F"
    A, B, C, D, E y F pueden tener los valores "limpio" y "sucio"

    Las acciones válidas en el entorno son ("ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada").
    La acción de "subir" solo es legal en el piso de abajo, en los cuartos de los extremos, 
    mientras que la acción de "bajar" solo es legal en el piso de arriba y en el cuarto de el 
    centro (dos escaleras para subir, una escalera para bajar).

    Los sensores es una tupla (robot, limpio?)
    con la ubicación del robot y el estado de limpieza
    """  
    def __init__(self, x0=["F", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]):
        """
        Por default inicialmente el robot está en B y todos los cuartos
        están sucios
        """
        self.x = x0[:]
        self.desempeño = 0

    def acción_legal(self, acción):
        robot = self.x[0]

        return (True if acción is "subir" and robot in ("A", "C") 
            or acción is "bajar" and robot is "E"
            or acción in ("ir_Derecha", "ir_Izquierda", "limpiar", "nada")
            else False)

    def transición(self, acción):
        if not self.acción_legal(acción):
            raise ValueError("La acción no es legal para este estado")

        robot, a, b, c, d, e, f = self.x

        if acción is "subir":
            self.desempeño -= 2
            self.x[0] = "D" if robot is "A" else "F"
        elif acción is "bajar":
            self.desempeño -= 2
            self.x[0] = "B"
        elif acción is not "limpiar" or "sucio" in (a, b, c, d, e, f):
            self.desempeño -= 1
        
        if acción is "limpiar":
            self.desempeño -= .5
            self.x[" ABCDEF".find(self.x[0])] = "limpio"
        elif acción is "ir_Derecha":
            self.x[0] = ("B" if robot is "A"
                   else "C" if robot is "B"
                   else "E" if robot is "D"
                   else "F" if robot is "E"
                   else robot)
        elif acción is "ir_Izquierda":
            self.x[0] = ("A" if robot is "B"
                   else "B" if robot is "C"
                   else "D" if robot is "E"
                   else "E" if robot is "F"
                   else robot)

    def percepción(self):
        return self.x[0], self.x[" ABCDEF".find(self.x[0])]
        
class AgenteReactivoModeloSeisCuartos():
    """
    Un agente reactivo basado en modelo para el entorno seis cuartos
    """
    def __init__(self, modelo=['F', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio']):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = modelo[:]    
            
    def programa(self, percepción):
        robot, situación = percepción

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[' ABCDEF'.find(robot)] = situación

        _ ,a, b, c, d, e, f = self.modelo

        return ('nada' if (a == b == c == d == e == f == 'limpio') 
            else 'limpiar' if (situación == 'sucio')
            else 'ir_Derecha' if (robot is "A") and ('sucio' in (b, c))
            else 'ir_Derecha' if (robot is "B") and ((c is 'sucio') and (a is 'limpio'))
            else 'ir_Izquierda' if (robot is "C") and ('sucio' in (a, b))
            else 'ir_Izquierda' if (robot is "B") and ((a is 'sucio') and (c is 'limpio'))
            else choice(['ir_Derecha', 'ir_Izquierda']) if (robot is "B") and ((a == c == 'sucio') or ('sucio' in (d, e, f)))
            else 'subir' if (robot in ("A", "C")) and ('sucio' in (d, e, f))
            else 'ir_Derecha' if (robot is "D") and (('sucio' in (e, f)) or ('sucio' in (a, b, c)))
            else 'ir_Derecha' if (robot is "E") and ((f is 'sucio') and (d is 'limpio'))
            else 'ir_Izquierda' if (robot is "F") and (('sucio' in (d, e)) or ('sucio' in (a, b, c)))
            else 'ir_Izquierda' if (robot is "E") and ((d is 'sucio') and (f is 'limpio'))
            else choice(['ir_Derecha', 'ir_Izquierda']) if (robot is "E") and (d == f == 'sucio')
            else 'bajar' if (robot is "E") and ('sucio' in (a, b, c))
            else 'nada')
        
class AgenteAleatorio(doscuartos_o.AgenteAleatorio):
    
    def programa(self, percepción):
        return choice(self.acciones)

def test():
    """
    Prueba del entorno y los agentes

    """
    #print("Prueba del entorno seis cuartos con un agente basado en modelo")
    #entornos_o.simulador(SeisCuartos(), AgenteReactivoModeloSeisCuartos(), 100)

    print("Prueba del entorno seis cuartos con un agente basado en modelo")
    entornos_o.simulador(SeisCuartos(), AgenteAleatorio(["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]), 100)

if __name__ == "__main__":
    test()

        