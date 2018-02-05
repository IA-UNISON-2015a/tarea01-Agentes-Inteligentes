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
__author__ = 'Francisco Javier Vicente Tequida'

import entornos_o
import random

# Requiere el modulo entornos_o.py
# Usa el modulo doscuartos_o.py para reutilizar código
# Agrega los modulos que requieras de python

# # # -------------------------------------------------------------------------------------------------------------
# # # PROBLEMA 4
# # # -------------------------------------------------------------------------------------------------------------
class DosCuartosEstocástico(entornos_o.Entorno):
   """
   Clase para un entorno de dos cuartos. Muy sencilla solo regrupa métodos.

   El estado se define como (robot, A, B)
   donde robot puede tener los valores "A", "B"
   A y B pueden tener los valores "limpio", "sucio"

   Las acciones válidas en el entorno son ("ir_A", "ir_B", "limpiar", "nada").
   Todas las acciones son válidas en todos los estados.

   Los sensores es una tupla (robot, limpio?)
   con la ubicación del robot y el estado de limpieza

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
      
      random.seed()
      # Es durante la transición donde se evalua si se realizará la acción.
      # Hay una probabilidad de que la acción no se realice dejando la situación como está pero elevando el costo
      robot, a, b = self.x
      if acción is not "nada" or a is "sucio" or b is "sucio":
         self.desempeño -= 1
      if acción is "limpiar" and random.random() >= 0.2:
         self.x[" AB".find(self.x[0])] = "limpio"
      elif acción is "ir_A" and random.random() >= 0.1:
         self.x[0] = "A"
      elif acción is "ir_B" and random.random() >= 0.1:
         self.x[0] = "B"

   def percepción(self):
      return self.x[0], self.x[" AB".find(self.x[0])]

class AgenteAleatorioEstocástico(entornos_o.Agente):
   """
   Un agente que solo regresa una accion al azar entre las acciones legales
   """
   def __init__(self, acciones):
      self.acciones = acciones

   def programa(self, percepcion):
      return random.choice(self.acciones)

class AgenteReactivoModelDoscuartosEstocástico(entornos_o.Agente):
   """
   Un agente reactivo basado en modelo
   """
   def __init__(self):
      """
      Inicializa el modelo interno en el peor de los casos
      """
      self.modelo = ['A', 'sucio', 'sucio']

   def programa(self, percepción):
      """
      @param percepción situación en la que se encuentra el modelo habitación / estado de la habitación

      @return ('nada' if a == b == 'limpio' else
            'limpiar' if situación == 'sucio' else
            'ir_A' if robot == 'B' else 'ir_B') donde cada una de las opciones es una acción
                                                aplicable por el agente
      """
      robot, situación = percepción

      # Actualiza el modelo interno
      self.modelo[0] = robot
      self.modelo[' AB'.find(robot)] = situación

      # Decide sobre el modelo interno
      a, b = self.modelo[1], self.modelo[2]
      return ('nada' if a == b == 'limpio' else
            'limpiar' if situación == 'sucio' else
            'ir_A' if robot == 'B' else 'ir_B')

def TestEstocástico():
   entornos_o.simulador(DosCuartosEstocástico(),AgenteAleatorioEstocástico(['ir_A', 'ir_B', 'limpiar', 'nada']),100)
   entornos_o.simulador(DosCuartosEstocástico(),AgenteReactivoModelDoscuartosEstocástico(),100)

# # # -------------------------------------------------------------------------------------------------------------
# # # PROBLEMA 3
# # # -------------------------------------------------------------------------------------------------------------
class DosCuartosCiego(entornos_o.Entorno):
   """
   Clase para un entorno de dos cuartos. Muy sencilla solo regrupa métodos.

   El estado se define como (robot, A, B)
   donde robot puede tener los valores "A", "B"
   A y B pueden tener los valores "limpio", "sucio"

   Las acciones válidas en el entorno son ("ir_A", "ir_B", "limpiar", "nada").
   Todas las acciones son válidas en todos los estados.

   Los sensores es una tupla (robot, limpio?)
   con la ubicación del robot y el estado de limpieza

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
      if acción is not "nada" or a is "sucio" or b is "sucio":
         self.desempeño -= 1
      if acción is "limpiar":
         self.x[" AB".find(self.x[0])] = "limpio"
      elif acción is "ir_A":
         self.x[0] = "A"
      elif acción is "ir_B":
         self.x[0] = "B"

   def percepción(self):
      return self.x[0]

