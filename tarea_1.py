#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Revisa el archivo README.md con las instrucciones de la tarea.

"""
__author__ = 'Manuel Búsani Yanes'

import entornos_f
# import entornos_o
from random import choice

# Requiere el modulo entornos_f.py o entornos_o.py
# Usa el modulo doscuartos_f.py para reutilizar código
# Agrega los modulos que requieras de python


class NueveCuartos(entornos_f.Entorno):
	'''
	acciones = ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]

	estados = [x, y, cuartos]
	
	x es un número de 0 a 2 y representa la posición horizontal

	y es un número de 0 a 2 y representa la posición vertical

	cuartos es una lista de listas de booleanos donde los indices
	con que se acceden representa el cuarto, e.g cuartos[0][0] es
	el cuarto del primer piso en la izquierda, y el valor booleano
	representa si está limpio o no

	'''
	def accion_legal(self, estado, accion):
		x = estado[0]
		y = estado[1]

		return ((x == 2 and y != 2) if accion == "subir" else
				(x == 0 and y != 0) or accion != "bajar")

	def transicion(self, estado, accion):
		# no se si aqui hay que checar si la accion es legal
		if not self.accion_legal(estado,accion):
			raise ValueError("Error en el agente, ofrece una acción no legal")

		x, y, cuartos = estado

		tmp = [[True,True,True],[True,True,True],[True,True,True]]
		c_local = (3 if ((accion == "subir") or (accion == "bajar")) else 
				   2 if ((accion == "ir_Derecha") or (accion == "ir_Izquierda")) else 
				   0 if ((accion == "nada") and (cuartos == tmp)) else 1)

		if accion == "ir_Derecha":
			x = x+1
		elif accion == "ir_Izquierda":
			x = x-1
		elif accion == "subir":
			y = y+1
		elif accion == "bajar":
			y = y-1
		elif accion == "limpiar":
			cuartos[x][y] = True

		return ([x,y,cuartos], c_local)

