#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Revisa el archivo README.md con las instrucciones de la tarea.

"""
__author__ = 'Julio Andrés Camargo Loaiza'

import entornos_f
import entornos_o
from random import choice


# Requiere el modulo entornos_f.py o entornos_o.py
# Usa el modulo doscuartos_f.py para reutilizar código
# Agrega los modulos que requieras de python


class TresCuartos(entornos_f.Entorno):
    """
    Clase para un entorno de tres cuartos.

    El estado se define como (robot, A, B, C)
    donde robot puede tener los valores "A", "B", "C"
    A, B y C pueden tener los valores "limpio", "sucio"

    Las acciones válidas en el entorno son
        ("ir_A", "ir_B", "ir_C", "limpiar", "nada").

    Todas las acciones son válidas en todos los estados.

    Los sensores es una tupla (robot, limpio?)
    con la ubicación del robot y el estado de limpieza

    """
    def accion_legal(self, _, accion):
        return accion in ("ir_A", "ir_B", "ir_C", "limpiar", "nada")

    def transicion(self, estado, acción):
        robot, a, b, c = estado

        c_local = 0 if a == b == c == "limpio" and acción == "nada" else 1

        return ((estado, c_local) if a == "nada" else
                (("A", a, b, c), c_local) if acción == "ir_A" else
                (("B", a, b, c), c_local) if acción == "ir_B" else
                (("C", a, b, c), c_local) if acción == "ir_C" else
                ((robot, "limpio", b, c), c_local) if robot == "A" else
                ((robot, a, "limpio", c), c_local) if robot == "B" else
                ((robot, a, b, "limpio"), c_local))

    def percepcion(self, estado):
        return estado[0], estado[" ABC".find(estado[0])]
