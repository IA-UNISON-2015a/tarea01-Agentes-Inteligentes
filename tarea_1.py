#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Revisa el archivo README.md con las instrucciones de la tarea.

"""
"""trabajado entre david y sofia"""

import entornos_f
from random import choice
import copy

# Requiere el modulo entornos_f.py o entornos_o.py
# Usa el modulo doscuartos_f.py para reutilizar código
# Agrega los modulos que requieras de python

"""
estado representa una tupla (robot, edificio), donde:
robot: ubicación (piso, cuarto).
edificio: Diccionario que almacena el estado de limpieza de cada cuarto.
Se usa un diccionario en vez de una lista de listas para tener un acceso
facil a cada cuarto del edificio.

accion_legal: se definen las acciones legales que puede hacer un agente

edificioLimpio: Recorre todo el cuarto del edificio para verificar si esta completamente limpio.

transicion: Se calcula el costo local teniendo la accion de no hacer nada como un costo nulo, limpiar es el menor costo
y moverse de derecha a izquierda tiene un costo de 2 y por ultimo subir y bajar tiene un costo de 3.

Ejecución de acciones:
La acción nada regresa el mismo estado y el costo.

La accion limpiar actualiza el cuarto donde esta el robot a "limpio":

Transicion recibe el estado, se crea una copia del edificio para mantener correctamente el historial de estados
despues actualiza el estado del cuarto a limpio y regresa el nuevo estado y el costo.
Las demas acciones lo que hacen es mover el robot a traves de los cuartos, si no es la accion limpiar se queda con el mismo diccionario.

Percepcion: devuelve el estado de limpieza del cuarto en el que esta el robot.
Entra un estado y esta se desglosa en robot y edificio, despues el robot se desglosa en su posicion
para regresar el estado (limpio o sucio) en el que se encuentra el cuarto en dicha posición (donde esta el robot).

"""


class NueveCuartos(entornos_f.Entorno):

    def accion_legal(self, _, accion):
        return accion in ("ir_derecha","ir_izquierda", "subir", "bajar", "limpiar", "nada")
    
    def edificioLimpio(self, edificio):
        for piso in edificio:
            for cuarto in piso:
                if cuarto != "limpio":
                    return False
        return True

    def transicion(self, estado, accion):
        
        robot, edificio = estado
        piso, cuarto = robot

        if self.edificioLimpio(edificio) and accion == "nada":
            c_local = 0
        elif accion == "limpiar":
            c_local = 1
        elif accion == "ir_derecha" or accion == "ir_izquierda":
            c_local = 2
        else:
            c_local = 3

        if accion == "nada":
            return (estado, c_local)
        elif accion == "limpiar":
            piso, cuarto = robot
            nuevo_edificio = copy.deepcopy(edificio)
            nuevo_edificio[(piso, cuarto)] = "limpio"
            return ((robot, nuevo_edificio), c_local)
        elif accion == "ir_derecha":
             if cuarto < 2:
                cuarto = cuarto + 1
                robot = piso, cuarto
                #nuevoCuarto = cuarto + 1
                #nuevoRobot = piso, nuevoCuarto
                #nuevoEstado = nuevoRobot, edificio
                return ((robot, edificio), c_local)   
             else:
                  print("No es legal moverse a la derecha")
                  return estado, c_local
        elif accion == "ir_izquierda":
             if cuarto > 0:
                  cuarto = cuarto - 1
                  robot = piso, cuarto
                  return ((robot,edificio), c_local)
             else:
                  print("No es legal moverse a la izquierda")
                  return estado, c_local
        elif accion == "subir":
             if piso > 0 and cuarto == 2:
                  piso = piso -1
                  robot = piso, cuarto 
                  return ((robot,edificio), c_local)
             else:
                  print("No es legal subir de piso")
                  return estado, c_local
        elif accion == "bajar":
             if piso < 2 and cuarto == 0:
                  piso = piso + 1
                  robot = piso, cuarto
                  return ((robot,edificio), c_local)
             else:
                  print("No es legal bajar de piso")
                  return estado, c_local

        # Si la acción no es válida, devolver el estado sin cambios
        return estado, c_local

    
    def percepcion(self, estado):
        if not isinstance(estado, tuple):
             raise TypeError("El estado debe ser una tupla")
        robot, edificio = estado
        piso, cuarto = robot
        return robot, edificio[(piso, cuarto)]

class AgenteAleatorio(entornos_f.Agente):
    
    def __init__(self, acciones):
            self.acciones = acciones
        
    def programa(self, _):
            return choice(self.acciones)

class AgenteReactivoNueveCuartos(entornos_f.Agente):
     
     def programa(self, percepcion):
          
          robot, situacion = percepcion
          piso, cuarto = robot

          if situacion == "sucio":
               return "limpiar"
          if piso == 0:
               if cuarto < 2 and situacion == "limpio":
                    return "ir_derecha"
               elif cuarto != 0 and situacion == "limpio":
                    return "ir_izquierda"
          if piso == 1:
               if cuarto < 2 and situacion != "limpio":
                    return "ir_derecha"
          if piso == 2:
               if cuarto < 2 and situacion != "limpio":
                    return "ir_derecha"
          else:
               return "nada"

def prueba_agente(agente):
     estado_inicial = ((0, 0), {
        (0, 0): "sucio", (0, 1): "sucio", (0, 2): "sucio",
        (1, 0): "sucio", (1, 1): "sucio", (1, 2): "sucio",
        (2, 0): "sucio", (2, 1): "sucio", (2, 2): "sucio"
    })
     pasos = 100
     entorno = NueveCuartos()
     resultados = entornos_f.simulador(entorno, agente, estado_inicial, pasos)

     entornos_f.imprime_simulacion(resultados, estado_inicial, formato="mejorado")

def test():
     
     print("Prueba del entorno con un agente aleatorio")
     prueba_agente(AgenteAleatorio(["ir_derecha", "ir_izquierda", "subir", "bajar", "limpiar", "nada"]))
     print("Prueba del entorno con un agente")
     prueba_agente(AgenteReactivoNueveCuartos())


if __name__ == "__main__":
     test()