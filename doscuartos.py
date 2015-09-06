#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
doscuartos.py.py
------------

Ejemplo de un entorno muy simple y agentes idem

"""

__author__ = 'Luis Fernando Suarez Astiazaran'

import entornos
from random import choice
import random

class DosCuartos(entornos.Entorno):
    """
    Clase para un entorno de dos cuartos. Muy sencilla solo regrupa métodos.

    El estado se define como 
                (robot, A, B) 
    donde robot puede tener los valores "A", "B"
    A y B pueden tener los valores "limpio", "sucio"

    Las acciones válidas en el entorno son 
            "irA", "irB", "limpiar" y "noOp". 
    Todas las acciones son válidas en todos los estados.

    Los sensores es una tupla 
                (robot, limpio?) 
    con la ubicación del robot y el estado de limieza

    """

    def transicion(self, estado, accion):
        if not self.accion_legal(estado, accion):
            raise ValueError("La accion no es legal para este estado")

        robot, A, B = estado

        '''
        return (('A', A, B) if accion == 'irA' else
                ('B', A, B) if accion == 'irB' else
                (robot, A, B) if accion == 'noOp' else
                ('A', 'limpio', B) if accion == 'limpiar' and robot == 'A' else
                ('B', A, 'limpio'))
        '''

        # __________#Inciso (4) de la tarea!!!!__________
        
        if accion == 'limpiar' and robot == 'A':
            if random.randint(1, 100)<80: # El 80% de las veces
                return (robot, A, B) # Regresa el nuevo estado
            else:  # El 20% restante no hace nada
                return ('A', 'noOp', B) # Regresa el nuevo estado
        if accion == 'noOp' and robot == 'B':
            if random.randint(1, 100)<80:
                return (robot, A, B) # Regresa el nuevo estado
            else:
                return ('B', A, 'noOp') # Regresa el nuevo estado  
        
        return (robot,A,B)
        
        #_______________________________________________
    
    def sensores(self, estado):
        robot, A, B = estado
        return robot, A if robot == 'A' else B

    def accion_legal(self, estado, accion):
        return accion in ('irA', 'irB', 'limpiar', 'noOp')

    def desempeno_local(self, estado, accion):
        robot, A, B = estado
        return 0 if accion == 'noOp' and A == B == 'limpio' else -1

"""
______________________________________________________________________________
"""
class AgenteAleatorio(entornos.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales

    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, percepcion):
        return choice(self.acciones)

"""
______________________________________________________________________________
"""
class AgenteReactivoDoscuartos(entornos.Agente):
    """
    Un agente reactivo simple

    """

    def programa(self, percepcion):
        robot, situacion = percepcion
        return ('limpiar' if situacion == 'sucio' else
                'irA' if robot == 'B' else
                'irB')

"""
______________________________________________________________________________
"""
class AgenteReactivoModeloDosCuartos(entornos.Agente):
    """
    Un agente reactivo basado en modelo

    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = ['A', 'sucio', 'sucio']
        self.lugar = {'A': 1, 'B': 2}

    def programa(self, percepcion):
        robot, situacion = percepcion

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[self.lugar[robot]] = situacion

        # Decide sobre el modelo interno
        A, B = self.modelo[1], self.modelo[2]
        return ('noOp' if A == B == 'limpio' else
                'limpiar' if situacion == 'sucio' else
                'irA' if robot == 'B' else
                'irB')

"""
______________________________________________________________________________
"""
class TresCuartos(entornos.Entorno):


        # son tres cuartos arriva y tres cuartos abajo #
    def transicion(self, estado, accion):
        if not self.accion_legal(estado, accion):
            raise ValueError("La accion no es legal para este estado")

        lista=list(estado)

        if accion == 'irDerecha':
            if lista[-1] == 3*3-1:
                lista[-1]=0
            else: 
                lista[-1]+=1
            return lista
        elif accion == 'irIzquierda':
            if lista[-1]==0:
                lista[-1]=3*3-1
            else: 
                lista[-1]-=1
            return lista
        elif accion == 'irArriba':
            lista[-1]-=3
            if lista[-1]<0:
                lista[-1]+=3*3-1
            return lista
        elif accion == 'irAbajo':
            lista[-1]+=3
            if lista[-1]>3*3-1:
                lista[-1]-=3*3-1
            return lista
        elif accion == 'limpiar':
            lista[lista[-1]]= 'limpio'
            return lista

        else:
            return lista
 
    def sensores(self, estado):
        
        return estado[-1],estado[estado[-1]]

    def accion_legal(self, estado, accion):
        return accion in ('irDerecha', 'irIzquierda', 'irArriba', 'irAbajo', 'limpiar' , 'noOp')

    def desempeno_local(self, estado, accion):
        return 0 if accion == 'noOp' and self.isClean(estado) else -1

    def isClean(self,estado):
        for s in range(0,3*3):
            if estado[s]=='sucio':
                return False
        return True
        
        
"""
______________________________________________________________________________
"""

def test():
    """
    Prueba del entorno y los agentes

    """
    print "Prueba del entorno de dos cuartos con un agente aleatorio"
    entornos.simulador(DosCuartos(),
                       AgenteAleatorio(['irA', 'irB', 'limpiar', 'noOp']),
                       ('A', 'sucio', 'sucio'), 100)

    print "Prueba del entorno de dos cuartos con un agente reactivo"
    entornos.simulador(DosCuartos(),
                       AgenteReactivoDoscuartos(),
                       ('A', 'sucio', 'sucio'), 100)

    print "Prueba del entorno de dos cuartos con un agente reactivo"
    entornos.simulador(DosCuartos(),
                       AgenteReactivoModeloDosCuartos(),
                       ('A', 'sucio', 'sucio'), 100)


    print "Prueba del entorno Tres cuartos"
    lista=[]
    for i in range(0,3*3):
        lista.append('sucio')
    lista.append(0)
    
    entornos.simulador(TresCuartos(),
                        AgenteAleatorio(['irDerecha', 'irIzquierda', 'irArriba', 'irAbajo', 'limpiar' , 'noOp']),
                        lista, 100)

if __name__ == '__main__':
    test()
