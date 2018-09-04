#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Tarea de desarrollo de entornos y agentes
==========================================

1. Desarrolla un entorno similar al de los dos cuartos (el cual se
   encuentra en el modulo doscuartos_o.py), pero con tres cuartos en
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
__author__ = 'Fabian Encinas Silvas'
from random import choice,random
import entornos_o
import doscuartos_o

# Requiere el modulo entornos_o.py
# Usa el modulo doscuartos_o.py para reutilizar código
# Agrega los modulos que requieras de python

#los cuartos se verian de este modo
# F E D
# A B C
class SeisCuartos(doscuartos_o.DosCuartos):
    def __init__(self, x0=["A","sucio","sucio","sucio","sucio", "sucio", "sucio"]):
     
        self.x = x0[:]
        self.desempenio = 0

    def percepcion(self):
        return self.x[0], self.x[" ABCDEF".find(self.x[0])]

    def accion_legal(self, accion ):

        percepcion = self.percepcion()
        
        lugar = percepcion[0]

        if lugar is "A":
            return accion in ("ir_derecha", "limpiar","subir",'nada')
        elif lugar is "B":
            return accion in ("ir_izquierda", "ir_der","nada", "limpiar")
        elif lugar is "C":
            return accion in ("ir_izquierda","nada", "limpiar","subir")
        elif lugar is "D":
            return accion in ("ir_izquierda","nada", "limpiar")
        elif lugar is "E":
            return accion in ( "ir_izquierda", "ir_der","nada", "limpiar","bajar")
        elif lugar is "F":
            return accion in ("ir_derecha", "nada", "limpiar")

    def saber_desempenio(self,accion):
        if accion is 'limpiar':
            self.desempenio -= 1
        elif accion is 'nada':
            if  any(cuarto is 'sucio' for cuarto in self.x[1:]) :
                self.desempenio -=2
        
        elif accion is 'ir_izquierda' or accion is 'ir_derecha':
            self.desempenio -=2
        elif accion is 'subir' or accion is 'bajar':
            self.desempenio -= 3
    def transicion(self,accion):
        self.saber_desempenio(accion)
        if accion is 'limpiar':
            self.x[" ABCDEF".find(self.x[0])] = 'limpio'

        if accion is 'ir_derecha':
            if self.x[0] is 'F':
                self.x[0]='E'
            elif self.x[0] is 'E':
                self.x[0]='D'
            elif self.x[0] is 'A':
                self.x[0]='B'
            elif self.x[0] is 'B':
                self.x[0]='C'
        
        if accion is 'ir_izquierda':
            if self.x[0] is 'D':
                self.x[0]='E'
            elif self.x[0] is 'E':
                self.x[0]='F'
            elif self.x[0] is 'F':
                self.x[0]='C'
            elif self.x[0] is 'C':
                self.x[0]='B'
            elif self.x[0] is 'B':
                self.x[0]='A'
        
        if accion is 'bajar':
            if self.x[0] is 'E':
                self.x[0]='B'
        if accion is 'subir':
            if  self.x[0] is 'A':
               self.x[0]='F'
            elif self.x[0] is 'C':
                self.x[0]= 'D'
            

class DosCuartosCiego(entornos_o.Entorno):
    
    def __init__(self, x0=["A", "sucio", "sucio"]):
        """
        Por default inicialmente el robot está en A y los dos cuartos
        están sucios
        """
        self.x = x0[:]
        self.desempenio = 0

    def accion_legal(self, acción):
        return acción in ("ir_izquierda", "ir_derecha", "limpiar", "nada")

    def transicion(self, acción):
        if not self.acción_legal(acción):
            raise ValueError("La acción no es legal para este estado")

        robot, a, b = self.x
        if acción is not "nada" or a is "sucio" or b is "sucio":
            self.desempenio -= 1
        if acción is "limpiar":
            self.limpiar(self.x[0])
        elif acción is "ir_izquierda":
            self.x[0] = "A"
        elif acción is "ir_derecha":
            self.x[0] = "B"
    def limpiar(self,target):
        self.x[" AB".find(target)] = "limpio"
    def percepcion(self):
        return self.x[0]



class AgenteAleatorioDosCuartosCiego(entornos_o.Agente):
    def __init__(self,x=['A','sucio','sucio']):
        self.x=x

    def programa(self,percepcion):
        lugar=percepcion
        situacion = self.x[" AB".find(lugar)]
        self.x[0] = lugar
        
        if all(cuarto is 'limpio' for cuarto in self.x[1:]):
            return "nada"
        if situacion is 'sucio':
            self.x[" AB".find(self.x[0])] = 'limpio'
            return "limpiar"
        if lugar is 'A':
            return "ir_derecha"
        else:
            return "ir_izquierda"