class AgenteAleatorioCiego(entornos_o.Agente):
   """
   Un agente que solo regresa una accion al azar entre las acciones legales
   """
   def __init__(self, acciones):
      self.acciones = acciones

   def programa(self, percepcion):
      return random.choice(self.acciones)

class AgenteReactivoModeloDosCuartosCiego(entornos_o.Agente):
   """
   Un agente reactivo basado en modelo
   """
   def __init__(self):
      """
      Inicializa el modelo interno en el peor de los casos
      """
      self.modelo = ['A', 'sucio', 'sucio']

   def programa(self, percepción):
      robot = percepción

      # Actualiza el modelo interno
      self.modelo[0] = robot

      # Decide sobre el modelo interno
      a, b = self.modelo[1], self.modelo[2]
      acción = 'nada'
      
      if a == b == 'limpio':
         acción = 'nada'
      elif self.modelo[' AB'.find(robot)] is 'sucio':
         acción = 'limpiar'
         # Actualiza el modelo interno y ahora asume que la habitación actual está limpia
         self.modelo[' AB'.find(robot)] = 'limpio'
      elif robot is 'B':
         acción = 'ir_A'
      else:
         acción = 'ir_B'
      
      return acción

def TestCiego():
   entornos_o.simulador(DosCuartosCiego(),AgenteAleatorioCiego(['ir_A', 'ir_B', 'limpiar', 'nada']),100)
   entornos_o.simulador(DosCuartosCiego(),AgenteReactivoModeloDosCuartosCiego(),100)

# # # -------------------------------------------------------------------------------------------------------------
# # # PROBLEMA 1
# # # -------------------------------------------------------------------------------------------------------------
class SeisCuartos(entornos_o.Entorno):
   """
   Clase para un entorno de seis cuartos. Muy sencilla solo regrupa métodos.

   El estado se define como (robot, A, B,C,D,E,F)
   donde robot puede tener los valores "A", "B", "C", "D", "E", "F"
   A, B, C, D, E, F pueden tener los valores "limpio", "sucio"

   Las acciones válidas en el entorno en general son 
   ("ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada")
   pero dependiendo de la habitación hay acciones específicas realizables por el agente.

   Los sensores es una tupla (robot, limpio?)
   con la ubicación del robot y el estado de limpieza

   """
   def __init__(self, x0=["A","sucio","sucio","sucio","sucio","sucio","sucio"]):
      """
      Por default inicialmente el robot está en A y los seis cuartos
      están sucios
      """
      self.x = x0[:]
      self.desempeño = 0

   def acción_legal(self, acción):
      if self.x[0] is 'A':
         return acción in ('limpiar', 'nada', 'ir_Derecha', 'subir')
      elif self.x[0] is 'B':
         return acción in ('limpiar', 'nada', 'ir_Derecha', 'ir_Izquierda')
      elif self.x[0] is 'C':
         return acción in ('limpiar', 'nada', 'ir_Izquierda', 'subir')
      elif self.x[0] is 'D':
         return acción in ('limpiar', 'nada', 'ir_Derecha')
      elif self.x[0] is 'E':
         return acción in ('limpiar', 'nada', 'ir_Izquierda', 'ir_Derecha', 'bajar')
      elif self.x[0] is 'F':
         return acción in ('limpiar', 'nada', 'ir_Izquierda')

   def función_costo(self, acción):
      if acción is 'limpiar':
         self.desempeño -= 1
      elif acción is 'ir_Izquierda' or acción is 'ir_Derecha':
         self.desempeño -= 2
      elif acción is 'subir' or acción is 'bajar':
         self.desempeño -= 3
      # Remover este caso
      else:
         self.desempeño -= 0

   def transición(self, acción):
      if not self.acción_legal(acción):
         raise ValueError("La acción no es legal para este estado")

      robot, a, b, c, d, e, f = self.x
      
      if acción is "limpiar":
         self.x[" ABCDEF".find(self.x[0])] = "limpio"
      elif acción is "ir_Derecha":
         self.x[0] = chr(ord(self.x[0]) + 1)
      elif acción is "ir_Izquierda":
         self.x[0] = chr(ord(self.x[0]) - 1)
      elif acción is 'subir':
         self.x[0] = chr(ord(self.x[0]) + 3)
      elif acción is 'bajar':
         self.x[0] = chr(ord(self.x[0]) - 3)

      self.función_costo(acción)

   def percepción(self):
      return self.x[0], self.x[" ABCDEF".find(self.x[0])]
   
   def percepción_para_aleatorio(self):
      return self.x[0]

