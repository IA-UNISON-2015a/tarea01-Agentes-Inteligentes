#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Tarea de desarrollo de entornos y agentes
==========================================

En esta tarea realiza las siguiente acciones:

1.- Desarrolla un entorno similar al de los dos cuartos, 
    pero con tres cuartos en el primer piso, 
    y tres cuartos en el segundo piso. 
    
    Las acciones totales serán

    A = {"irDerecha", "irIzquierda", "subir", "bajar", "limpiar" y "noOp"}

    La acción de "subir" solo es legal en el piso de abajo (cualquier cuarto), 
    y la acción de "bajar" solo es legal en el piso de arriba.

    Las acciones de subir y bajar son mas costosas en término de energía 
    que ir a la derecha y a la izquierda, por lo que la función de desempeño 
    debe de ser de tener limpios todos los cuartos, con el menor numero de 
    acciones posibles, y minimozando subir y bajar en relación a ir a los lados.

2.- Diseña un Agente reactivo basado en modelo para este entorno y compara 
    su desempeño con un agente aleatorio despues de 100 pasos de simulación.

3.- Al ejemplo original de los dos cuardos, modificalo de manera que el agente 
    sabe en que cuarto se encuentra pero no sabe si está limpio o sucio. 
    Diseña un agente racional para este problema, pruebalo y comparalo 
    con el agente aleatorio.

4.- Reconsidera el problema original de los dos cuartos, pero ahora modificalo 
    para que cuando el agente decida aspirar, el 80% de las veces limpie pero 
    el 20% (aleatorio) deje sucio el cuarto. Diseña un agente racional
    para este problema, pruebalo y comparalo con el agente aleatorio. 

Todos los incisos tienen un valor de 25 puntos sobre la calificación de la tarea.


"""
__author__ = 'Gerardo'

import entornos
# Requiere el modulo entornos.py
# El modulo doscuartos.py puede ser de utilidad para reutilizar código
# Agrega los modulos que requieras de python

class TresCuartos(entornos.Entorno):
    
    def transicion(self, estado, accion):
        if not self.accion_legal(estado, accion):
            raise ValueError("La accion " + accion + " no es legal para el estado " + estado[0])
        
        posicion, A, B = estado
        if accion == 'irDerecha':
            return (('down_2', A, B) if posicion == 'down_1' else
                    ('down_3', A, B) if posicion == 'down_2' or posicion == 'down_3' else
                    ('up_2', A, B) if posicion == 'up_1' else
                    ('up_3', A, B))
        elif accion == 'irIzquierda':
            return (('down_1', A, B) if posicion == 'down_1' or posicion == 'down_2' else
                    ('down_2', A, B) if posicion == 'down_3' else
                    ('up_1', A, B) if posicion == 'up_1' or posicion == 'up_2' else
                    ('up_2', A, B))
        elif accion == 'subir':
            return (('up_1', A, B) if posicion == 'down_1' else
                    ('up_2', A, B) if posicion == 'down_2' else
                    ('up_3', A, B))
        elif accion == 'bajar':
            return (('down_1', A, B) if posicion == 'up_1' else
                    ('down_2', A, B) if posicion == 'up_2' else
                    ('down_3', A, B))
        elif accion == 'limpiar':
            if posicion == 'down_1':
                A[0] = 'limpio'
            elif posicion == 'down_2': 
                A[1] ='limpio'
            elif posicion == 'down_3': 
                A[2] ='limpio'
            elif posicion == 'up_1':
                B[0] = 'limpio'
            elif posicion == 'up_2': 
                B[1] = 'limpio'
            else: 
                B[2] = 'limpio'
        
        return (posicion, A, B)

        
    def sensores(self, estado):
        posicion, A, B = estado
        if 'down' in posicion:
            return posicion, A[int(posicion[-1]) -1]
        else:
            return posicion, B[int(posicion[-1]) -1]
                
    
    def accion_legal(self, estado, accion):
        posicion, A, B = estado
        pisoAbajo = ['down_1', 'down_2', 'down_3']
        listaAcciones = ["irDerecha", "irIzquierda", "subir", "bajar", "limpiar", "noOp"]
        if (posicion in pisoAbajo) and accion == 'subir' and accion in listaAcciones:
            return True
        elif posicion not in pisoAbajo and accion == 'bajar' and accion in listaAcciones:
            return True
        elif accion == 'irDerecha' or accion == 'irIzquierda' or accion == 'noOp' or accion == 'limpiar':
            return True
        else:
            
            return False
        
        
    def desempeno_local(self, estado, accion):
        posicion, A, B = estado
        if accion == 'noOp' and all( i == 'limpio' for i in A) and all(i == 'limpio' for i in B):
            return 0
        elif accion == 'subir' or accion == 'bajar':
            return -2
        else:
            return -1
        