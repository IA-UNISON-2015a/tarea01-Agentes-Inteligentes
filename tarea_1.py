#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Tarea de desarrollo de entornos y agentes
==========================================

1. Desarrolla un entorno similar al de los dos cuartos (el cual se
   encuentra en el módulo doscuartos_f.py), pero con tres cuartos en
   el primer p==o, y tres cuartos en el segundo piso.
   
   El entorno se llamará `SeisCuartos`.

   Las acciones totales serán
   
   ```
   ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]
   ``` 
    
   La acción de `"subir"` solo es legal en el piso de abajo, en los cuartos de los extremos, 
   mientras que la acción de `"bajar"` solo es legal en el piso de arriba y en el cuarto de el centro (dos
   escaleras para subir, una escalera para bajar).

   Las acciones de subir y bajar son mas costosas en término de
   energía que ir a la derecha y a la izquierda, por lo que la función
   de desempeño debe de ser de tener limpios todos los cuartos, con el
   menor numero de acciones posibles, y minimizando subir y bajar en
   relación a ir a los lados. El costo de limpiar es menor a los costos
   de cualquier acción.

2. Diseña un Agente reactivo basado en modelo para este entorno y
   compara su desempeño con un agente aleatorio despues de 100 pasos
   de simulación.

3. Al ejemplo original de los dos cuartos, modificalo de manera que el
   agente solo pueda saber en que cuarto se encuentra pero no sabe si
   está limpio o sucio.

   A este nuevo entorno llamalo `DosCuartosCiego`.

   Diseña un agente racional para este problema, pruebalo y comparalo
   con el agente aleatorio.

4. Reconsidera el problema original de los dos cuartos, pero ahora
   modificalo para que cuando el agente decida aspirar, el 80% de las
   veces limpie pero el 20% (aleatorio) deje sucio el cuarto. Igualmente, 
   cuando el agente decida cambiar de cuarto, se cambie correctamente de cuarto el 90% de la veces
   y el 10% se queda en su lugar. Diseña
   un agente racional para este problema, pruebalo y comparalo con el
   agente aleatorio.

   A este entorno llámalo `DosCuartosEstocástico`.

Todos los incisos tienen un valor de 25 puntos sobre la calificación de
la tarea.

