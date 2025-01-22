#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Revisa el archivo README.md con las instrucciones de la tarea.

"""
__author__ = 'georginasalcido'

import entornos_f
from doscuartos_f import AgenteAleatorio

# Requiere el modulo entornos_f.py o entornos_o.py
# Usa el modulo doscuartos_f.py para reutilizar código
# Agrega los modulos que requieras de python

class NueveCuartos(entornos_f.Entorno):

    def accion_legal(self, _, accion):
        return accion in ("ir_Izquierda", "ir_Derecha", "subir", "bajar", "limpiar", "nada")
    
    def transicion(self, estado, accion):
        robot, cuarto, piso = estado

        # El robot puede estar en uno de los 3 cuartos --> robot puede ser 1, 2 o 3
        # El robot puede estar en uno de los 3 pisos --> piso puede ser 1, 2 o 3
        # cuarto sería un arreglo/matriz con el estado de cada cuarto del piso --> cada cuarto puede ser "limpio" o "sucio"

        c_local = 0 if cuarto[piso][robot] == "limpio" and accion == "nada" else 1 
        # REVISAR SI FUNCIONA Y CAMBIAR COSTOS
        return ((estado, c_local) if accion == "nada" else
                ((robot - 1, cuarto, piso), c_local) if accion == "ir_Izquierda" and robot > 0 else
                ((robot + 1, cuarto, piso), c_local) if accion == "ir_Derecha" and robot < 2 else
                ((robot, cuarto, piso + 1), c_local) if robot == "subir" and robot == 2 and piso < 3 else
                ((robot, cuarto, piso - 1), c_local) if robot == "bajar" and robot == 0 and piso > 0 else
                ((robot, "limpio", piso), c_local) if robot == "limpiar" else # VER COMO ACCEDER AL CUARTO ESPECIFICO
                (estado, c_local) # VER COMO QUITAR PARA NO REPETIR
                )
    
    def percepcion(self, estado):
        return cuarto[piso][robot]



class AgenteReactivo(entornos_f.Agente):
    def programa(self, percepcion):
        robot, situacion = percepcion
        return ('limpiar' if situacion == 'sucio' else
                'ir_Izquierda' if robot < 0 else 
                'bajar' if robot == 0 else
                'ir_Derecha' if robot > 2 else
                'subir' #if robot == 2 
                )