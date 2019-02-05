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
__author__ = 'Xavier Paredes'

import entornos_o
import doscuartos_o 

from random import choice

# Requiere el modulo entornos_o.py
# Usa el modulo doscuartos_o.py para reutilizar código
# Agrega los modulos que requieras de python

class SeisCuartos (entornos_o.Entorno):
  """
    Clase para un entorno de seis cuartos, tres arriba y tres abajo.

    El estado se define como (robot, ABCDEF)
    donde robot puede tener los valores "A", "B", "C", "D", "E", "F"
    A, B, C, D, E, F pueden tener los valores "limpio", "sucio"

    Las acciones válidas en el entorno son ("ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada").

    Los sensores es una tupla (robot, limpio?)
    con la ubicación del robot y el estado de limpieza

  """

  def __init__(self, x0=["A", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]):
    self.x = x0[:]
    self.desempeño = 0

  def accion_legal(self, acción):
    return acción in ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]

  def transición(self, acción):
    robot, a, b, c, d, e, f = self.x
    if not self.acción_legal(acción):
      raise ValueError("La acción no es legal para este estado")

    if acción is "nada" and "sucio" in self.x:
      self.desempeño -= 1

    if acción is "limpiar":
      self.desempeño -= 1
      self.x[" ABCDEF".find(self.x[0])] = "limpio"
    
    elif acción is "nada" and "sucio" not in self.x:
      pass

    elif acción is "ir_Izquerda":
      if robot is 'A' or robot is 'D':
        pass
      else:
        self.desempeño -= 1
        if robot is 'B' or robot is 'C':
          self.x[0] =  list(" ABCDEF")[ " ABCDEF".find( self.x[0] ) - 1 ]
        elif robot is 'E' or robot is 'F':
          self.x[0] = list(" ABCDEF")[ " ABCDEF".find( self.x[0] ) - 1 ]
    
    elif acción is "ir_Derecha":
      self.desempeño -= 1
      if robot is 'C' or robot is 'F':
        pass
      else:
        if robot is 'A' or robot is 'B':
          self.x[0] = list(" ABCDEF")[ " ABCDEF".find( self.x[0] ) + 1 ]
        elif robot is 'D' or robot is 'E':
          self.x[0] = list(" ABCDEF")[" ABCDEF".find(self.x[0]) + 1]

    elif acción is "subir":
      self.desempeño -= 2
      if robot is 'A' or robot is 'B' or robot is 'C' :
        self.x[0] = list(" ABCDEF")[" ABCDEF".find(self.x[0]) + 3]

    elif acción is "bajar":
      self.desempeño -= 2
      if robot is 'D' or robot is 'E' or robot is 'F':
        self.x[0] = list(" ABCDEF")[" ABCDEF".find(self.x[0]) - 3]
      
  def percepción(self):
    return self.x[0], self.x[ " ABCDEF".find( self.x[0] ) ]
  
#INCISO 2
class AgenteReactivo(entornos_o.Agente):
    def __init__(self):
        self.modelo = {"robot":"A", "A":"sucio", "B":"sucio", "C":"sucio", "D":"sucio", "E":"sucio", "F":"sucio"}
    def programa(self,percepción):
        cuarto_actual, estado_actual = percepción

        self.modelo["robot"] = cuarto_actual
        self.modelo[cuarto_actual] = estado_actual

        if estado_actual is "sucio":
            return "limpiar"

        if not "sucio" in [self.modelo[i] for i in "ABCDEF"]: return "nada"
        if cuarto_actual in "ABC":
            if cuarto_actual in 'AC' and not("sucio" in [self.modelo[i] for i in "ABC"]):
                return "subir"
            elif cuarto_actual in "AB" and self.modelo["A"] == "limpio":
                return "ir_Derecha"
            elif cuarto_actual in "BC":
                return "ir_Izquierda"
        if cuarto_actual in "DEF":
            if cuarto_actual is 'E' and not "sucio" in [self.modelo[i] for i in "DEF"]:
                return "bajar"
            elif cuarto_actual in 'DE' and self.modelo["D"] == "limpio":
                return "ir_Derecha"
            elif cuarto_actual in "EF": 
                return "ir_Izquierda"

        return "nada"
