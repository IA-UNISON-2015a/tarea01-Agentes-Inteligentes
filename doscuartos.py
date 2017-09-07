#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SeisCuartos.py.py
------------

#probando de nuevo atte temoc

Ejemplo de un entorno muy simple y agentes idem

"""

__author__ = 'Jose Cuauhtemoc Moyron Higuera'

import entornos
from random import choice


class SeisCuartos(entornos.Entorno):
    """
    Empezare por definir la distribuicion de los cuartos 
    
                | D | | E | | F | 
                | A | | B | | C |

                
    donde robot puede tener los valores "A","B","C","D","E","F"
    A,B,C,D,E,F pueden tener los valores "limpio" o "sucio"

    Las acciones válidas en el entorno son :
            "irDerecha","irIzquierda" "subir" "bajar" "limpiar" y "noOp". 
    Casi todas las acciones son válidas, sabemos que en todos los cuartos podemos limpiar o no limpiar,
    pero al trasladarnos hay movimientos permitidos y no permitidos (ejemplo: los cuartos A,B,C son los de
    la planta baja, E,D,F son la planta alta, por ejemplo no se podra subir en los de la planta alta, ni se p
    podra bajar en la planta baja)

    """

    def transicion(self, estado, accion):
        if not self.accion_legal(estado, accion):
            raise ValueError("La accion no es legal para este estado")
  #  EN LA LINEA SIGUIENTE AGREGAMOS LAS HABITACIONES extras. 
        robot, A, B, C, D, E, F = estado
  # En esta linea creamos una lista que recibe como argumento lo que hay en estado      
        nuevo = list(estado)
        modelo = ('robot','A','B','C','D','E','F')
        
        
        if accion == 'limpiar':
            nuevo[modelo.index(nuevo[0])] = 'limpio'
        elif accion == 'subir':
            nuevo[0] = modelo[modelo.index(nuevo[0]) + 3]
        elif accion == 'bajar':
            nuevo[0] = modelo[modelo.index(nuevo[0]) - 3]
        elif accion == 'irDerecha':
            nuevo[0] = modelo[modelo.index(nuevo[0]) + 1]
        elif accion == 'irIzquierda':
            nuevo[0] = modelo[modelo.index(nuevo[0]) - 1]
 
        return tuple(nuevo) #aqui regresamos una tupla con los datos de la lista nuevo 
    
    def sensores(self, estado):
        
        modelo = ('robot', 'A', 'B', 'C', 'D', 'E', 'F')
        return (estado[0], estado[modelo.index(estado[0])])
        
                
                                    

    def accion_legal(self, estado, accion):
 #       return accion in ('irDerecha', 'irIzquierda', 'subir', 'bajar', 'limpiar', 'noOp')
    """En la siguiente declaracion tenemos la condicional de que si estamos en D o en A no podemos ir
            a la izquierda 
            |-D | | E | | F | 
            |-A | | B | | C |
    """
         if (estado[0] == 'A' or estado[0] == 'D') and accion == 'irIzquierda'):
            return False
        
        
        """En la siguiente declaracion tenemos la condicional de que si estamos en C o en F no podemos ir
            a la Derecha 
            |D | | E | |-F | 
            |A | | B | |-C |
        """
        if (estado[0] == 'C' or estado[0] == 'F') and accion == 'irDerecha'):
            return False
        
        
        """En la siguiente declaracion tenemos la condicional en la cual dice que si lo que esta en estado 
           es menor o igual a D entonces quiere decir que estamos en el piso de abajo por lo tanto no 
           podremos ir abajo 
            | D | | E | | F | 
            |-A | |-B | |-C |
        """
        if (estado[0] == <'D' and accion == 'bajar'):
            return False
        
        
        """En la siguiente declaracion tenemos la condicional en la cual dice que si lo que esta en estado 
           es mayor o igual que D entonces quiere decir que estamos en el piso de arriba por lo tanto no 
           podremos subir  
            |-D | |-E | |-F | 
            | A | | B | | C |
        """
        if (estado[0] == >'D' and accion == 'subir'):
            return False
        
    def desempeno_local(self, estado, accion):
        robot, A, B, C, D, E, F  = estado
        if accion == 'subir' or accion == 'bajar' :
            return -2 
        if accion == 'noOp' and not 'sucio' in estado :
            return 0
        return -1 


class AgenteAleatorio(entornos.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales

    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, percepcion):
        return choice(self.acciones)


class AgenteReactivoDoscuartos(entornos.Agente):
    """
    Un agente reactivo simple

    """

    def programa(self, percepcion):
        robot, situacion = percepcion
        return ('limpiar' if situacion == 'sucio' else
                'irA' if robot == 'B' else
                'irB')


class AgenteReactivoModeloDosCuartos(entornos.Agente):
    """
    Un agente reactivo basado en modelo

    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = ['A', 'sucio', 'sucio']
        self.lugar = {'A': 1, 'B': 2}

    def programa(self, percepcion):
        robot, situacion = percepcion

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[self.lugar[robot]] = situacion

        # Decide sobre el modelo interno
        A, B = self.modelo[1], self.modelo[2]
        return ('noOp' if A == B == 'limpio' else
                'limpiar' if situacion == 'sucio' else
                'irA' if robot == 'B' else
                'irB')


def test():
    """
    Prueba del entorno y los agentes

    """
    print "Prueba del entorno de dos cuartos con un agente aleatorio"
    entornos.simulador(SeisCuartos(),
                       AgenteAleatorio(['irA', 'irB', 'limpiar', 'noOp']),
                       ('A', 'sucio', 'sucio'), 100)

    print "Prueba del entorno de dos cuartos con un agente reactivo"
    entornos.simulador(DosCuartos(),
                       AgenteReactivoDoscuartos(),
                       ('A', 'sucio', 'sucio'), 100)

    print "Prueba del entorno de dos cuartos con un agente reactivo"
    entornos.simulador(DosCuartos(),
                       AgenteReactivoModeloDosCuartos(),
                       ('A', 'sucio', 'sucio'), 100)

if __name__ == '__main__':
    test()
