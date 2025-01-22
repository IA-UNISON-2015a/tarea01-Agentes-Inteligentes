#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
"""
__author__ = 'Jesus Flores Lacarra'

import entornos_o
from random import choice

class NueveCuartos(entornos_o.Entorno):
    """
    Clase para un entorno de nueve cuartos.

    El estado se define como (robot, 1A, 1B, 1C, 2A, 2B, 2C, 3A, 3B, 3C)
    donde robot puede tener los valores "1A", "1B", "1C", "2A", "2B", "2C", "3A", "3B", "3C"
    y pueden tener los valores "limpio", "sucio"

    Las acciones válidas en el entorno son ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"].
    Solo algunas acciones son posibles en algunos estados, por ejemplo, no se puede subir si el robot está en 3A.
    Solamente se sube por la derecha y se baja por la izquierda.

    Los sensores es una tupla (robot, limpio?)
    con la ubicación del robot y el estado de limpieza.

    """
    
    def __init__(self, x0=["1A", "Sucio", "Sucio", "Sucio", "Sucio", "Sucio", "Sucio", "Sucio", "Sucio", "Sucio"]):
        super().__init__(x0)
        
    