#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Revisa el archivo README.md con las instrucciones de la tarea.

"""
__author__ = 'georginasalcido'

import entornos_f
import doscuartos_f
# import entornos_o

# Requiere el modulo entornos_f.py o entornos_o.py
# Usa el modulo doscuartos_f.py para reutilizar código
# Agrega los modulos que requieras de python

class NueveCuartos(entornos_f.Entorno):

    def accion_legal(self, _, accion):
        return accion in ("ir_Izquierda", "ir_Derecha", "subir", "bajar", "limpiar", "nada")
    
    def transicion(self, estado, accion):
        # robot, izq, centro, der, piso = estado
        robot, cuarto, piso = estado #VER COMO FUNCIONARÍA CUARTO

        # El robot puede estar en uno de los 3 cuartos --> robot puede ser 1, 2 o 3
        # El robot puede estar en uno de los 3 pisos --> robot puede ser 1, 2 o 3
        # cuarto sería un arreglo/matriz con el estado del cuarto --> cuarto puede ser "limpio" o "sucio"

        # c_local = 0 if izq == der == centro == "limpio" and accion == "nada" else 1
        c_local = 0 if cuarto[piso] == "limpio" and accion == "nada" else 1 #VER SI FUNCIONA

        return ((estado, c_local) if accion == "nada" else
                ((robot - 1, izq, der), c_local) if acción == "ir_Izquierda" else
                #(("Derecha", izq, der), c_local) if acción == "ir_Derecha" else
                #((robot, "limpio", der), c_local) if robot == "Izquierda" else
                #((robot, izq, "limpio"), c_local) if robot == "Derecha" else
                #((robot, "bajar", der), c_local) if robot == 
                )