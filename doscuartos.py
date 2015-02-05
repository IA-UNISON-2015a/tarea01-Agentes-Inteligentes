#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
doscuartos.py.py
------------

Ejemplo de un entorno muy simple y agentes idem

"""
from copy import deepcopy
__author__ = 'juliowaissman'

import entornos
from tarea_1 import TresCuartos
from random import choice
import collections

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

        return (('A', A, B) if accion == 'irA' else
                ('B', A, B) if accion == 'irB' else
                (robot, A, B) if accion == 'noOp' else
                ('A', 'limpio', B) if accion == 'limpiar' and robot == 'A' else
                ('B', A, 'limpio'))

    def sensores(self, estado):
        robot, A, B = estado
        #return robot, A if robot == 'A' else B
        
        #Para el problema tres:
        return robot

    def accion_legal(self, estado, accion):
        return accion in ('irA', 'irB', 'limpiar', 'noOp')

    def desempeno_local(self, estado, accion):
        robot, A, B = estado
        return 0 if accion == 'noOp' and A == B == 'limpio' else -1


class AgenteAMedias(entornos.Agente):
    """
    Un agente que no sabe el estado del cuarto
    """
    def __init__(self, acciones):
        self.acciones = acciones
        self.termine = [0,0]
        
    def programa(self, percepcion):
        posicion = percepcion
        if self.termine[0] == 0 :
            self.termine[0] = 1
            return 'limpiar'
        elif posicion == 'A' and self.termine[0] == 1:
            return 'irB'
        elif posicion == 'B' and self.termine[1] == 0:
            self.termine[1] = 1
            return 'limpiar'
        else:
            return 'noOp'
            
        
class AgenteAleatorioDosCuartos(entornos.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales
    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, percepcion):
        return choice(self.acciones)

class AgenteAleatorioTresCuartos(entornos.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales
    
    """
    def __init__(self, acciones):
        self.acciones = acciones
    
    def programa(self, percepcion):
        posicion, estado = percepcion
        if 'bajar' in self.acciones or 'subir' in self.acciones:
            self.acciones.pop()
        if 'down' in posicion and (int(posicion[-1]) == 1 or int(posicion[-1]) == 3):
            self.acciones.append('subir')
        elif 'up' in posicion and (int(posicion[-1]) -1 == 1 or int(posicion[-1]) -1 == 3):
            self.acciones.append('bajar')    
        return choice(self.acciones)


class AgenteReactivoDoscuartos(entornos.Agente):
    """
    Un agente reactivo simple

    """

    def programa(self, percepcion):
        robot, situacion = percepcion
        return ('limpiar' if situacion == 'sucio' else
                'irA' if robot == 'B' else
                'irB')


class AgenteReactivoModeloTresCuartos(entornos.Agente):
    """
    Otro agente reactivo basado en modelo 
    """
    def __init__(self):
        A = ['sucio','sucio','sucio']
        B = ['sucio','sucio','sucio']
        self.modelo = ['down_1', A, B]
        self.compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
        
    def programa(self, percepcion):
        
        posicion, situacion = percepcion
        
        #Actualiza el modelo interno
        self.modelo[0] = posicion
        lugar = 1
        if 'up' in posicion: lugar = 2
        self.modelo[lugar][int(posicion[-1]) -1] = situacion
        
        #Decide sobre el modelo interno
        A, B = deepcopy(self.modelo[1]), deepcopy(self.modelo[2])
        if self.compare(A,B) and 'limpio' in A[0]:
            return 'noOp'   
        elif (situacion == 'sucio' and 'down' in posicion) or ('up' in posicion and situacion == 'sucio'):
            return 'limpiar'
        elif situacion == 'limpio' and posicion != 'down_3' and 'up' not in posicion:
            return 'irDerecha'
        elif posicion == 'down_3':
            return 'subir'
        else:
            return 'irIzquierda'
        
       


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


def test():
    """
    Prueba del entorno y los agentes

    """
    """
    a = ['','',''] #Constuyo el piso de abajo
    b = ['','',''] #Consruyo el piso de arriba
    a[0] = a[1] = a[2] = b[0] = b[1] = b[2] = 'sucio' #Los ensucio
    
    print "Prueba del entorno tres cuartos con un agente reactivo basado en modelo"
    entornos.simulador(TresCuartos(),
                       AgenteReactivoModeloTresCuartos(),
                       ('down_1', a, b), 100)   
    print "Prueba del entorno tres cuartos con un agente aleatorio"
    entornos.simulador(TresCuartos(),
                       AgenteAleatorioTresCuartos(['irIzquierda', 'irDerecha', 'limpiar', 'noOp']),
                       ('down_1', a, b), 100)   
    """
    print "Prueba del entorno de dos cuartos con un agente aleatorio"
    entornos.simulador(DosCuartos(),
                      AgenteAleatorioDosCuartos(['irA', 'irB', 'limpiar', 'noOp']),
                      ('A', 'sucio', 'sucio'), 100)
    
    
    print "Prueba del entorno de dos cuartos con un agente que no ve como esta el rollo"
    entornos.simulador(DosCuartos(),
                       AgenteAMedias(['irA', 'irB', 'limpiar', 'noOp']),
                       ('A', 'sucio', 'sucio'), 100)
"""
    print "Prueba del entorno de dos cuartos con un agente reactivo"
    entornos.simulador(DosCuartos(),
                       AgenteReactivoModeloDosCuartos(),
                       ('A', 'sucio', 'sucio'), 100)

    """
if __name__ == '__main__':
    test()