class AgenteAleatorioSeisCuartos(entornos_o.Agente):
    """
    Regresa una accion aleatoria entre las acciones legales
    """
    

    def accion_legal(self, lugar ):


        if lugar is "A":
            return ["ir_derecha", "limpiar","subir",'nada']
        elif lugar is "B":
            return ["ir_izquierda", "ir_der","nada", "limpiar"]
        elif lugar is "C":
            return  ["ir_izquierda","nada", "limpiar","subir"]
        elif lugar is "D":
            return ["ir_izquierda","nada", "limpiar"]
        elif lugar is "E":
            return ["ir_izquierda", "ir_der","nada", "limpiar","bajar"]
        elif lugar is "F":
            return ["ir_derecha", "nada", "limpiar"]
        
    def programa(self, percepcion):
        return choice(percepcion[0])



class AgenteReactivoSeisCuartos(entornos_o.Agente):
    def __init__(self,x=['A','sucio','sucio','sucio','sucio','sucio']):

        self.x = x
    def programa(self,percepcion):
        lugar_actual,situacion = percepcion #me devuelvo en donde estoy y si esta limpio o no
        self.x[0] = lugar_actual
        self.x[" ABCDEF".find(lugar_actual)] = situacion
        if all(cuarto is 'limpio' for cuarto in self.x[1:]):
            return 'nada'
        if situacion is 'sucio':
            return 'limpiar'
        
        if lugar_actual is 'A':
            if self.x[2] is 'sucio' or self.x[3] is'sucio':
                return 'ir_derecha'
            elif self.x[4] is 'sucio' or self.x[5] is 'sucio' or self.x[6] is 'sucio':
               return 'subir' 

        elif lugar_actual is 'B':
            
            if self.x[1] is 'sucio':
                return 'ir_izquierda'
            elif self.x[3] is 'sucio':
                return  'ir_derecha'
            
        elif lugar_actual is 'C':
            if self.x[1] is 'sucio':
                return 'ir_izquierda'
            elif self.x[2] is 'sucio':
                return 'ir_izquierda'
            if self.x[4] is 'sucio' or self.x[5] is 'sucio' or self.x[6] is 'sucio':
               return 'subir' 

        elif lugar_actual is 'D':
            if self.x[5] is 'sucio':
                return 'ir_izquierda'
            elif self.x[6] is 'sucio':
                return 'ir_izquierda'

        elif lugar_actual is 'E':
            print("Entre a esta madre")
            if self.x[4] is 'sucio':
                print("Entre al primer if")
                return 'ir_derecha'
            elif self.x[6] is 'sucio':
                print("Entre al segundo if")
                return 'ir_izquierda'
            elif self.x[1] is 'sucio' or self.x[2] is 'sucio' or self.x[3] is 'sucio':
               print("Entre a bajar ")
               return 'bajar' 

        elif lugar_actual is 'F':

            if self.x[5] is 'sucio':
                return 'ir_derecha'
            elif self.x[4] is 'sucio':
                return 'ir_derecha'


class DosCuartos(entornos_o.Entorno):
    
    def __init__(self, x0=["A", "sucio", "sucio"]):
        
        self.x = x0[:]
        self.desempenio = 0

    def accion_legal(self, acción):
        return acción in ("ir_izquierda", "ir_derecha", "limpiar", "nada")

    def transicion(self, acción):
        if not self.acción_legal(acción):
            raise ValueError("La acción no es legal para este estado")

        robot, a, b = self.x
        if acción is not "nada" or a is "sucio" or b is "sucio":
            self.desempenio -= 1
        if acción is "limpiar":
            self.x[" AB".find(self.x[0])] = "limpio"
        elif acción is "ir_izquierda":
            self.x[0] = "A"
        elif acción is "ir_derecha":
            self.x[0] = "B"

    def percepcion(self):
        return self.x[0], self.x[" AB".find(self.x[0])]

class AgenteEstocastico(entornos_o.Agente):
    """
    Un agente reactivo simple

    """
    def __init__(self, x= ["A","sucio","sucio"]):
        self.x = x
    def programa(self, percepcion):
        
        if all(cuarto is 'limpio' for cuarto in self.x[1:]):
            return 'nada'
        lugar, situacion = percepcion

        if situacion is 'sucio':
            if random() < 0.8 :
                return 'limpiar'
            else:
                return 'nada'
        if lugar is 'A':
            if random() < 0.9:
                return 'ir_derecha'
            else:
                return 'nada'
        if lugar is 'B':
            if random() < 0.9:
                return 'ir_izquierda'
            else: 
                return 'nada'
    

 
def test():
    print("Punto 1 y 2 ")
    #entornos_o.simulador(SeisCuartos(),AgenteReactivoSeisCuartos(),100)
    #entornos_o.simulador(DosCuartosCiego(),AgenteAleatorioDosCuartosCiego(),100)
    entornos_o.simulador(DosCuartos(),AgenteEstocastico(),100)
    #entornos_o.simulador(SeisCuartos(),AgenteAleatorio(),100)



test()