"""
__author__ = 'MiguelRomero'

import entornos_f
from random import choice, randint

# Requiere el modulo entornos_f.py
# Usa el modulo doscuartos_f.py para reutilizar código
# Agrega los modulos que requieras de python


class NueveCuartos(entornos_f.Entorno):

    def acción_legal(self, s, a):
        """
        @param s: Una tupla con un estado legal del entorno
        @param a: Una accion en el entorno

        Las acciones son: subir, bajar, ir_Izquierda, ir_Derecha, limpiar, nada.

        @return: True si accion es legal en estado, False en caso contrario

        Por default acepta cualquier acción.

        """

        robot, A, B, C, D, E, F, G, H, I = s
        

        if a == "subir":
            if robot == "C" or robot == "F":
                return True
            else:
                return False

        elif a == "bajar":
            if robot == "G" or robot == "D":
                return True
            else:
                return False

        elif a == "ir_Izquierda":
            if robot == "A" or robot == "D" or robot == "G":
                return False
            else: return True

        elif a == "ir_Derecha":
            if robot == "C" or robot == "F" or robot == "I":
                return False
            else: return True

        elif a == "limpiar" or a == "nada":
            return True
        
        else: return False
             

    #Fin funcion accion_legal



    def transición(self, s, a):

        """
        @param s: Una tupla con un estado legal del entorno
        @param a: Una accion en el entorno

        @return: (s_n, c_local) una tupla con el nuevo estado y
                 el costo de ir de s a s_n con la acción a

        """

        robot, A, B, C, D, E, F, G, H, I = s

        

        if A == B == C == D == E == F == G == H == I == "limpio" \
           and a == "nada":
            c_local = 0

        elif a == "nada":
            c_local = 1
        
        elif a == "limpiar":
            c_local = 2
        elif a == "ir_Izquierda" or a == "ir_Derecha":
            c_local = 3
        elif a == "subir" or a == "bajar":
            c_local = 4



        if a == "limpiar":
            if robot == "A":
                A = "limpio"
            elif robot == "B":
                B = "limpio"
            elif robot == "C":
                C = "limpio"
                
            elif robot == "D":
                D = "limpio"
            elif robot == "E":
                E = "limpio"
            elif robot == "F":
                F = "limpio"
                
            elif robot == "G":
                G = "limpio"
            elif robot == "H":
                H = "limpio"
            elif robot == "I":
                I = "limpio"


        elif a == "ir_Izquierda":
            if robot == "B":
                robot = "A"
            elif robot == "C":
                robot = "B"

            if robot == "E":
                robot = "D"
            elif robot == "F":
                robot = "E"

            if robot == "H":
                robot = "G"
            elif robot == "I":
                robot = "H"


        elif a == "ir_Derecha":
            if robot == "A":
                robot = "B"
            elif robot == "B":
                robot = "C"

            if robot == "D":
                robot = "E"
            elif robot == "E":
                robot = "F"

            if robot == "G":
                robot = "H"
            elif robot == "H":
                robot = "I"

        elif a == "subir":
            if robot == "C":
                robot = "F"
            elif robot == "F":
                robot = "I"

        elif a == "bajar":
            if robot == "D":
                robot = "A"
            elif robot == "G":
                robot = "D"  
        

        s = (robot, A, B, C, D, E, F, G, H, I)

        return (s, c_local)

    #Fin funcion transicion


    def percepción(self, s):
        """
        @param s: Una tupla con un estado legal del entorno
        @return: Tupla con los valores que se perciben del entorno por
                 default el estado completo

        """

        cuarto_actual = s[0]
        estatus_cuarto = s[" ABCDEFGHI".find(cuarto_actual)]
        
        return cuarto_actual, estatus_cuarto

    #Fin funcion percepcion


#Fin clase NueveCuartos

#########################################################################


class AgenteNueveCuartosEstocastico(NueveCuartos):


    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = ['A', 'sucio', 'sucio', 'sucio',
                       'sucio', 'sucio', 'sucio',
                       'sucio', 'sucio', 'sucio']

    #Fin constructor


    def programa(self, percepción):
        robot, situación = percepción

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[' ABCDEFGHI'.find(robot)] = situación

        # Decide sobre el modelo interno
        a, b, c, d, e, f, g, h , i = self.modelo[1], self.modelo[2], self.modelo[3], \
                                     self.modelo[4], self.modelo[5], self.modelo[6], \
                                     self.modelo[7], self.modelo[8], self.modelo[9]


        n = randint(1, 100)

        if a == b == c == \
           d == e == f ==\
           g == h == i == "limpio":

            sig_accion = "nada"
            
        elif situación == "sucio":
            if n <= 80:
                sig_accion = "limpiar"
            else:
                sig_accion = "limpiar"
            
        elif robot == "A":
            if n <= 80:
                sig_accion = "ir_Derecha"
            elif n > 80 and n <= 90:
                sig_accion = choice(["nada", "limpiar"])
            else:
                sig_accion = "nada"
        
        elif robot == "B":

            if a == "sucio" and n <= 80:
                sig_accion = "ir_Izquierda"    
            elif n <= 80:
                sig_accion = "ir_Derecha"
            elif n > 80 and n <= 90:
                sig_accion = choice(["nada", "limpiar"])
            else:
                sig_accion = "nada"

        elif robot == "C":

            if b == "sucio" and n <= 80:
                sig_accion = "ir_Izquierda"
            elif n <= 80:
                sig_accion = "subir"
            elif n > 80 and n <= 90:
                sig_accion = choice(["nada", "limpiar"])
            else:
                sig_accion = "nada"

        elif robot == "D":

            if e == "sucio" and n <= 80:
                sig_accion = "ir_Derecha"
            elif n <= 80:
                sig_accion = "bajar"
            elif n > 80 and n <= 90:
                sig_accion = choice(["nada", "limpiar"])
            else:
                sig_accion = "nada"

        elif robot == "E":

            if d == "sucio" and n <= 80:
                sig_accion = "ir_Izquierda"
            elif n <= 80:
                sig_accion = "ir_Derecha"
            elif n > 80 and n <= 90:
                sig_accion = choice(["nada", "limpiar"])
            else:
                sig_accion = "nada"

        elif robot == "F":

            if e == "sucio" and n <= 80:
               sig_accion = "ir_Izquierda"
            elif n <= 80:
                sig_accion = "subir"
            elif n > 80 and n <= 90:
                sig_accion = choice(["nada", "limpiar"])
            else:
                sig_accion = "nada"

        elif robot == "G":

            if h == "sucio" and n <= 80:
                sig_accion = "ir_Derecha"
            elif n <= 80:
                sig_accion = "bajar"
            elif n > 80 and n <= 90:
                sig_accion = choice(["nada", "limpiar"])
            else:
                sig_accion = "nada"

        elif robot == "H":

            if i == "sucio" and n <= 80:
                sig_accion = "ir_Derecha"
            elif n <= 80:
                sig_accion = "ir_Izquierda"
            elif n > 80 and n <= 90:
                sig_accion = choice(["nada", "limpiar"])
            else:
                sig_accion = "nada"

        elif robot == "I":

            if n <= 80:
                sig_accion = "ir_Izquierda"
            elif n > 80 and n <= 90:
                sig_accion = choice(["nada", "limpiar"])
            else:
                sig_accion = "nada"
        
        
        return sig_accion
        
    #Fin funcion programa
       
                    

#Fin clase AgenteNueveCuartosEstocastico

#######################################################################

class AgenteRacionalNueveCuartosCiego(entornos_f.Agente):

    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = ['A', 'sucio', 'sucio', 'sucio',
                       'sucio', 'sucio', 'sucio',
                       'sucio', 'sucio', 'sucio']

    #Fin constructor


    def programa(self, percepción):
        robot, situación = percepción

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[' ABCDEFGHI'.find(robot)] = situación

        # Decide sobre el modelo interno
        a, b, c, d, e, f, g, h , i = self.modelo[1], self.modelo[2], self.modelo[3], \
                                     self.modelo[4], self.modelo[5], self.modelo[6], \
                                     self.modelo[7], self.modelo[8], self.modelo[9]

        if a == b == c == \
           d == e == f ==\
           g == h == i == "limpio":

            sig_accion = "nada"
            
        elif robot == "A":
            sig_accion = choice(["ir_Derecha", "limpiar", "nada"])

        elif robot == "B":

            sig_accion = choice(["ir_Derecha", "ir_Izquierda", "limpiar", "nada"])

        elif robot == "C":

            sig_accion = choice(["ir_Izquierda", "subir", "limpiar", "nada"])

        elif robot == "D":

            sig_accion = choice(["ir_Derecha", "bajar", "limpiar", "nada"])

        elif robot == "E":

            sig_accion = choice(["ir_Derecha", "ir_Izquierda", "limpiar", "nada"])

        elif robot == "F":

            sig_accion = choice(["subir", "ir_Izquierda", "limpiar", "nada"])

        elif robot == "G":

            sig_accion = choice(["ir_Derecha", "bajar", "limpiar", "nada"])

        elif robot == "H":

            sig_accion = choice(["ir_Derecha", "ir_Izquierda", "limpiar", "nada"])

        elif robot == "I":

            sig_accion = choice(["ir_Izquierda", "limpiar", "nada"])
        
        
        return sig_accion

    #Fin funcion programa
    

#Fin clase AgenteRacionalNueveCuartosCiego
    
#####################################################################################
    

class AgenteAleatorio(entornos_f.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales

    """
    def __init__(self, acciones):
        self.acciones = acciones
        

    def programa(self, percepción):
        
        robot, situación = percepción

        
        if robot == "A":
            sig_accion = choice(["nada", "limpiar", "ir_Derecha"])

        elif robot == "B":
            sig_accion = choice(["nada", "limpiar", "ir_Izquierda", "ir_Derecha"])

        elif robot == "C":
            sig_accion = choice(["nada", "limpiar", "ir_Izquierda", "subir"])

        elif robot == "D":
            sig_accion = choice(["nada", "limpiar", "bajar", "ir_Derecha"])

        elif robot == "E":
            sig_accion = choice(["nada", "limpiar", "ir_Derecha", "ir_Izquierda"])

        elif robot == "F":
            sig_accion = choice(["nada", "limpiar", "subir", "ir_Izquierda"])

        elif robot == "G":
            sig_accion = choice(["nada", "limpiar", "ir_Derecha", "bajar"])

        elif robot == "H":
            sig_accion = choice(["nada", "limpiar", "ir_Derecha", "ir_Izquierda"])

        elif robot == "I":
            sig_accion = choice(["nada", "limpiar", "ir_Izquierda"])
            
            
        return sig_accion

    #Fin funcion programa    


