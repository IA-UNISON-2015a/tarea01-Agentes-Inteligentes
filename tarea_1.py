#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Revisa el archivo README.md con las instrucciones de la tarea.

"""
__author__ = 'Julio Andrés Camargo Loaiza'

import entornos_f_tarea
from random import choice


# Requiere el modulo entornos_f.py o entornos_o.py
# Usa el modulo doscuartos_f.py para reutilizar código
# Agrega los modulos que requieras de python


class TresCuartos(entornos_f_tarea.Entorno):
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
    def accion_legal(self, estado, accion):
        robot = estado[0]  # Posición actual del robot
        if accion == "izq" and robot == "A":
            return False
        if accion == "der" and robot == "C":
            return False
        return accion in ("izq", "der", "limpiar", "nada")

    def transicion(self, estado, accion):
        # Descompone el estado actual
        robot, a, b, c = estado

        # Determina costo local
        c_local = 0 if a == b == c == "limpio" and accion == "nada" else 1

        # Transiciones posibles según su acción y estado actual
        if robot == "A":
            return ((estado, c_local) if accion == "nada" else
                    (("B", a, b, c), c_local) if accion == "der" else
                    ((robot, "limpio", b, c), c_local))
        if robot == "B":
            return ((estado, c_local) if accion == "nada" else
                    (("A", a, b, c), c_local) if accion == "izq" else
                    (("C", a, b, c), c_local) if accion == "der" else
                    ((robot, a, "limpio", c), c_local))
        if robot == "C":
            return ((estado, c_local) if accion == "nada" else
                    (("B", a, b, c), c_local) if accion == "izq" else
                    ((robot, a, b, "limpio"), c_local))

    def percepcion(self, estado):
        return estado[0], estado[" ABC".find(estado[0])]
