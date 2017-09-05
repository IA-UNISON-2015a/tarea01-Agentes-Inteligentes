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
    acciones posibles, y minimizando subir y bajar en relación a ir a los
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
__author__ = 'Belen_Chavarría'

import entornos_o
from random import choice
import numpy.random as np

# Requiere el modulo entornos_o.py
# Usa el modulo doscuartos_o.py para reutilizar código
# Agrega los modulos que requieras de python


class SeisCuartos(entornos_o.Entorno):
    """
    Clase para un entorno de seis cuartos.

    El estado se define como (robot, A1, A2, A3, B1, B2, B3)
    donde robot puede tener los valores "A1","A2","A3", "B1", "B2", "B3"
    (los Ai representan los cuartos del piso de abajo y los Bi los de arriba, Bi está sobre Ai).
    Ai y Bi pueden tener los valores "limpio", "sucio"

    Las acciones válidas en el entorno son ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"].
    Todas las acciones son válidas en todos los estados.

    Los sensores es una tupla (robot, limpio?)
    con la ubicación del robot y el estado de limpieza

    """
    def __init__(self, x0=[["S","S","S"],["S","S","S"], [0,0]]):
        """
        Por default inicialmente el robot está en el primer cuarto de abajo (0,0) los seis cuartos
        están sucios
        """
        self.x = [x0[0][:], x0[1][:], x0[2][:]]
        self.desempeño = 0

    def acción_legal(self, acción):
        if self.x[2][0] is 0:
            return acción in ('ir_D', 'ir_I', 'subir', 'limpiar', 'nada')
        else:
            return acción in ('ir_D', 'ir_I', 'bajar', 'limpiar', 'nada')

    def transición(self, acción):
        try: 
            if not self.acción_legal(acción):
                raise ValueError("La acción '{}' no es legal para este estado".format(acción))
        except ValueError as v:
            print(v)
            return
            
        if acción is 'limpiar':
            self.x[self.x[2][0]][self.x[2][1]] = 'L'
            self.desempeño-=1
        elif acción is 'ir_D':
            if self.x[2][1] < 2:
                self.x[2][1]+= 1 
            self.desempeño-=1
        elif acción is 'ir_I':
            if self.x[2][1] > 0:
                self.x[2][1] -=1  
            self.desempeño-=1
        elif acción is 'subir':
            self.x[2][0]=1 
            self.desempeño-=2
        elif acción is 'bajar':
            self.x[2][0]=0
            self.desempeño-=2
        elif self.x[0][0] is 'S' or self.x[0][1] is 'S' or self.x[0][2] is 'S' or self.x[1][0] is 'S' or self.x[1][1] is 'S' or self.x[1][2] is 'S':
            self.desempeño-=1


    def percepción(self):
        return self.x[2], self.x[self.x[2][0]][self.x[2][1]]


###########################################

class AgenteAleatorio(entornos_o.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales

    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, percepcion):
        return choice(self.acciones)
        
###########################################