class AgenteAleatorio(entornos_o.Agente):
	def __init__(self,acciones):
        self.acciones = acciones
    def programa(self, percepción):
        cuarto_actual = percepción[0]
        acciones = self.acciones[:]

        if cuarto_actual in "ABC":
            acciones.remove("bajar")
            if cuarto_actual is "B":    acciones.remove("subir")
            elif cuarto_actual is "A":  acciones.remove("ir_Izquierda")
            elif cuarto_actual is "C":  acciones.remove("ir_Derecha")
        elif cuarto_actual in "DEF":
            acciones.remove("subir")
            if cuarto_actual in "DF":   acciones.remove("bajar")
            if cuarto_actual is "D":  acciones.remove("ir_Izquierda")
            if cuarto_actual is "F":  acciones.remove("ir_Derecha")

        return random.choice(acciones)
	def test1(pasos = 100):
		print("Prueba en SeisCuartos con un agente aleatorio.")
		entornos_o.simulador(SeisCuartos(), AgenteAleatorio(['ir_Derecha', 'ir_Izquierda', 'subir', 'bajar', 'limpiar', 'nada']), pasos)

		print("Prueba en SeisCuartos con un agente reactivo basado en modelo.")
		entornos_o.simulador(SeisCuartos(), AgenteReactivo(), pasos)
#FIN INCISO 2
#INCISO 3
class DosCuartosCiego(entornos_o.Entorno):
    def __init__(self, x0=["A", "sucio", "sucio"]):
        self.x = x0[:]
        self.desempeño = 0

    def acción_legal(self, accion):
        return accion in ("ir_A", "ir_B", "limpiar", "nada")

    def transición(self, accion):
        if not self.acción_legal(accion):
            raise ValueError("La acción no es legal para este estado")

        robot, a, b = self.x
        if accion is not "nada" or a is "sucio" or b is "sucio":
            self.desempeño -= 1

        if accion is "limpiar":
            self.x[" AB".find(self.x[0])] = "limpio"
        elif accion is "ir_A":
            self.x[0] = "A"
        elif accion is "ir_B":
            self.x[0] = "B"

    def percepción(self):
        return self.x[0]

class AgenteRacional(entornos_o.Agente):
    def __init__(self):
        self.modelo = ['A', 'sucio', 'sucio']

    def programa(self, percepción):
        robot = percepción
        self.modelo[0] = robot
        situacion = self.modelo[' AB'.find(robot)]

        if situacion is "sucio":
            self.modelo[' AB'.find(robot)] = "limpio"
            return "limpiar"
        if self.modelo[1] == self.modelo[2] == "limpio": return "nada"
        if robot == "A": return "ir_B"
        else: return "ir_A"

def test2():
    print("Prueba del entorno DosCuartosCiego con un agente aleatorio")
    entornos_o.simulador(DosCuartosCiego(),doscuartos_o.AgenteAleatorio(['ir_A', 'ir_B', 'limpiar', 'nada']),100)

    print("Prueba del entorno DosCuartosCiego con un agente reactivo con modelo")
    entornos_o.simulador(DosCuartosCiego(), AgenteRacional(), 100)
#FIN INCISO 3
#INCISO 4
class DosCuartosEstocastico(entornos_o.Entorno):
    def __init__(self, x0=["A", "sucio", "sucio"]):
        self.x = x0[:]
        self.desempeño = 0

    def acción_legal(self, accion):
        return accion in ("ir_A", "ir_B", "limpiar", "nada")
    def transición(self, accion):
        if not self.acción_legal(accion):
            raise ValueError("La acción no es legal para este estado")

        robot, a, b = self.x
        if accion is not "nada" or a is "sucio" or b is "sucio":
            self.desempeño -= 1
        if accion is "limpiar":
            if random.random() <= 0.8:
                self.x[" AB".find(self.x[0])] = "limpio"
        elif accion is "ir_A":
            if random.random() <= 0.9:
                self.x[0] = "A"
        elif accion is "ir_B":
            if random.random() <= 0.9:
                self.x[0] = "B"

    def percepción(self):
        return self.x[0], self.x[" AB".find(self.x[0])]

class AgenteRacional_estocastico(entornos_o.Agente):
    def __init__(self):
        self.modelo = ['A', 'sucio', 'sucio']

    def programa(self, percepción):
        robot, situacion = percepción

        self.modelo[0] = robot
        self.modelo[' AB'.find(robot)] = situacion

        a, b = self.modelo[1], self.modelo[2]
        return ('nada' if a == b == 'limpio' else
                'limpiar' if situacion == 'sucio' else
                'ir_A' if robot == 'B' else 'ir_B')
def test3():
    print("Prueba del entorno estocastico con un agente aleatorio")
    entornos_o.simulador(DosCuartosEstocastico(),doscuartos_o.AgenteAleatorio(['ir_A', 'ir_B', 'limpiar', 'nada']),100)

    print("Prueba del entorno estocastico con un agente reactivo con modelo")
    entornos_o.simulador(DosCuartosEstocastico(), AgenteRacional_estocastico(), 100)
#FIN INCISO 4

if __name__ == "__main__":
    test1() #  prueba Ejercicio 1 y 2
    #test2() #  prueba Ejercicio 3
    #test3() #  prueba ejercicio 4