#Fin clase AgenteAleatorio

###################################################


class AgenteReactivoModeloNueveCuartos(entornos_f.Agente):

    """
    Un agente reactivo basado en modelo

    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = ['A', 'sucio', 'sucio', 'sucio',
                       'sucio', 'sucio', 'sucio',
                       'sucio', 'sucio', 'sucio']

    #Fin constructor


    def programa(self, percepción):
        robot, situación = percepción

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[' ABCDEFGHI'.find(robot)] = situación

        # Decide sobre el modelo interno
        a, b, c, d, e, f, g, h , i = self.modelo[1], self.modelo[2], self.modelo[3], \
                                     self.modelo[4], self.modelo[5], self.modelo[6], \
                                     self.modelo[7], self.modelo[8], self.modelo[9]


        if a == b == c == \
           d == e == f ==\
           g == h == i == "limpio":

            sig_accion = "nada"
            
        elif situación == "sucio":
            sig_accion = "limpiar"
            
        elif robot == "A":
            sig_accion = "ir_Derecha"

        elif robot == "B":

            if a == "sucio":
                sig_accion = "ir_Izquierda"    
            else:
                sig_accion = "ir_Derecha"

        elif robot == "C":

            if b == "sucio":
                sig_accion = "ir_Izquierda"
            else:
                sig_accion = "subir"

        elif robot == "D":

            if e == "sucio":
                sig_accion = "ir_Derecha"
            else:
                sig_accion = "bajar"

        elif robot == "E":

            if d == "sucio":
                sig_accion = "ir_Izquierda"
            else:
                sig_accion = "ir_Derecha"

        elif robot == "F":

            if e == "sucio":
               sig_accion = "ir_Izquierda"
            else:
                sig_accion = "subir"

        elif robot == "G":

            if h == "sucio":
                sig_accion = "ir_Derecha"
            else:
                sig_accion = "bajar"

        elif robot == "H":

            if i == "sucio":
                sig_accion = "ir_Derecha"
            else:
                sig_accion = "ir_Izquierda"

        elif robot == "I":

            sig_accion = "ir_Izquierda"
        
        
        return sig_accion


#Fin clase AgenteReactivoModeloNueveCuartos

def prueba_agente(agente):
    entornos_f.imprime_simulación(
        entornos_f.simulador(
            NueveCuartos(),
            agente,
            ["A", "sucio", "sucio", "sucio",
                "sucio", "sucio", "sucio",
                "sucio", "sucio", "sucio"],
            200
        ),
        ['A', 'sucio', 'sucio', 'sucio',
            'sucio', 'sucio', 'sucio',
            'sucio', 'sucio', 'sucio']
    )

def test():
    """
    Prueba del entorno y los agentes

    """
    print("Prueba del entorno con un agente aleatorio")
    prueba_agente(AgenteAleatorio(['subir', 'bajar', 'ir_Izquierda', 'ir_Derecha', 'limpiar', 'nada']))

    print("Prueba del entorno con un agente reactivo con modelo")
    prueba_agente(AgenteReactivoModeloNueveCuartos())

    print("Prueba del entorno ciego con un agente racional.")
    prueba_agente(AgenteRacionalNueveCuartosCiego())

    print("Prueba del entorno con un agente estocástico.")
    prueba_agente(AgenteNueveCuartosEstocastico())


if __name__ == "__main__":
    test()    


