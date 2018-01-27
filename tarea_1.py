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
   
   El entorno se llamara `SeisCuartos`.

   Las acciones totales seran
   
   ```
   ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]
   ``` 
    
   La accion de `"subir"` solo es legal en el piso de abajo, en los cuartos de los extremos, 
   mientras que la accion de `"bajar"` solo es legal en el piso de arriba y en el cuarto de el centro (dos
   escaleras para subir, una escalera para bajar).

   Las acciones de subir y bajar son mas costosas en termino de
   energia que ir a la derecha y a la izquierda, por lo que la funcion
   de desempenio debe de ser de tener limpios todos los cuartos, con el
   menor numero de acciones posibles, y minimizando subir y bajar en
   relacion a ir a los lados. El costo de limpiar es menor a los costos
   de cualquier accion.

2. Disenia un Agente reactivo basado en modelo para este entorno y
   compara su desempenio con un agente aleatorio despues de 100 pasos
   de simulacion.

3. Al ejemplo original de los dos cuartos, modificalo de manera que el
   agente solo pueda saber en que cuarto se encuentra pero no sabe si
   esta limpio o sucio.

   A este nuevo entorno llamalo `DosCuartosCiego`.

   Disenia un agente racional para este problema, pruebalo y comparalo
   con el agente aleatorio.

4. Reconsidera el problema original de los dos cuartos, pero ahora
   modificalo para que cuando el agente decida aspirar, el 80% de las
   veces limpie pero el 20% (aleatorio) deje sucio el cuarto. Igualmente, 
   cuando el agente decida cambiar de cuarto, se cambie correctamente de cuarto el 90% de la veces
   y el 10% se queda en su lugar. Disenia
   un agente racional para este problema, pruebalo y comparalo con el
   agente aleatorio.

   A este entorno llamalo `DosCuartosEstocastico`.

Todos los incisos tienen un valor de 25 puntos sobre la calificacion de
la tarea.

"""
__author__ = 'escribe_tu_nombre'

import entorno_o

# Requiere el modulo entornos_o.py
# Usa el modulo doscuartos_o.py para reutilizar codigo
# Agrega los modulos que requieras de python

def SeisCuartos(doscuartos_o.DosCuartos):
    """
    Clase para un entorno de seis cuartos. 

    Hay 3 cuartos arriba y 3 cuartos abajo, enumerados como sigue:
    1 2 3
`   4 5 6

    El estado se define como (robot, 1, 2, 3, 4, 5, 6)
    donde robot puede tener los valores "1", "2", ..., "6"
    1, 2, ..., 6 pueden tener los valores "limpio", "sucio"

    Las acciones validas en el entorno son ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]
    Para ir al primer piso es necesario subir desde el cuarto 4 o 6 y para bajar es necesario hacerlo desde el
    cuarto 2.
    Si por ejemplo el agente se encuentra en 2, solo puede elegir ["ir_Derecha", "ir_Izquierda", "bajar", "limpiar", "nada"]

    Los sensores es una tupla (robot, limpio?)
    con la ubicacion del robot y el estado de limpieza

    """
    def __init__(self, x0=[1, "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]):
        """
        Por default inicialmente el robot esta en 1 y los seis cuartos
        estan sucios

        """
        self.x = x0[:]
        self.desempenio = 0

    def accion_legal(self, accion):
        if self.x[0] == 1:
            return accion in ["ir_Derecha", "limpiar", "nada"]
        if self.x[0] == 2:
            return accion in ["ir_Derecha", "ir_Izquierda", "bajar", "limpiar", "nada"]
        if self.x[0] == 3:
            return accion in ["ir_Izquierda", "limpiar", "nada"]
        if self.x[0] == 4:
            return accion in ["ir_Derecha", "subir", "limpiar", "nada"]
        if self.x[0] == 5:
            return accion in ["ir_Derecha", "ir_Izquierda", "limpiar", "nada"]
        if self.x[0] == 6:
            return accion in ["ir_Izquierda", "subir", "limpiar", "nada"]

    def costo(self, accion):
        costoMin = 0.5
        costoIzqDer = 2 * costoMin
        costoSubirBajar = 2 * costoIzqDer
        if accion is "limpiar" or \
           (accion is "nada" and any(cuarto is "sucio" for cuarto in self.x[1:]):
           self.desempenio -= costoMin
        if accion is "ir_Derecha" or accion is "ir_Izquierda":
            self.desempenio -= costoIzqDer
        if accion is "subir" or accion is "bajar":
            self.desempenio -= costoSubirBajar

    def transicion(self, accion):
        if not self.accion_legal(accion):
            raise ValueError("La accion no es legal para este estado")

        self.costo(accion)
        if accion is "limpiar":
            self.x[ self.x[0] ] = "limpio"
        #Debido a nombre y acomodo de los cuartos se puede aplicar la siguiente aritmetica.
        #Si aumenta el numero de cuartos o se cambia el acomodo, deja de funcionar
        elif accion is "ir_Derecha":
            self.x[0] += 1
        elif accion is "ir_Izquierda":
            self.x[0] -= 1
        elif accion is "subir":
            self.x[0] -= 3
        elif accion is "bajar":
            self.x[0] += 3

    def percepcion(self):
        return self.x[0], self.x[ self.x[0] ]
