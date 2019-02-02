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
   despues de 200 pasos de simulación. DONE

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
import random
#from random import choice


class NueveCuartos(entornos_o.Entorno):
    """
    El estado se define como (robot, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    donde robot puede tener los valores del 1-9
    1-9 pueden tener los valores "limpio", "sucio"

    Las acciones válidas en el entorno son ("ir_Izquierda", "ir_Derecha", "limpiar", "nada","subir, "bajar").
    Todas las acciones son válidas en todos los estados.


    """
    def __init__(self, x0=[5, "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio","sucio","sucio"]):
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
        acc_legal_lista=self.a_legal[robot] + ["limpiar", "nada"] 
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

"""
*****************************************************************************************************************************************************
"""

class NueveCuartosEstocástico(entornos_o.Entorno):
    """
    El estado se define como (robot, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    donde robot puede tener los valores del 1-9
    1-9 pueden tener los valores "limpio", "sucio"

    Las acciones válidas en el entorno son ("ir_Izquierda", "ir_Derecha", "limpiar", "nada","subir, "bajar").
    Todas las acciones son válidas en todos los estados.

    """
    def __init__(self, x0=[5, "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio","sucio","sucio"]):
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
        acc_legal_lista=self.a_legal[robot] + ["limpiar", "nada"] 
        return acción in acc_legal_lista

    def transición(self, acción, segunda_vuelta=False):
        ran_num = random.uniform(0, 1) if not segunda_vuelta else 0
        if not self.acción_legal(acción):
            raise ValueError("La acción no es legal para este estado")

        if acción is "nada" and any(cuarto is "sucio" for cuarto in self.x):
            self.desempeño -= 2
        if acción is "limpiar":
            
            if ran_num<=0.20:
                self.x[" 123456789".find(str(self.x[0]))] = "limpio"
                self.desempeño -= 1
            else:
                #print("nokeyo")
                self.desempeño -= 2
        elif acción is "ir_Izquierda":
            if ran_num<=0.80:
                self.desempeño -= 3
                self.x[0] -= 1
            elif ran_num<=0.90:
                self.desempeño -= 2
            else:
                self.transición(random.choice(self.a_legal[self.x[0]]),True)
                
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
                      7:["ir_Derecha","bajar"],
                      8:["ir_Izquierda","ir_Derecha"],
                      9:["ir_Izquierda"],
                      }
        self.acciones = acciones

    def programa(self, percepcion):
        robot,situacion_cuarto = percepcion
        self.x=[robot,situacion_cuarto]
        lista_legales_nolegales= list(self.acciones)
        lista_legales=[ac for ac in lista_legales_nolegales if self.acción_legal(ac)]
        return (random.choice(lista_legales))

class AgenteReactivoModeloNueveCuartos(entornos_o.Agente):
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
        self.modelo[0] = robot
        self.modelo[' 123456789'.find(str(robot))] = situación
        piso_1 = self.modelo[1:4]
        piso_2 = self.modelo[4:7]
        piso_3 = self.modelo[7:]
        print(piso_3)
        print(piso_2)
        print(piso_1)
        print("")
        

        if all(cuarto is "limpio" for cuarto in self.modelo[1:]):
            return "nada"
        
        elif situación == "sucio":
            return "limpiar"
        
        elif robot<=3:
            if robot is 1:
                return "ir_Derecha"
            elif robot is 2 and piso_1[0] is "sucio":
                return "ir_Izquierda"
            elif robot is 2 and piso_1[0] is "limpio":
                return "ir_Derecha"
            elif any(cuarto is "sucio" for cuarto in piso_1) and robot is 3:
                return "ir_Izquierda"
            else: 
                return "subir"
            
        elif robot>3 and robot<=7:
            if robot is 6:
                if all(cuarto is "limpio" for cuarto in piso_2):
                    if all(cuarto is "limpio" for cuarto in piso_3):
                        return "ir_Izquierda"
                    else: 
                        return "subir"
                else:
                    return "ir_Izquierda"
            elif robot is 5:
                if all(cuarto is "limpio" for cuarto in piso_1):
                    if piso_2[0] is "sucio": 
                        return "ir_Izquierda"
                    else:
                        return "ir_Derecha"
                else:
                    if piso_2[2] is "sucio": 
                        return "ir_Derecha"
                    else:
                        return "ir_Izquierda"
            elif any(cuarto is "sucio" for cuarto in piso_2) and robot is 4:
                return "ir_Derecha"
            else: 
                return "bajar"
            
        elif robot>7:
            if robot is 9:
                return "ir_Izquierda"
            elif robot is 8 and piso_3[2] is "sucio":
                return "ir_Derecha"
            elif robot is 8 and piso_3[2] is "limpio":
                return "ir_Izquierda"
            elif any(cuarto is "sucio" for cuarto in piso_3) and robot is 7:
                return "ir_Derecha"
            else: return "bajar"

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

    #print("Prueba del entorno con un agente reactivo con modelo")
    #entornos_o.simulador(NueveCuartos(), AgenteReactivoModeloNueveCuartos(), 50)

    print("Prueba del entorno con un agente reactivo con modelo")
    entornos_o.simulador(NueveCuartosEstocástico(), AgenteReactivoModeloNueveCuartos(), 50)

if __name__ == "__main__":
    test()