class AgenteAleatorioSeisCuartos(entornos_o.Agente):
   """
   Un agente que solo regresa una accion al azar entre las acciones legales
   """
   def __init__(self):
      self.acciones = []

   def elección(self, percepcion):
      # Nunca se usa la variable 'situación'
      habitación, situación = percepcion

      x = []
      if habitación is 'A':
         x = ['limpiar', 'nada', 'ir_Derecha', 'subir']
      elif habitación is 'B':
         x = ['limpiar', 'nada', 'ir_Derecha', 'ir_Izquierda']
      elif habitación is 'C':
         x = ['limpiar', 'nada', 'ir_Izquierda', 'subir']
      elif habitación is 'D':
         x = ['limpiar', 'nada', 'ir_Derecha']
      elif habitación is 'E':
         x = ['limpiar', 'nada', 'ir_Izquierda', 'ir_Derecha', 'bajar']
      elif habitación is 'F':
         x = ['limpiar', 'nada', 'ir_Izquierda']
      random.shuffle(x)

      acción = x[0]
      return acción

   def programa(self, percepcion):
      return self.elección(percepcion)

# # # -------------------------------------------------------------------------------------------------------------
# # # PROBLEMA 2
# # # -------------------------------------------------------------------------------------------------------------

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
      a, b, c, d, e, f = self.modelo[1], self.modelo[2], self.modelo[3], self.modelo[4], self.modelo[5], self.modelo[6]
      acción = 'nada'

      primera_planta = [a,b,c]
      segunda_planta = [d,e,f]

      # Buscar la acción de acuerdo con el estado de las habitaciones continuas
      if a == b == c == d == e == f == 'limpio':
         acción = 'nada'
      elif situación is 'sucio':
         acción = 'limpiar'
      elif self.modelo[0] is 'A':
         if self.modelo[(' ABCDEF').find('B')] is 'limpio' and self.modelo[(' ABCDEF').find('C')] is 'limpio':
            acción = 'subir'
         else:
            acción = 'ir_Derecha'
      elif self.modelo[0] is 'B':
         if self.modelo[(' ABCDEF').find('A')] is 'sucio':
            acción = 'ir_Izquierda'
         else:
            acción = 'ir_Derecha'
      elif self.modelo[0] is 'C':
         if self.modelo[(' ABCDEF').find('A')] is 'limpio' and self.modelo[(' ABCDEF').find('B')] is 'limpio':
            acción = 'subir'
         else:
            acción = 'ir_Izquierda'
      elif self.modelo[0] is 'D':
         if self.modelo[(' ABCDEF').find('E')] is 'sucio' or self.modelo[(' ABCDEF').find('F')] is 'sucio':
            acción = 'ir_Derecha'
         if any(cuarto is 'sucio' for cuarto in primera_planta):
            acción = 'ir_Derecha'
      elif self.modelo[0] is 'E':
         if self.modelo[(' ABCDEF').find('D')] is 'sucio':
            acción = 'ir_Izquierda'
         elif self.modelo[(' ABCDEF').find('F')] is 'sucio':
            acción = 'ir_Derecha'
         else:
            acción = 'bajar'
      elif self.modelo[0] is 'F':
         if self.modelo[(' ABCDEF').find('D')] is 'sucio' or self.modelo[(' ABCDEF').find('E')] is 'sucio':
            acción = 'ir_Izquierda'
         if any(cuarto is 'sucio' for cuarto in primera_planta):
            acción = 'ir_Izquierda'
      return acción

def TestSeisCuartos():
   entornos_o.simulador(SeisCuartos(),AgenteAleatorioSeisCuartos(),100)
   entornos_o.simulador(SeisCuartos(),AgenteReactivoModeloSeisCuartos(),100)

if __name__ == "__main__":
   #TestEstocástico()
   #TestCiego()
   TestSeisCuartos()