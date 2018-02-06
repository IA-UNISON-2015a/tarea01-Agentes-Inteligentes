#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
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
__author__ = 'Victor Ariel Noriega Ortiz' 

import entornos_o


# Requiere el modulo entornos_o.py
# Usa el modulo doscuartos_o.py para reutilizar código
# Agrega los modulos que requieras de python

class SeisCuartos(entornos_o.Entorno):
    """
    

    El estado se define como ((A,B,C,D,E,F),robot)
    robot puede tener algun valor del vector (A,B,C,D,E,F) 
    que indica en que cuarto esta
    Cada elemento en el arreglo de los cuartos puede tener el valor de "Limpio" o "Sucio"

    Los sensores es una tupla (robot, limpio?)
    con la ubicación del robot y el estado de limpieza

    """
    def __init__(self, x0=[["sucio","sucio","sucio","sucio","sucio","sucio"],"A"]):
        """
        Por default inicialmente el robot está en el A, y todos los cuartos
        están sucios

        """
        self.x = x0[:]
        self.desempeño = 0

    def acción_legal(self, acción):
        if self.x[1] is "A":
            return acción in ('limpiar', 'nada','ir_derecha','subir')
        elif self.x[1] is 'B':
            return acción in ('limpiar', 'nada', 'ir_derecha', 'ir_izquierda')
        elif self.x[1] is 'C':
            return acción in ('limpiar', 'nada', 'ir_izquerda', 'subir')
        elif self.x[1] is 'D':
            return acción in ('limpiar', 'nada', 'ir_derecha')
        elif self.x[1] is 'E':
            return acción in ('limpiar', 'nada', 'ir_derecha', 'ir_izquierda','bajar')
        elif self.x[1] is 'F':
            return acción in ('limpiar', 'nada', 'ir_izquierda')
        

    def transición(self, acción):
        if not self.acción_legal(acción):
            raise ValueError("La acción no es legal para este estado")
        
        if acción is "limpiar":
            self.x[" ABCDEF".find(self.x[1])] = "limpio"
            self.desempeño-=1
        elif acción is "ir_derecha":
            self.x[1] = chr(ord(self.x[1]) + 1)
            self.desempeño-=2
        elif acción is "ir_izquierda": 
            self.x[1] = chr(ord(self.x[1]) -1)
            self.desempeño-=2
        elif acción is "subir":
            self.x[1] = chr(ord(self.x[1]) + 3)
            self.desempeño-=3
        elif acción is 'bajar':
            self.x[1] = chr(ord(self.x[1]) -3)
            self.desempeño-=3

    def percepción(self):
        print(self.x[1])
        return self.x[1], self.x[" ABCDEF".find(self.x[1])]


class AgenteAleatorioSeisCuartos(entornos_o.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales

    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, percepcion):
        x = []
        cuarto, y = percepcion
        ### la variable y contendria el estado en el que se encuentra el cuarto pero eso no nos importa ahora mismo
        if cuarto is 'A':
            x = ['limpiar', 'nada', 'ir_Derecha', 'subir']
        elif cuarto is 'B':
            x = ['limpiar', 'nada', 'ir_Derecha', 'ir_Izquierda']
        elif cuarto is 'C':
            x = ['limpiar', 'nada', 'ir_Izquierda', 'subir']
        elif cuarto is 'D':
            x = ['limpiar', 'nada', 'ir_Derecha']
        elif cuarto is 'E':
            x = ['limpiar', 'nada', 'ir_Izquierda', 'ir_Derecha', 'bajar']
        elif cuarto is 'F':
            x = ['limpiar', 'nada', 'ir_Izquierda']
            
        random.shuffle(x)            
    
        accion = x[0]
        return accion


def test():
    """
    Prueba del entorno y los agentes

    """
    print("Prueba del entorno con un agente aleatorio")
    entornos_o.simulador(SeisCuartos(),
                         AgenteAleatorioSeisCuartos(['ir_A', 'ir_B', 'limpiar', 'nada']),
                         100)


if __name__ == "__main__":
    test()