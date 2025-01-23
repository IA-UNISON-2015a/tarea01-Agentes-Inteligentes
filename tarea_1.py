#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Revisa el archivo README.md con las instrucciones de la tarea.

"""
__author__ = 'Manuel Búsani Yanes'

import entornos_f
from doscuartos_f import AgenteAleatorio

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
				(x == 0 and y != 0) if accion == "bajar" else
				accion in ["ir_Derecha", "ir_Izquierda", "limpiar", "nada"])

	def transicion(self, estado, accion):
		# no se si aqui hay que checar si la accion es legal
		if not self.accion_legal(estado, accion):
			raise ValueError("Error en transicion, la acción recibida no es legal")

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

		return ([x, y, cuartos], c_local)
	
	def percepcion(self, estado):
		x, y, cuartos = estado
		return (x, y, cuartos[x][y])

class AgenteReactivoModeloNueveCuartos(entornos_f.Agente):
    # Un agente reactivo basado en modelo

    def __init__(self):
        # Inicializa el modelo interno
        self.modelo = [0, 0, [[False,False,False],[False,False,False],[False,False,False]]]

    def programa(self, percepcion):
    	x, y, cuarto_limpio = percepcion
    	cuartos = self.modelo[2] 

    	# Actualiza el modelo interno
    	self.modelo[0] = x
    	self.modelo[1] = y
    	self.modelo[2][x][y] = cuarto_limpio

    	# Decide sobre el modelo interno
		return ("limpiar" if not cuarto_limpio else
				"ir_Derecha" if ((x != 2) and (not cuartos[x+1][y]) or
								 (x == 0) and (not(cuartos[2][y]))) else 
				"ir_Izquierda" if ((x != 0) and (not cuartos[x-1][y]) or
								   (x == 2) and (not(cuartos[0][y]))) else
				"subir" if ((x == 0) and (y != 2) and (cuartos[0] != [True, True, True])

