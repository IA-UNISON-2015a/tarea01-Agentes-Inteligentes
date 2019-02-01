#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Tarea de desarrollo de entornos y agentes
==========================================

1. Desarrolla un entorno similar al de los dos cuartos (el cual se encuentra en el módulo doscuartos_o.py), pero con
   tres cuartos en el primer piso, tres cuartos en el segundo piso y tres cuartos en el 3er piso.

   El entorno se llamará NueveCuartos.

   Las acciones totales serán

   ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]
   La acción de "subir" solo es legal en los primeros dos pisos, en los cuartos de la derecha, mientras que la acción 
   de "bajar" solo es legal en los dos pisos de arriba de arriba y en el cuarto de la izquierda.

   Las acciones de subir y bajar son mas costosas en término de energía que ir a la derecha y a la izquierda, por lo 
   que la función de desempeño debe de ser de tener limpios todos los cuartos, con el menor numero de acciones 
   posibles, y minimizando subir y bajar en relación a ir a los lados. El costo de limpiar es menor a los costos   
   de cualquier acción. DONE

2. Diseña un Agente reactivo basado en modelo para este entorno y compara su desempeño con un agente aleatorio 
   despues de 200 pasos de simulación.

3. A este modelo de NueveCuartos, modificalo de manera que el agente solo pueda saber en que cuarto se encuentra pero
   no sabe si está limpio o sucio. Utiliza la herencia entre clases para no escribir código redundante.

   A este nuevo entorno llamalo NueveCuartosCiego.

   Diseña un agente racional para este problema, pruebalo y comparalo con el agente aleatorio.

4. Al modelo original de NueveCuartos modificalo para que cuando el agente decida aspirar, el 80% de las veces limpie
   pero el 20% (aleatorio) deje sucio el cuarto. Igualmente, cuando el agente decida cambiar de cuarto, se cambie 
   correctamente de cuarto el 80% de la veces, el 10% de la veces se queda en su lugar y el 10% de las veces realiza 
   una acción legal aleatoria. Diseña un agente racional para este problema, pruebalo y comparalo con el agente aleatorio.

   A este entorno llámalo NueveCuartosEstocástico.

Todos los incisos tienen un valor de 25 puntos sobre la calificación de la tarea.

"""
__author__ = 'Lizeth Soto Félix'

import entornos_o
from random import choice


class NueveCuartos(entornos_o.Entorno):
    """
    El estado se define como (robot, A, B, C, piso_actual, estado_piso_1, estado_piso_2, estado_piso_3)
    donde robot puede tener los valores "A", "B"
    A y B pueden tener los valores "limpio", "sucio"

    Las acciones válidas en el entorno son ("ir_A", "ir_B", "limpiar", "nada").
    Todas las acciones son válidas en todos los estados.

    Los sensores es una tupla (robot, limpio?, piso)
    con la ubicación del robot y el estado de limpieza

    """
    def __init__(self, x0=[1, "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio","sucio","sucio"]):
        """
        Por default inicialmente el robot está en A y los dos cuartos
        están sucios

        """
        self.x = x0[:]
        self.desempeño = 0
        self.a_legal={1:["ir_Derecha"],
                      2:["ir_Derecha","ir_Izquierda"],
                      3:["ir_Izquierda","subir"],
                      4:["ir_Derecha","bajar"],
                      5:["ir_Izquierda","ir_Derecha"],
                      6:["ir_Izquierda","subir"],
                      7:["ir_Derecha"],
                      8:["ir_Izquierda","ir_Derecha"],
                      9:["ir_Izquierda"],
                      }

    def acción_legal(self, acción):
        robot = self.x[0]
        #print("robot",robot)
        #print(self.a_legal[int(robot)])
        acc_legal_lista=self.a_legal[robot] + ["limpiar", "nada"] 
        #print(acc_legal_lista)
        return acción in acc_legal_lista

    def transición(self, acción):
        if not self.acción_legal(acción):
            raise ValueError("La acción no es legal para este estado")

        if acción is "nada" and any(cuarto is "sucio" for cuarto in self.x):
            self.desempeño -= 2
        if acción is "limpiar":
            self.x[" 123456789".find(str(self.x[0]))] = "limpio"
            self.desempeño -= 1
        elif acción is "ir_Izquierda":
            self.desempeño -= 3
            self.x[0] -= 1 
        elif acción is "ir_Derecha":
            self.desempeño -= 3
            self.x[0] += 1
        elif acción is "subir":
            self.desempeño -= 13
            self.x[0] += 3
        elif acción is "bajar":
            self.desempeño -= 13
            self.x[0] -= 3


    def percepción(self):
        return self.x[0], self.x[" 123456789".find(str(self.x[0]))]


class AgenteAleatorio(entornos_o.Agente,NueveCuartos):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales

    """
    def __init__(self, acciones):
        self.a_legal={1:["ir_Derecha"],
                      2:["ir_Derecha","ir_Izquierda"],
                      3:["ir_Izquierda","subir"],
                      4:["ir_Derecha","bajar"],
                      5:["ir_Izquierda","ir_Derecha"],
                      6:["ir_Izquierda","subir"],
                      7:["ir_Derecha"],
                      8:["ir_Izquierda","ir_Derecha"],
                      9:["ir_Izquierda"],
                      }
        self.acciones = acciones

    def programa(self, percepcion):
        robot,situacion_cuarto = percepcion
        self.x=[robot,situacion_cuarto]
        lista_legales_nolegales= list(self.acciones)
        lista_legales=[ac for ac in lista_legales_nolegales if self.acción_legal(ac)]
        #choice1 = choice(lista_legales)
        #print("lista:",lista_legales)
        #print("choice:", choice1)
        return (choice(lista_legales))



