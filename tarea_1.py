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

	CONCLUSIÓN.- subir y bajar generan mucho costo en el desempeño, al momento de
				ejecutarse aun asi el agente aleatorio genera menos costo ( pero sin limpiar 
				todos lo cuartos, oscilando en 2 los restantes ). 

2.- Diseña un Agente reactivo basado en modelo para este entorno y compara
    su desempeño con un agente aleatorio despues de 100 pasos de simulación.

    CONCLUSIÓN.- pasa lo mismo que en el entorno "SeisCuartos", siempre es
    			 constante el costo del desempeño de este agente mientras que el agente
    			 aleatorio suele limpiar todo en un costo igual.

3.- Al ejemplo original de los dos cuartos, modificalo de manera que el agente
    solo pueda saber en que cuarto se encuentra pero no sabe si está limpio
    o sucio.

    A este nuevo entorno llamalo DosCuartosCiego

    Diseña un agente racional para este problema, pruebalo y comparalo
    con el agente aleatorio.
	
	CONCLUSIÓN.- se obtuvo un resultado similar, para este agente se utilizo una pila 
				para poder saber como moverse. 

4.- Reconsidera el problema original de los dos cuartos, pero ahora modificalo
    para que cuando el agente decida aspirar, el 80% de las veces limpie pero
    el 20% (aleatorio) deje sucio el cuarto. Diseña un agente racional
    para este problema, pruebalo y comparalo con el agente aleatorio.

    A este entorno llamalo DosCuartosEstocástico
	
	CONCLUSIÓN.- uno pensaria que el entorno "DosCuartosEstocástico" fuera mas preciso, 
				 debido a que tiene mas probabilidad de limpiar que de no hacer nada pero si 
				 suele haber iteraciones( bastantes ) en las que si es sucede esto. 


Todos los incisos tienen un valor de 25 puntos sobre la calificación de
la tarea.

"""
__author__ = 'Carlos_Huguez'

import entorno_o

# Requiere el modulo entornos_o.py
# Usa el modulo doscuartos_o.py para reutilizar código
# Agrega los modulos que requieras de python
