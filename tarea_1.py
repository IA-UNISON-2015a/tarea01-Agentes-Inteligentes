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
__author__ = 'Brayan_Durazo'

import entornos_o
from random import choice
# Requiere el modulo entornos_o.py
# Usa el modulo doscuartos_o.py para reutilizar código
# Agrega los modulos que requieras de python

class NueveCuartos(entornos_o.Entorno):
    """
    Clase para un entorno de dos cuartos. Muy sencilla solo regrupa métodos.

    El estado se define como (robot, piso, A, B, C)
    donde robot puede tener los valores "A", "B", "C", piso los valores "1", "2", y "3"
    "A", "B", "C" pueden tener los valores "limpio", "sucio"
    La estructura de los cuartos:
    3er Piso: 7 8 9
    2do Piso: 4 5 6
    1er Piso: 1 2 3

    Las acciones válidas en el entorno son:
    ("ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada").
    Las acciones tienes las siguientes restricciones:
        No se puede usar la acción subir en el 3er piso
        No se puede usar la acción bajar en el 1er piso
        No se puede usar la acción ir_Izquierda en la habitacion A
        No se puede usar la acción ir_Derecha en la habitacion C
        
    Los sensores es una tupla (robot, limpio?)
    con la ubicación del robot(piso y habitación) y el estado de limpieza

    """
    def __init__(self, x0=[1, "sucio", "sucio", "sucio",
                              "sucio", "sucio", "sucio",
                              "sucio", "sucio", "sucio"]):
        """
        Por default inicialmente el robot está en A del primer piso y todos los cuartos
        están sucios
        """
        self.x = x0[:]
        self.desempeño = 0

    def acción_legal(self, acción):
        if (self.x[0] is 1 or self.x[0] is 4 or  self.x[0] is 7) and acción is "ir_Izquierda" : return False
        if (self.x[0] is 3 or self.x[0] is 6 or  self.x[0] is 9) and acción is "ir_Derecha" : return False
        if (self.x[0] is not 3 and self.x[0] is not 6) and acción is "subir": return False
        if (self.x[0] is not 4 and self.x[0] is not 7) and acción is "bajar": return False

        return acción in ("ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada")

    def transición(self, acción):
        if not self.acción_legal(acción):
            acción = "nada"

            #raise ValueError("La acción no es legal para este estado")
        robot, a, b, c, d, e, f, g, h, i = self.x[:]
        if acción is not "nada" or (a or b or c or e or f or g or h or i) is "sucio":
            self.desempeño -= 1
        if acción is "limpiar":
          self.desempeño -= 1
        if acción is ("ir_Derecha" or "ir_Izquierda"):
          self.desempeño -= 2
        if acción is ("subir" or "bajar"):
          self.desempeño -= 3
        if acción is "limpiar" and robot < 10:
            self.x[robot] = "limpio"
        if acción is "ir_Izquierda":
            self.x[0] -= 1
        if acción is "ir_Derecha":
            self.x[0] += 1
        if acción is "subir":
            self.x[0] += 3
        if acción is "bajar":
            self.x[0] -= 3
        
    def percepción(self):
        return (self.x[0], self.x[self.x[0]])


class AgenteAleatorio(entornos_o.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales
    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, percepcion):
        return choice(self.acciones)


class AgenteReactivoNuevecuartos(entornos_o.Agente):
    """
    Un agente reactivo simple
    """
    def programa(self, percepción):
        robot, situación = percepción
        if situación == 'sucio' :
            return 'limpiar'
        return ('limpiar' if situación == 'sucio' else'ir_A' if robot == 'B' else 'ir_B')


class AgenteReactivoModeloNueveCuartos(entornos_o.Agente):
    """
    Un agente reactivo basado en modelo
    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos
        """
        self.modelo = [1, "sucio", "sucio", "sucio", 
                            "sucio", "sucio", "sucio", 
                            "sucio", "sucio", "sucio"]

    def programa(self, percepción):
        robot, situación = percepción

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[robot] = situación

        #La estrategia general es limpiar todo un piso, y luego ir al siguiente piso
        if all(habitación is 'limpio' for habitación in self.modelo[1:]):
            return 'nada'
        if situación is 'sucio':
            return 'limpiar'
        #----------------------------------------------------------------------
        if robot is 1:
            return 'ir_Derecha'
        elif robot is 2:
            if self.modelo[1] is 'sucio':
                return 'ir_Izquierda'
            if self.modelo[3] is 'sucio':
                return 'ir_Derecha'
            else:
                return 'ir_Derecha'
        elif robot is 3:
            if self.modelo[1] is 'limpio' and self.modelo[3] is 'limpio':
                return 'subir'
        #----------------------------------------------------------------------
        if robot is 4:
            return 'ir_Derecha'
        elif robot is 5:
            if self.modelo[4] is 'sucio':
                return 'ir_Izquierda'
            if self.modelo[6] is 'sucio':
                return 'ir_Derecha'
            else:
                return 'ir_Derecha'
        elif robot is 6:
            if self.modelo[4] is 'limpio' and self.modelo[5] is 'limpio':
                return 'subir'
            else:
                return 'ir_Izquierda' 
        #----------------------------------------------------------------------
        if robot is 7:
            return 'ir_Derecha'
        elif robot is 8:
            if self.modelo[7] is 'sucio':
                return 'ir_Izquierda'
            if self.modelo[9] is 'sucio':
                return 'ir_Derecha'
            else:
                return 'ir_Derecha'
        elif robot is 9:
            if self.modelo[7] is 'limpio' and self.modelo[8] is 'limpio':
                return 'nada'
            else:
                return 'ir_Izquierda'
        return("nada")
        
def test():
    print("Prueba del entorno con un agente aleatorio")
    entornos_o.simulador(NueveCuartos(),
                         AgenteAleatorio(['ir_Izquierda', 'ir_Derecha',
                                          'limpiar','nada',
                                          'subir', 'bajar']), 200)
    print("Prueba del entorno con un agente reactivo con modelo")
    entornos_o.simulador(NueveCuartos(), AgenteReactivoModeloNueveCuartos(), 200)
    
if __name__ == "__main__":
    test()