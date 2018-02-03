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
__author__ = 'CesarSalazar'

import entornos_o

# Requiere el modulo entornos_o.py
# Usa el modulo doscuartos_o.py para reutilizar código
# Agrega los modulos que requieras de python

from doscuartos_o import DosCuartos, AgenteAleatorio, AgenteReactivoDoscuartos, AgenteReactivoModeloDosCuartos

from random import choice

"""

EJERCICIO 1

Clase 6 cuartos con 3 pisos arriba y 3 abajo

"""

class SeisCuartos(entornos_o.Entorno):
  #A B C cuartos de abajo y D E F arriba en ese orden
  #se inicia en A y con todos los cuartos sucios
    def __init__(self, x0 = ["A", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]):
        self.x = x0[:]
        self.desempeño = 0

    """
      La acción de `"subir"` solo es legal en el piso de abajo, en los cuartos de los extremos, 
      mientras que la acción de `"bajar"` solo es legal en el piso de arriba y en el cuarto de el centro (dos
      escaleras para subir, una escalera para bajar).
    """
    def acción_legal(self, acción):
        if acción == "subir" and (self.x[0] == "A" or self.x[0] == "C"):
          return True
        if acción == "bajar" and self.x[0] == "E":
          return True
        
        return acción in ("ir_Derecha", "ir_Izquierda", "limpiar", "nada")

    def transición(self, acción):
        ##ver si es legal
        if not self.acción_legal(acción):
            #raise ValueError("La acción no es legal para este estado")
            self.desempeño-=5
            return

        robot, a, b, c, d ,e ,f = self.x
        ##desempeño
        if acción == "subir" or acción == "bajar":
          self.desempeño-=4
        elif acción == "ir_Derecha" or acción == "ir_Izquierda":
          self.desempeño-=2
        elif acción == "limpiar" or a == "sucio" or b == "sucio" or c == "sucio" or d == "sucio" or e == "sucio" or f == "sucio":  
          self.desempeño-=1

        #modificar
        if acción == "limpiar":
            self.x[" ABCDEF".find(robot)] = "limpio"
        elif acción == "ir_Derecha":
          if robot == "A":
            self.x[0] = "B"
          elif robot == "B":
            self.x[0] = "C"
          elif robot == "D":
            self.x[0] = "E"
          elif robot == "E":
            self.x[0] = "F"
        elif acción == "ir_Izquierda":
          if robot == "B":
            self.x[0] = "A"
          elif robot == "C":
            self.x[0] = "B"
          elif robot == "E":
            self.x[0] = "D"
          elif robot == "F":
            self.x[0] = "E"
        elif acción == "subir":
          if robot == "A":
            self.x[0] = "D"
          else:
            self.x[0] = "F"
        elif acción == "bajar":
          self.x[0] = "B"
          
    def percepción(self):
        return self.x[0], self.x[" ABCDEF".find(self.x[0])]

"""
EJERCICIO 2

  Diseña un Agente reactivo basado en modelo para este entorno y
  compara su desempeño con un agente aleatorio despues de 100 pasos
  de simulación.

"""
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
        #SI esta limpio ya no hacer nada
        if not 'sucio' in self.modelo:
          return 'nada'
        #SI puede limpiar que limpie  
        if situación == 'sucio':
          return 'limpiar'  
        #si esta en el piso de abajo  
        if robot in ('A','B','C'):
          #si esta limpio el piso
          if not 'sucio' in self.modelo[1:4]:
            return 'subir' if robot == 'A' or robot == 'C' else 'ir_Izquierda'
          #si no esta limpio el piso
          else:
            return 'ir_Derecha' if robot == 'A' or self.modelo[1] == 'limpio' else 'ir_Izquierda'    
        #piso de arriba
        else:
          #si el piso esta limpio
          if not 'sucio' in self.modelo[4:]:
            return 'bajar' if robot == 'E' else 'ir_Derecha' if robot == 'D' else 'ir_Izquierda'
          #si hya algo sucio en el piso
          else:
            return 'ir_derecha' if  robot == 'D' or self.modelo[4] == 'limpio' else 'ir_Izquierda'
"""

EJERCICIO 3

   Al ejemplo original de los dos cuartos, modificalo de manera que el
   agente solo pueda saber en que cuarto se encuentra pero no sabe si
   está limpio o sucio.

   A este nuevo entorno llamalo `DosCuartosCiego`.

   Diseña un agente racional para este problema, pruebalo y comparalo
   con el agente aleatorio.

"""
class DosCuartosCiego(entornos_o.Entorno):
    """
    Clase para un entorno de dos cuartos donde el agente es ciego?

    """
    def __init__(self, x0=["A", "sucio", "sucio"]):
        """
        Por default inicialmente el robot está en A y los dos cuartos
        están sucios

        """
        self.x = x0[:]
        self.desempeño = 0

    def acción_legal(self, acción):
        return acción in ("ir_A", "ir_B", "limpiar", "nada")

    def transición(self, acción):
        if not self.acción_legal(acción):
            raise ValueError("La acción no es legal para este estado")

        robot, a, b = self.x
        if acción is not "nada" or a == "sucio" or b == "sucio":
            self.desempeño -= 1
        if acción == "limpiar":
            self.x[" AB".find(robot)] = "limpio"
        elif acción == "ir_A":
            self.x[0] = "A"
        elif acción == "ir_B":
            self.x[0] = "B"

    def percepción(self):
      #solo sabe en que cuarto esta
        return self.x[0]


"""
Funcion para probar
"""
def test():
    """
    Prueba del entorno y los agentes

    """
    print("Prueba del entorno  SeisCuartos con un agente aleatorio")
    entornos_o.simulador(SeisCuartos(["A", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]),
                         AgenteAleatorio(['ir_Derecha', 'ir_Izquierda', 'limpiar', 'nada','subir', 'bajar']),
                         100)
    print("Prueba del entorno con un agente reactivo con modelo para Seis cuartos")
    entornos_o.simulador(SeisCuartos(["A", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]), AgenteReactivoModeloSeisCuartos(), 100)

if __name__ == "__main__":
    test()
