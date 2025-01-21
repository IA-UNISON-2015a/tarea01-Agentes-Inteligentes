#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Revisa el archivo README.md con las instrucciones de la tarea.

"""
__author__ = 'Raul Leoanrdo Lopez Ruiz'

import entornos_f
from random import choice

class NueveCuartos(entornos_f.Entorno):
    def accion_legal(self,_,accion):
        return accion in ("ir_Derecha", "ir_Izquierda","Subir",
                          "Bajar","Limpiar","Nada")
    def transicion(self, estado, accion):
        robot, a,b,c,d,e,f,g,h,i = estado
        
        if accion in ["ir_Derecha", "ir_Izquierda", "Nada"]:
            c_local = 1
        elif accion == "Limpiar":
            c_local = 0
        else:
            c_local = 2
        
        return ((estado, c_local) if a == "Nada" else
                (("B",a,b,c,d,e,f,g,h,i),c_local) if robot == "A" and accion == "ir_Izquierda" 
                    or robot == "C" and accion == "ir_Derecha" else 
                (("E",a,b,c,d,e,f,g,h,i),c_local) if robot == "F" and accion == "ir_Izquierda"
                    or robot == "D" and accion == "ir_Derecha" else
                (("H",a,b,c,d,e,f,g,h,i),c_local)if robot == "I" and accion == "ir_Izquierda"
                    or robot == "G" and accion == "ir_Derecha" else
                (("A",a,b,c,d,e,f,g,h,i),c_local) if robot == "B" and accion == "ir_Derecha" else
                (("D",a,b,c,d,e,f,g,h,i),c_local) if robot == "E" and accion == "ir_Derecha"
                    or robot == "A" and accion == "Subir" else
                (("G",a,b,c,d,e,f,g,h,i),c_local) if robot == "H" and accion == "ir_Izquierda" 
                    or robot == "D" and accion == "Subir" else
                (("C",a,b,c,d,e,f,g,h,i),c_local) if robot == "B" and accion == "ir_Izquierda"
                    or robot == "F" and accion == "Bajar" else
                (("F",a,b,c,d,e,f,g,h,i),c_local) if robot == "E" and accion == "ir_Izquierda"
                    or robot == "I" and accion == "Bajar" else
                (("I",a,b,c,d,e,f,g,h,i),c_local) if robot == "H" and accion == "ir_Izquierda"else
                ((robot,"limpio",b,c,d,e,f,g,h,i),c_local))        
        
                
    def percepcion(self, estado):
        return estado[0], estado[" ABCDEFGHI".find(estado[0])] 

class AgenteReactivoModeloNueveCuartos(entornos_f.Agente):
    """
    Un agente reactivo basado en modelo

    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = ['A', 'sucio', 'sucio','sucio','sucio','sucio','sucio','sucio','sucio','sucio']

    def programa(self, percepción):
        robot, situación = percepción

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[' ABCDEFGHI'.find(robot)] = situación

        # Decide sobre el modelo interno
        a, b,c,d,e,f,g,h,i = self.modelo[1], self.modelo[2],self.modelo[3],self.modelo[4],self.modelo[5],self.modelo[6],self.modelo[7],self.modelo[8],self.modelo[9]
        return ('Nada' if a == b == c == d == e == f == g == h == i == 'limpio' else
                'Limpiar' if situación == 'sucio' else
                 'ir_Derecha' if robot in ['B','C','E','F','H','I'] else
                 'ir_Izquierda' if robot in ['A','B','D','E','G','H'] else
                 'Subir' if robot in ['A','D'] else 
                 'bajar' if robot in ['I','F'] else
                 'otra accion')



class AgenteAleatorio(entornos_f.Agente):
    def __init__(self,acciones):
        self.acciones = acciones

    def programa(self, p):
        return choice(self.acciones)

def prueba_agente(agente):
    entornos_f.imprime_simulacion(
        entornos_f.simulador(
            NueveCuartos(),
            agente,
            ["A", "sucio", "sucio","sucio","sucio","sucio","sucio","sucio","sucio","sucio"],
            200
        ),
        ["A", "sucio", "sucio","sucio","sucio","sucio","sucio","sucio","sucio","sucio"]
    )

def test():
    """
    Prueba del entorno y los agentes

    """
    print("Prueba del entorno con un agente aleatorio")
    prueba_agente(AgenteAleatorio(['ir_Derecha', 'ir_Izquierda', 'Subir', 'Bajar','Limpiar','Nada']))

    #print("Prueba del entorno con un agente reactivo con modelo")
    #prueba_agente(AgenteReactivoModeloNueveCuartos())

if __name__ == "__main__":
    test()

# Requiere el modulo entornos_f.py o entornos_o.py
# Usa el modulo doscuartos_f.py para reutilizar código
# Agrega los modulos que requieras de python