class AgenteReactivoModeloSeisCuartos(entornos_o.Agente):
    """
    Un agente reactivo basado en modelo

    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = [['S', 'S','S'],['S','S','S'],[0,0]]

    def programa(self, percepción):
        robot, situación = percepción

        # Actualiza el modelo interno
        self.modelo[2] = robot[:]
        self.modelo[robot[0]][robot[1]] = situación


        a1,a2,a3,b1,b2,b3 = self.modelo[0][0],self.modelo[0][1],self.modelo[0][2],self.modelo[1][0], self.modelo[1][1],self.modelo[1][2]
        #Decide sobre el modelo interno
        if situación == 'S':
            return 'limpiar'
        elif a1==a2==a3==b1==b2==b3=='L':
            return 'nada'
        elif self.modelo[2][0]==0 and self.modelo[2][1]==2:
            return 'subir'
        elif self.modelo[2][0]==1 and self.modelo[2][1]==0:
            return 'bajar'
        elif self.modelo[2][0]==0:
            return 'ir_D'
        else:
            return 'ir_I'
        
            
###########################################
class DosCuartosCiego(entornos_o.Entorno):
    """
    Clase para un entorno de dos cuartos.

    El estado se define como (robot, A, B)
    donde robot puede tener los valores "A", "B"
    A y B pueden tener los valores "limpio", "sucio"

    Las acciones válidas en el entorno son ("ir_A", "ir_B", "limpiar", "nada").
    Todas las acciones son válidas en todos los estados.

    el sensor 'robot' indica la ubicación del mismo

    """
    def __init__(self, x0=["A", "limpio", "sucio"]):
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

########################################### 
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
        self.flag= False
        # Actualiza el modelo interno
        self.modelo[0] = percepción

        # Decide sobre el modelo interno
        a, b = self.modelo[1], self.modelo[2]

        if self.modelo[" AB".find(self.modelo[0])] is 'sucio':
           self.flag=True
           self.modelo[" AB".find(self.modelo[0])] = 'limpio'

        return ('nada' if a == b == 'limpio' else
                'limpiar' if self.flag else
                'ir_A' if percepción == 'B' else 'ir_B')

   
###########################################
class DosCuartosEstocastico(entornos_o.Entorno):
    """
    Clase para un entorno de dos cuartos.

    El estado se define como (robot, A, B)
    donde robot puede tener los valores "A", "B"
    A y B pueden tener los valores "limpio", "sucio"

    Las acciones válidas en el entorno son ("ir_A", "ir_B", "limpiar", "nada").
    Todas las acciones son válidas en todos los estados.

    Los sensores es una tupla (robot, limpio?)
    con la ubicación del robot y el estado de limpieza
    
    La particularidad de este entorno es que se tiene un 80% de probabilidad 
    de que el cuarto se limpie una vez tomada la decisión de limpiar.

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
        return self.x[0], self.x[" AB".find(self.x[0])]

########################################### 
class ARM_DosCuartosEstocastico(entornos_o.Agente):
    """
    Un agente reactivo basado en modelo

    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = ['A', 'sucio', 'sucio']
        
    def programa(self, percepción):
        robot, situación = percepción

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[' AB'.find(robot)] = situación

        # Decide sobre el modelo interno
        a, b = self.modelo[1], self.modelo[2]


        if situación=='sucio':
            return('limpiar' if np.random_integers(1, 100) <= 80 else 'nada')
        else:
            return('nada' if a == b == 'limpio' else
                'ir_A' if robot == 'B' else 'ir_B')
            

###########################################    
def test():
    """
    Prueba del entorno y los agentes

    """
    print("ENTORNO: SEIS CUARTOS \n Prueba del entorno con un agente aleatorio")
    entornos_o.simulador(SeisCuartos(),
                        AgenteAleatorio(['ir_D', 'ir_I', 'subir', 'bajar', 'limpiar', 'nada']),
                        100)


    print("ENTORNO: SEIS CUARTOS \n Prueba del entorno con un agente reactivo con modelo")
    entornos_o.simulador(SeisCuartos(), AgenteReactivoModeloSeisCuartos(), 100)
    
    ##############
    
    print("ENTORNO: DOS CUARTOS CIEGO \n Prueba del entorno con un agente aleatorio")
    entornos_o.simulador(DosCuartosCiego(),
                        AgenteAleatorio(['ir_A', 'ir_B', 'limpiar', 'nada']),
                        100)


    print("ENTORNO: DOS CUARTOS CIEGO \n Prueba del entorno con un agente reactivo con modelo")
    entornos_o.simulador(DosCuartosCiego(), AgenteReactivoModeloDosCuartosCiego(), 100)
    
    ###############
    
    print("ENTORNO: DOS CUARTOS ESTOCÁSTICO \n Prueba del entorno con un agente aleatorio")
    entornos_o.simulador(DosCuartosEstocastico(),
                        AgenteAleatorio(['ir_A', 'ir_B', 'limpiar', 'nada']),
                        100)


    print("ENTORNO: DOS CUARTOS ESTOCÁSTICO \n Prueba del entorno con un agente reactivo con modelo")
    entornos_o.simulador(DosCuartosEstocastico(), ARM_DosCuartosEstocastico(), 100)
    

###########################################
if __name__ == "__main__":
    test()