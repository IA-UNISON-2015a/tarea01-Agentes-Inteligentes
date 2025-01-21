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
        # robot, izq, centro, der, piso = estado # LIMPIAR DESPUES
        robot, cuarto, piso = estado

        # El robot puede estar en uno de los 3 cuartos --> robot puede ser 1, 2 o 3
        # El robot puede estar en uno de los 3 pisos --> piso puede ser 1, 2 o 3
        # cuarto sería un arreglo/matriz con el estado de cada cuarto del piso --> cada cuarto puede ser "limpio" o "sucio"

        # c_local = 0 if izq == der == centro == "limpio" and accion == "nada" else 1 # LIMPIAR DESPUES
        c_local = 0 if cuarto[piso][robot] == "limpio" and accion == "nada" else 1 #VER SI FUNCIONA

        # REVISAR SI FUNCIONA
        return ((estado, c_local) if accion == "nada" else
                ((robot - 1, cuarto, piso), c_local) if acción == "ir_Izquierda" and robot > 0 else
                ((robot + 1, cuarto, piso), c_local) if acción == "ir_Derecha" and robot < 2 else
                ((robot, cuarto, piso + 1), c_local) if robot == "subir" and robot == 2 and piso < 3 else
                ((robot, cuarto, piso - 1), c_local) if robot == "bajar" and robot == 0 and piso > 0 else
                ((robot, "limpio", piso), c_local) if robot == "limpiar" # VER COMO ACCEDER AL CUARTO ESPECIFICO
                )