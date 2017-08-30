#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Tarea de desarrollo de entornos y agentes
==========================================

En esta tarea realiza las siguiente acciones:

1.- Desarrolla un entorno similar al de los dos cuartos (el cual se encuentra
    en el módulo doscuartos_o.py), pero con tres cuartos en el primer piso,
    y tres cuartos en el segundo piso.

    El entorno se llamará SeisCuartos

    Las acciones totales serán

    ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]

    La acción de "subir" solo es legal en el piso de abajo (cualquier cuarto),
    y la acción de "bajar" solo es legal en el piso de arriba.

    Las acciones de subir y bajar son mas costosas en término de energía
    que ir a la derecha y a la izquierda, por lo que la función de desempeño
    debe de ser de tener limpios todos los cuartos, con el menor numero de
    acciones posibles, y minimozando subir y bajar en relación a ir a los
    lados.

2.- Diseña un Agente reactivo basado en modelo para este entorno y compara
    su desempeño con un agente aleatorio despues de 100 pasos de simulación.

3.- Al ejemplo original de los dos cuartos, modificalo de manera que el agente
    solo pueda saber en que cuarto se encuentra pero no sabe si está limpio
    o sucio.

    A este nuevo entorno llamalo DosCuartosCiego

    Diseña un agente racional para este problema, pruebalo y comparalo
    con el agente aleatorio.

4.- Reconsidera el problema original de los dos cuartos, pero ahora modificalo
    para que cuando el agente decida aspirar, el 80% de las veces limpie pero
    el 20% (aleatorio) deje sucio el cuarto. Diseña un agente racional
    para este problema, pruebalo y comparalo con el agente aleatorio.

    A este entorno llamalo DosCuartosEstocástico

Todos los incisos tienen un valor de 25 puntos sobre la calificación de
la tarea.

"""
__author__ = 'Erick Fernando López Fimbres'

import entornos_o
from random import choice

# Requiere el modulo entornos_o.py
# Usa el modulo doscuartos_o.py para reutilizar código
# Agrega los modulos que requieras de python

class SeisCuartos(entornos_o.Entorno):
    """
    Clase para un entorno de seis cuartos.

    El estado se define como (robot, A, B, C, D, E, F)
    donde robot puede tener los valores "A", "B", "C", "D", "E" y "F"
    A, B, C, D, E, F pueden tener los valores "limpio", "sucio"

    Las acciones válidas en el entorno son ("ir_Izquierda", "ir_Derecha", "limpiar", "nada") en
    cualquier cuarto ("subir") solo si se encuentra en los cuartos de abajo.
    ("bajar") solo si se encuentra en los cuartos de arriba ("D","E","F").
    
    Los sensores es una tupla (robot, limpio?)
    con la ubicación del robot y el estado de limpieza
    """
    
    def __init__(self, x0=["A", "sucio", "sucio","sucio", "sucio","sucio", "sucio"]):
        """
        Por default inicialmente el robot está en A y losdemas cuartos
        están sucios
        """
        
        self.x = x0[:]
        self.desempeño = 0

    def acción_legal(self, acción):
        acción_legal=True
        if(acción=="bajar" and (self.x[0]=="A" or self.x[0]=="B" or self.x[0]=="C")):
            acción_legal=False
        if(acción=="subir"and (self.x[0]=="D" or self.x[0]=="E" or self.x[0]=="F")):
            acción_legal=False
        return acción_legal

    def transición(self, acción):
        try:
            
            if not self.acción_legal(acción):
                raise ValueError("La acción",acción," no es legal para el estado",self.x[0])
            else:
                dic = {1:"A", 2:"B",3:"C",4:"D",5:"E",6:"F"}
                
                robot, a, b,c,d,e,f = self.x
                if(acción=="subir"):
                    self.x[0]=dic[" ABCDEF".find(robot)+3]
                    self.desempeño-=5
                elif(acción=="bajar"):
                    self.x[0]=dic[" ABCDEF".find(robot)-3]
                    self.desempeño-=5
                elif(acción=="ir_Derecha" and (robot!="C" and robot!="F")):
                    self.x[0]=dic[" ABCDEF".find(robot)+1]
                    self.desempeño-=1
                elif(acción=="ir_Izquierda" and (robot!="A" and robot!="D")):
                    self.x[0]=dic[" ABCDEF".find(robot)-1]
                    self.desempeño-=1
                elif acción is "limpiar":
                    self.x[" ABCDEF".find(self.x[0])] = "limpio"
                    self.desempeño -= 1
                elif (acción is "nada" and a is "sucio" or b is "sucio" or c is "sucio" or d is "sucio" or e is "sucio" or f is "sucio"):
                    self.desempeño -= 1
                else:
                    self.desempeño -= 0
                
        except Exception as error:
            print('Error: ' + repr(error))

    def percepción(self):
        return self.x[0], self.x[" ABCDEF".find(self.x[0])]

class AgenteAleatorio(entornos_o.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales

    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, percepcion):
        return choice(self.acciones)
    
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
        a, b, c, d, e, f = self.modelo[1], self.modelo[2],self.modelo[3], self.modelo[4],self.modelo[5], self.modelo[6]
        
        return ('nada' if a == b == c == d == e == f == 'limpio' else
                'limpiar' if situación == 'sucio' else
                'ir_Derecha' if robot == 'B' or robot== 'A' else
                'ir_Izquierda' if robot=='E' or robot== 'F' else
                'subir' if robot=='C' else
                'nada')
        
class DosCuartosCiegos(entornos_o.Entorno):
    """
    Clase para un entorno de dos cuartos. Muy sencilla solo regrupa métodos.

    El estado se define como (robot, A, B)
    donde robot puede tener los valores "A", "B"
    A y B pueden tener los valores "limpio", "sucio"

    Las acciones válidas en el entorno son ("ir_A", "ir_B", "limpiar", "nada").
    Todas las acciones son válidas en todos los estados.
    
    Los sensores solo muestran el lugar que se encuentra
    El sensor es (robot)
    con la ubicación del robot.

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

class AgenteRacionalCiego(entornos_o.Agente):
    """
    Un agente racional

    """
    def __init__(self):
        self.acc_Ant=[]
        self.acc=''
    def programa(self, percepción):
        robot = percepción
        
        if(len(self.acc_Ant)>=2):
            self.acc='nada'
        else:
            if(not(robot in self.acc_Ant)):
                self.acc_Ant.append(robot)
                self.acc='limpiar'
            else:
                if(robot=='A'):
                    self.acc='ir_B'
                else:
                    self.acc='ir_A'
            
        return (self.acc)

def test():
    """
    Prueba del entorno y los agentes

    """
    """print("Prueba del entorno con un agente aleatorio")
    entornos_o.simulador(SeisCuartos(),
                         AgenteAleatorio(['ir_Izquierda', 'ir_Derecha','subir','bajar', 'limpiar', 'nada']),
                         100)
    """
    """print("Prueba del entorno con un agente reactivo con modelo")
    entornos_o.simulador(SeisCuartos(), AgenteReactivoModeloSeisCuartos(), 100)

    """
    print("Prueba del entorno con un agente racional")
    entornos_o.simulador(DosCuartosCiegos(), AgenteRacionalCiego(), 100)
    
    """print("Prueba del entorno con un agente reactivo")
    entornos_o.simulador(DosCuartos(), AgenteReactivoDoscuartos(), 100)

    """

if __name__ == "__main__":
    test()
