#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Tarea de desarrollo de entornos y agentes
==========================================

1. Desarrolla un entorno similar al de los dos cuartos (el cual se
   encuentra en el módulo doscuartos_o.py), pero con tres cuartos en
   el primer piso, y tres cuartos en el segundo piso.
   
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
__author__ = 'Jose Carlos Pimienta Ibarra'

import entornos_o
from random import choice
from random import randint

# Requiere el modulo entornos_o.py
# Usa el modulo doscuartos_o.py para reutilizar código
# Agrega los modulos que requieras de python
class NueveCuartos(entornos_o.Entorno):
    """
    Clase para un entorno de nueve cuartos. Muy sencilla solo regrupa métodos.
    
    los cuartos estan acomodados de la forma
          _____________
    (down)|_7_|_8_|_9_|
    (down)|_4_|_5_|_6_|(up)
          |_1_|_2_|_3_|(up)

    El estado se define como (robot, 1, 2, ... , 9)
    donde robot puede tener los valores 1-9
    1-9 pueden tener los valores "limpio", "sucio"

    Las acciones válidas en el entorno son ('ir_Derecha', "izg", "subir", "bajar",  "limpiar", "nada").
    No todas las acciones son válidas en todos los estados.
    

    Los sensores es una tupla (robot, limpio?)
    con la ubicación del robot y el estado de limpieza

    """
    def __init__(self, x0=[1, "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]):
        """
        Por default inicialmente el robot está en A y los dos cuartos
        están sucios

        """
        self.x = x0[:]
        self.desempeño = 0

    def acción_legal(self, acción):
        if self.x[0]==1:
            return acción in ('ir_Derecha', "limpiar", "nada")
        if self.x[0]==2:
            return acción in ('ir_Derecha','ir_Izquierda', "limpiar", "nada")
        if self.x[0]==3:
            return acción in ('ir_Izquierda', "subir" , "limpiar", "nada")
        if self.x[0]==4:
            return acción in ('ir_Derecha', "bajar", "limpiar", "nada")
        if self.x[0]==5:
            return acción in ('ir_Derecha','ir_Izquierda', "limpiar", "nada")
        if self.x[0]==6:
            return acción in ('ir_Izquierda', "subir" , "limpiar", "nada")
        if self.x[0]==7:
            return acción in ('ir_Derecha', "bajar", "limpiar", "nada")
        if self.x[0]==8:
            return acción in ('ir_Derecha','ir_Izquierda', "limpiar", "nada")
        if self.x[0]==9:
            return acción in ('ir_Izquierda', "limpiar", "nada")

    def transición(self, acción):
        if not self.acción_legal(acción):
            #raise ValueError("La acción no es legal para este estado")
            acción = "nada"

        robot, a, b, c, d, e, f, g, h, i = self.x
        if acción is not "nada" or "sucio" in {a,b,c,d,e,f,g,h,i}:
            self.desempeño -= 1
        
        # limpiar, ir_Derecha e ir_izquierda cuestan 1
        #subir cuesta 3 y bajar cuesta 2
        if acción is "limpiar":
            self.desempeño-=1
            self.x[self.x[0]] = "limpio"
        elif acción is 'ir_Derecha':
            self.desempeño-=1
            self.x[0] += 1 
        elif acción is 'ir_Izquierda':
            self.desempeño-=1
            self.x[0] -= 1 
        elif acción is "subir":
            self.desempeño-=3
            self.x[0] += 3 
        elif acción is "bajar":
            self.desempeño-=2
            self.x[0] -= 3

    def percepción(self):
        return self.x[0], self.x[self.x[0]]
#---------------------------------------------------------------------
#========NueveCuartosCiego
#---------------------------------------------------------------------
class NueveCuartosCiego(NueveCuartos):
    
    def __init__(self, x0=[1]):
        """
        Por default inicialmente el robot está en A 

        """
        self.x = x0[:]
        self.desempeño = 0

    def acción_legal(self, acción):
        if self.x[0]==1:
            return acción in ('ir_Derecha', "limpiar", "nada")
        if self.x[0]==2:
            return acción in ('ir_Derecha','ir_Izquierda', "limpiar", "nada")
        if self.x[0]==3:
            return acción in ('ir_Izquierda', "subir" , "limpiar", "nada")
        if self.x[0]==4:
            return acción in ('ir_Derecha', "bajar", "limpiar", "nada")
        if self.x[0]==5:
            return acción in ('ir_Derecha','ir_Izquierda', "limpiar", "nada")
        if self.x[0]==6:
            return acción in ('ir_Izquierda', "subir" , "limpiar", "nada")
        if self.x[0]==7:
            return acción in ('ir_Derecha', "bajar", "limpiar", "nada")
        if self.x[0]==8:
            return acción in ('ir_Derecha','ir_Izquierda', "limpiar", "nada")
        if self.x[0]==9:
            return acción in ('ir_Izquierda', "limpiar", "nada")

    def transición(self, acción):
        if not self.acción_legal(acción):
            #raise ValueError("La acción no es legal para este estado")
            acción = "nada"

        robot, a, b, c, d, e, f, g, h, i = self.x
        if acción is not "nada":
            self.desempeño -= 1
        
        # limpiar, ir_Derecha e ir_izquierda cuestan 1
        #subir y bajar cuestan 2
        if acción is "limpiar":
            self.desempeño-=1
        elif acción is 'ir_Derecha':
            self.desempeño-=1
            self.x[0] += 1 
        elif acción is 'ir_Izquierda':
            self.desempeño-=1
            self.x[0] -= 1 
        elif acción is "subir":
            self.desempeño-=2
            self.x[0] += 3 
        elif acción is "bajar":
            self.desempeño-=2
            self.x[0] -= 3

    def percepción(self):
        return self.x[0]
    

#---------------------------------------------------------------------
#========NueveCuartosEstocastico
#---------------------------------------------------------------------
class NueveCuartosEstocastico(entornos_o.Entorno):
    """
    Esta clase es parecida a NueveCuarto
    a diferencia que tiene la incertidumbre  de 
    que a veces no seguira las acciones correctamente

    """
    def __init__(self, x0=[1, "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]):
        """
        Por default inicialmente el robot está en A y los dos cuartos
        están sucios

        """
        self.x = x0[:]
        self.desempeño = 0

    def acción_legal(self, acción):
        if self.x[0]==1:
            return acción in ('ir_Derecha', "limpiar", "nada")
        if self.x[0]==2:
            return acción in ('ir_Derecha','ir_Izquierda', "limpiar", "nada")
        if self.x[0]==3:
            return acción in ('ir_Izquierda', "subir" , "limpiar", "nada")
        if self.x[0]==4:
            return acción in ('ir_Derecha', "bajar", "limpiar", "nada")
        if self.x[0]==5:
            return acción in ('ir_Derecha','ir_Izquierda', "limpiar", "nada")
        if self.x[0]==6:
            return acción in ('ir_Izquierda', "subir" , "limpiar", "nada")
        if self.x[0]==7:
            return acción in ('ir_Derecha', "bajar", "limpiar", "nada")
        if self.x[0]==8:
            return acción in ('ir_Derecha','ir_Izquierda', "limpiar", "nada")
        if self.x[0]==9:
            return acción in ('ir_Izquierda', "limpiar", "nada")

    def transición(self, acción):
        if not self.acción_legal(acción):
            #raise ValueError("La acción no es legal para este estado")
            acción = "nada"

        robot, a, b, c, d, e, f, g, h, i = self.x
        if acción is not "nada" or "sucio" in {a,b,c,d,e,f,g,h,i}:
            self.desempeño -= 1
        
        aleatorio = randint(0,9)
        # limpiar, ir_Derecha e ir_izquierda cuestan 1
        #subir cuesta 3 y bajar cuesta 2
        if acción is "limpiar":
            self.desempeño-=1
            if aleatorio < 8:
                self.x[self.x[0]] = "limpio"
        elif acción is 'ir_Derecha':
            if aleatorio < 8:
                self.desempeño-=1
                self.x[0] += 1
            elif aleatorio == 8:
                self.desempeño-=1
            else:##elejimos una accion aleatoriamente
                ##vemos donde esta para escogfer su accion aleatoria
                if robot == 1:
                    self.desempeño-=1
                    accion_aleatoria= choice(['limpiar','nada'])
                    if accion_aleatoria == 'limpiar':
                        self.x[robot]='limpio'
                #-----------terminamos las acciones del cuarto 1
                if robot == 4 or robot == 7:
                    accion_aleatoria= choice(['limpiar','nada', 'bajar'])
                    if accion_aleatoria == 'limpiar':
                        self.desempeño-=1
                        self.x[robot]='limpio'
                    elif accion_aleatoria == 'bajar':
                        self.desempeño-=2
                        self.x[0] -= 3
                    else:
                        self.desempeño-=1
                #-------------terminamos las acciones de los cuartos 4 y 7
                if robot == 2 or robot == 5 or robot == 8:
                    accion_aleatoria= choice(['limpiar','nada', 'ir_Izquierda'])
                    if accion_aleatoria == 'limpiar':
                        self.desempeño-=1
                        self.x[robot]='limpio'
                    elif accion_aleatoria == 'ir_Izquierda':
                        self.desempeño-=1
                        self.x[0] -= 1
                    else:
                        self.desempeño-=1
                #---------terminamos las acciones de los cuartos 2, 5, 8
        #=====terminamos todas las acciones que podrian pasar por ir a la derecha
        elif acción is 'ir_Izquierda':
            if aleatorio < 8:
                self.desempeño-=1
                self.x[0] -= 1
            elif aleatorio == 8:
                self.desempeño-=1
            else:##elejimos una accion aleatoriamente
                ##vemos donde esta para escogfer su accion aleatoria
                if robot == 9:
                    self.desempeño-=1
                    accion_aleatoria= choice(['limpiar', 'nada'])
                    if accion_aleatoria == 'limpiar':
                        self.x[robot]='limpio'
                #-----------terminamos las acciones del cuarto 1
                if robot == 3 or robot == 6:
                    accion_aleatoria= choice(['limpiar', 'nada', 'subir'])
                    if accion_aleatoria == 'limpiar':
                        self.desempeño-=1
                        self.x[robot]='limpio'
                    elif accion_aleatoria == 'subir':
                        self.desempeño-=2
                        self.x[0] += 3
                    else:
                        self.desempeño-=1
                #-------------terminamos las acciones de los cuartos 4 y 7
                if robot == 2 or robot == 5 or robot == 8:
                    accion_aleatoria= choice(['limpiar', 'nada', 'ir_Derecha'])
                    if accion_aleatoria == 'limpiar':
                        self.desempeño-=1
                        self.x[robot]='limpio'
                    elif accion_aleatoria == 'ir_Derecha':
                        self.desempeño-=1
                        self.x[0] += 1
                    else:
                        self.desempeño-=1
                #---------terminamos las acciones de los cuartos 2, 5, 8
        #=====terminamos todas las acciones que podrian pasar por ir a la IZQUIERDA
        elif acción is "subir":
            if aleatorio < 8:
                self.desempeño-=2
                self.x[0] += 3
            elif aleatorio == 8:
                self.desempeño-=1
            else:##elejimos una accion aleatoriamente
                ##vemos donde esta para escogfer su accion aleatoria
                accion_aleatoria= choice(['limpiar', 'nada', 'ir_Izquierda'])
                if accion_aleatoria == 'limpiar':
                    self.desempeño-=1
                    self.x[robot]='limpio'
                elif accion_aleatoria == 'ir_Izquierda':
                    self.desempeño-=1
                    self.x[0] -= 1
                else:
                    self.desempeño-=1
        #=====terminamos todas las acciones que podrian pasar por SUBIR
        elif acción is "bajar":
            if aleatorio < 8:
                self.desempeño-=2
                self.x[0] -= 3
            elif aleatorio == 8:
                self.desempeño-=1
            else:##elejimos una accion aleatoriamente
                ##vemos donde esta para escogfer su accion aleatoria
                accion_aleatoria= choice(['limpiar', 'nada', 'ir_Derecha'])
                if accion_aleatoria == 'limpiar':
                    self.desempeño-=1
                    self.x[robot]='limpio'
                elif accion_aleatoria == 'ir_Derecha':
                    self.desempeño-=1
                    self.x[0] += 1
                else:
                    self.desempeño-=1
        #=====terminamos todas las acciones que podrian pasar por BAJAR

    def percepción(self):
        return self.x[0], self.x[self.x[0]]

#---------------------------------------------------------------------
#=======FIN ENTORNOS==================================================
#---------------------------------------------------------------------
        
class AgenteAleatorio(entornos_o.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales

    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, percepcion):
        return choice(self.acciones)

class AgenteReactivoNuevecuartos(entornos_o.Agente):
    """
    Un agente reactivo simple

    """
    def programa(self, percepción):
        robot, situación = percepción
        return ('limpiar' if situación == 'sucio' else
                'ir_A' if robot == 'B' else 'ir_B')


class AgenteReactivoModeloNueveCuartos(entornos_o.Agente):
    """
    Un agente reactivo basado en modelo

    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = [1, 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio']

    def programa(self, percepción):
        robot, situación = percepción

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[robot] = situación

        # Decide sobre el modelo interno
        a, b, c, d, e= self.modelo[1], self.modelo[2], self.modelo[3], self.modelo[4], self.modelo[5]
        f, g, h, i = self.modelo[6], self.modelo[7], self.modelo[8], self.modelo[9]
        
        if a == b == c == d == e == f == g == h == i == 'limpio':
            return'nada' #si todo esta limpio no hacemos nada
        elif situación == 'sucio':
            return 'limpiar' #si el cuarto en el que esta el robot esta sucio lo limpiamos
        elif robot == 1: 
            return 'ir_Derecha'#si esl robot esta en el primer cuarto, su unica opcion es ir a la derecha
        elif robot == 2:#limpiamos en orden el piso
            if a =='sucio':
                return 'ir_Izquierda'
            else:
                return 'ir_Derecha'
        elif robot == 3:
            if b == 'sucio':
                return 'ir_Izquierda'
            else:
                return 'subir'
        elif robot == 4:#cuarto de mas a la derecha del segundo piso
            if a == 'sucio':
                return 'bajar'
            else:
                return 'ir_Derecha'
        elif robot == 5:#cuarto de el centro del segundo piso
            if d == 'sucio':
                return 'ir_Izquierda'
            else:
                return 'ir_Derecha'
        elif robot == 6: #cuarto de la izq del segundo piso
            if e == 'sucio':
                return 'ir_Izquierda'
            else:
                return 'subir'
        elif robot == 7: #cuarto de la derecha del tercer piso
            if d == 'sucio':
                return 'bajar'
            else:
                return 'ir_Derecha'
        elif robot == 8:# cuarto del centro del tercer piso
            if g == 'sucio':
                return 'ir_Izquierda'
            else:
                return 'ir_Derecha'
        elif robot == 9: #cuaro de la izq del tercer piso, ya no se puede subir mas
            return 'ir_Izquierda'

class AgenteRacionalNueveCuartosCiego(entornos_o.Agente):
    """
    Un agente reactivo basado en modelo

    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = [1, 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio']

    def programa(self, percepción):
        robot, situación = percepción

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[robot] = situación

        
        if a == b == c == d == e == f == g == h == i == 'limpio':
            return'nada' #si todo esta limpio no hacemos nada
        elif situación == 'sucio':
            return 'limpiar' #si el cuarto en el que esta el robot esta sucio lo limpiamos
        elif robot == 1: 
            return 'ir_Derecha'#si esl robot esta en el primer cuarto, su unica opcion es ir a la derecha
        elif robot == 2:#limpiamos en orden el piso
            if a =='sucio':
                return 'ir_Izquierda'
            else:
                return 'ir_Derecha'
        elif robot == 3:
            if b == 'sucio':
                return 'ir_Izquierda'
            else:
                return 'subir'
        elif robot == 4:#cuarto de mas a la derecha del segundo piso
            if a == 'sucio':
                return 'bajar'
            else:
                return 'ir_Derecha'
        elif robot == 5:#cuarto de el centro del segundo piso
            if d == 'sucio':
                return 'ir_Izquierda'
            else:
                return 'ir_Derecha'
        elif robot == 6: #cuarto de la izq del segundo piso
            if e == 'sucio':
                return 'ir_Izquierda'
            else:
                return 'subir'
        elif robot == 7: #cuarto de la derecha del tercer piso
            if d == 'sucio':
                return 'bajar'
            else:
                return 'ir_Derecha'
        elif robot == 8:# cuarto del centro del tercer piso
            if g == 'sucio':
                return 'ir_Izquierda'
            else:
                return 'ir_Derecha'
        elif robot == 9: #cuaro de la izq del tercer piso, ya no se puede subir mas
            return 'ir_Izquierda'
        
def test():
    """
    Prueba del entorno y los agentes

    """
    """
    PRUEBAS DE NueveCuartos
    
    print("Prueba del entorno con un agente aleatorio")
    entornos_o.simulador(NueveCuartos(),
                         AgenteAleatorio(['ir_Derecha', 'ir_Izquierda', 'subir', 'bajar', 'limpiar', 'nada']),
                         200)

    #print("Prueba del entorno con un agente reactivo")
    #entornos_o.simulador(NueveCuartos(), AgenteReactivoNuevecuartos(), 100)

    print("Prueba del entorno con un agente reactivo con modelo")
    entornos_o.simulador(NueveCuartos(), AgenteReactivoModeloNueveCuartos(), 200)

    """
    #PRUEBAS DE NueveCuartosEstocasticos
    print("Prueba del entorno con un agente aleatorio")
    entornos_o.simulador(NueveCuartosEstocastico(),
                         AgenteAleatorio(['ir_Derecha', 'ir_Izquierda', 'subir', 'bajar', 'limpiar', 'nada']),
                         200)

    #print("Prueba del entorno con un agente reactivo")
    #entornos_o.simulador(NueveCuartos(), AgenteReactivoNuevecuartos(), 100)

    print("Prueba del entorno con un agente reactivo con modelo")
    entornos_o.simulador(NueveCuartosEstocastico(), AgenteReactivoModeloNueveCuartos(), 200)


if __name__ == "__main__":
    test()