#class AgenteReactivoDoscuartos(entornos_o.Agente):
    #"""
   # Un agente reactivo simple

   # """
   # def programa(self, percepción):
   #     robot, situación = percepción
    #    return ('limpiar' if situación == 'sucio' else
   #             'ir_A' if robot == 'B' else 'ir_B')


class AgenteReactivoModeloNueveCuartos(entornos_o.Agente,NueveCuartos):
    """
    Un agente reactivo basado en modelo

    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.a_legal={1:["ir_Derecha"],
                      2:["ir_Derecha","ir_Izquierda"],
                      3:["ir_Izquierda","subir"],
                      4:["ir_Derecha","bajar"],
                      5:["ir_Izquierda","ir_Derecha"],
                      6:["ir_Izquierda","subir"],
                      7:["ir_Derecha"],
                      8:["ir_Izquierda","ir_Derecha"],
                      9:["ir_Izquierda"],
                      }
        self.modelo = [1, "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio","sucio","sucio"]

    def programa(self, percepción):
        robot, situación = percepción

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[' 123456789'.find(str(robot))] = situación

        cuartos = self.modelo[1:]
        piso_1 = cuartos[0:3]
        piso_2 = cuartos[3:6]
        piso_3 = cuartos[6:]

        if all(cuarto is "limpio" for cuarto in cuartos):
            return "nada"
        elif situación == "sucio":
            return "limpiar"
        elif robot<=3:
            if any(cuarto is "sucio" for cuarto in piso_1):
                acc_pref = set(self.a_legal[robot]).intersection(["ir_Izquierda","ir_Derecha"])
                return choice(acc_pref)
        elif robot>3 and robot<=7:
            if any(cuarto is "sucio" for cuarto in piso_2):
                acc_pref = set(self.a_legal[robot]).intersection(["ir_Izquierda","ir_Derecha"])
                return choice(acc_pref)
        # Decide sobre el modelo interno
        #a, b = self.modelo[1], self.modelo[2]
        
        return ('nada' if a == b == 'limpio' else
                'limpiar' if situación == 'sucio' else
                'ir_A' if robot == 'B' else 'ir_B')


def test():
    """
    Prueba del entorno y los agentes

    """
    #print("Prueba del entorno con un agente aleatorio")
    #entornos_o.simulador(NueveCuartos(),
                         #AgenteAleatorio(['ir_Izquierda', 'ir_Derecha', 'limpiar', 'nada', "subir", "bajar"]),
                         #50)

    #print("Prueba del entorno con un agente reactivo")
    #entornos_o.simulador(DosCuartos(), AgenteReactivoDoscuartos(), 100)

    print("Prueba del entorno con un agente reactivo con modelo")
    entornos_o.simulador(NueveCuartos(), AgenteReactivoModeloNueveCuartos(), 100)


if __name__ == "__main__":
    test()