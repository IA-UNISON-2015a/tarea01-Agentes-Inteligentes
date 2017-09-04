
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Tarea de desarrollo de entornos y agentes
==========================================

En esta tarea realiza las siguiente acciones:

1.- Desarrolla un entorno similar al de los dos cuartos (el cuál se encuentra
    en el módulo doscuartos_o.py), pero con tres cuartos en el primer piso,
    y tres cuartos en el segundo piso.

    El entorno se llamará SeisCuartos

    Las acciones totales serán

    ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]

    La acción de "subir" solo es legal en el piso de abajo (cualquier cuarto),
    y la acción de "bajar" solo es legal en el piso de arriba.

    Las acciones de subir y bajar son mas costosas en término de energía
    que ir a la derecha y a la izquierda, por lo que la función de desempeño
    debe de ser de tener limpios todos los cuartos, con el menor numero de
    acciones posibles, y minimizando subir y bajar en relación a ir a los
    lados.

2.- Diseña un Agente reactivo basado en modelo para este entorno y compara
    su desempeño con un agente aleatorio despues de 100 pasos de simulación.

3.- Al ejemplo original de los dos cuartos, modificalo de manera que el agente
    solo pueda saber en que cuarto se encuentra pero no sabe si está limpio
    o sucio.

    A este nuevo entorno llamalo DosCuartosCiego

    Diseña un agente racional para este problema, pruebalo y comparalo
    con el agente aleatorio.

4.- Reconsidera el problema original de los dos cuartos, pero ahora modificalo
    para que cuando el agente decida aspirar, el 80% de las veces limpie pero
    el 20% (aleatorio) deje sucio el cuarto. Diseña un agente racional
    para este problema, pruebalo y comparalo con el agente aleatorio.

    A este entorno llamalo DosCuartosEstocástico

Todos los incisos tienen un valor de 25 puntos sobre la calificación de
la tarea.

"""
__author__ = 'Jorge Adrián Olmos Morales'



import random
import entornos_o
import doscuartos_o

""" **************************************************************************** """ 
""" **************************************************************************** """ 
""" **************************************************************************** """ 
class SeisCuartos(entornos_o.Entorno):
    
    def __init__(self, x0=["A", "sucio", "sucio","sucio", "sucio", "sucio", "sucio"]):
        self.x = x0[:]
        self.desempeño = 0
        
    def acción_legal(self, acción):
        return acción in ("ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada")
    
    def transición(self, acción):
        if not self.acción_legal(acción):
            raise ValueError("La acción no es legal para este estado")
        if acción is "nada" and "sucio" in self.x:
            self.desempeño -= 1
        if acción is "limpiar":
            self.x[" ABCDEF".find(self.x[0])] = "limpio"
            self.desempeño -= 1
        elif acción is "ir_Derecha":
            if(self.x[0] == "A" or self.x[0] == "D"):
                self.desempeño -= 1
            elif self.x[0] == "B":
                self.x[0] = "A"
                self.desempeño -= 1
            elif self.x[0] == "C":
                self.x[0] = "B"
                self.desempeño -= 1
            elif self.x[0] == "E":
                self.x[0] = "D"
                self.desempeño -= 1
            elif self.x[0] == "F":
                self.x[0] = "E"
                self.desempeño -= 1
        elif acción is "ir_Izquierda":
            if(self.x[0] == "C" or self.x[0] == "F"):
                self.desempeño -= 1
            elif self.x[0] == "A":
                self.x[0] = "B"
                self.desempeño -= 1
            elif self.x[0] == "B":
                self.x[0] = "C"
                self.desempeño -= 1
            elif self.x[0] == "D":
                self.x[0] = "E"
                self.desempeño -= 1
            elif self.x[0] == "E":
                self.x[0] = "F"
                self.desempeño -= 1
        elif acción is "subir":
            if(self.x[0] == "A" or self.x[0] == "B" or self.x[0] == "C"):
                self.desempeño -= 1
            elif self.x[0] == "D":
                self.x[0] = "A"
                self.desempeño -= 2
            elif self.x[0] == "E":
                self.x[0] = "B"
                self.desempeño -= 2
            elif self.x[0] == "F":
                self.x[0] = "C"
                self.desempeño -= 2
        elif acción is "bajar":
            if(self.x[0] == "D" or self.x[0] == "E" or self.x[0] == "F"):
                self.desempeño -= 1
            elif self.x[0] == "A":
                self.x[0] = "D"
                self.desempeño -= 2
            elif self.x[0] == "B":
                self.x[0] = "E"
                self.desempeño -= 2
            elif self.x[0] == "C":
                self.x[0] = "F"
                self.desempeño -= 2
    
    def percepción(self):
        return self.x[0], self.x[" ABCDEF".find(self.x[0])]

""" **************************************************************************** """ 
    
class DosCuartosCiego(entornos_o.Agente):

    def __init__(self, x0=["A", "sucio", "sucio"]):
        """
        Por default inicialmente el robot está en A y los dos cuartos
        están sucios
        """
        self.x = x0[:]
        self.desempeño = 0
        
    def acción_legal(self, acción):
        return acción in ("ir_A", "ir_B", "limpiar", "nada")
    
    def transición(self, acción):
        if not self.acción_legal(acción):
            raise ValueError("La acción no es legal para este estado")

        if(acción =="nada" and ("sucio" in self.x)):
            self.desempeño -= 1
        if acción is "limpiar":
            self.x[" AB".find(self.x[0])] = "limpio"
            self.desempeño -= 1
        elif acción is "ir_A":
            self.x[0] = "A"
            self.desempeño -= 1
        elif acción is "ir_B":
            self.x[0] = "B"
            self.desempeño -= 1

    def percepción(self):
        return self.x[0]
    
""" **************************************************************************** """    

class DosCuartosEstocastico(entornos_o.Agente):

    def __init__(self, x0=["A", "sucio", "sucio"]):
        """
        Por default inicialmente el robot está en A y los dos cuartos
        están sucios
        """
        self.x = x0[:]
        self.desempeño = 0
        
    def acción_legal(self, acción):
        return acción in ("ir_A", "ir_B", "limpiar", "nada")
    
    def transición(self, acción):
        if not self.acción_legal(acción):
            raise ValueError("La acción no es legal para este estado")

        if(acción =="nada" and ("sucio" in self.x)):
            self.desempeño -= 1
        if acción is "limpiar":
            self.x[" AB".find(self.x[0])] = "limpio"
            self.desempeño -= 1
        elif acción is "ir_A":
            self.x[0] = "A"
            self.desempeño -= 1
        elif acción is "ir_B":
            self.x[0] = "B"
            self.desempeño -= 1

    def percepción(self):
        return self.x[0]  
    
""" **************************************************************************** """

class AgenteReactivoModeloSeisCuartos(entornos_o.Agente):
    
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos
        """
        self.modelo = ["A", "sucio", "sucio","sucio", "sucio", "sucio", "sucio"]
    
    def respuesta(self, percepcion):
        posicion_robot, situación = percepcion
        
        # Actualiza el modelo interno
        self.modelo[0] = posicion_robot
        self.modelo[' ABCDEF'.find(posicion_robot)] = situación

        accion_respuesta = "nada"
        if(not("sucio" in self.modelo)):
            accion_respuesta = "nada"
        elif(situación == "sucio"):
            accion_respuesta = "limpiar"
        elif posicion_robot == "A" or posicion_robot == "B":
            accion_respuesta = "ir_Izquierda"
        elif posicion_robot == "C":
            accion_respuesta = "bajar"
        elif posicion_robot == "E" or posicion_robot == "F":
            accion_respuesta = "ir_Derecha"
        elif posicion_robot == "D":
            accion_respuesta = "subir"
            
        return accion_respuesta

""" **************************************************************************** """
    
class AgenteReactivoCiegoModeloDosCuartos(entornos_o.Agente):
    
    def __init__(self):
        self.paso = 0
    def respuesta(self, percepcion):
        accion_respuesta = "nada"
        posicion_robot = percepcion
        if(self.paso >2):
            accion_respuesta = "nada" 
        elif(self.paso == 0 or self.paso == 2):
            accion_respuesta = "limpiar"
            self.paso += 1
        elif(self.paso == 1):
            if(posicion_robot == "A"):
                accion_respuesta = "ir_B"
            else:
                accion_respuesta = "ir_A"
            self.paso += 1
        return accion_respuesta
    
""" **************************************************************************** """ 

class AgenteReactivoModeloDosCuartosProbabilidadFallo(entornos_o.Agente):

    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = ["A", "sucio", "sucio"]

    def respuesta(self, percepción):
        posicion_robot, situación = percepción

        # Actualiza el modelo interno
        self.modelo[0] = posicion_robot
        self.modelo[' AB'.find(posicion_robot)] = situación
        accion_respuesta = "nada"
        if(not("sucio" in self.modelo)):
            accion_respuesta = "nada"
        elif(situación == "limpio"):
            if(posicion_robot == "A"):
                accion_respuesta = "ir_B"
            else:
                accion_respuesta = "ir_A"
        elif(situación == "sucio"):
            #Probabilidad de fallar
            probabilidad_fallo = round(random.uniform(0,1),2)
            if(probabilidad_fallo > .20):
                accion_respuesta = "nada"
            else:
                accion_respuesta = "limpiar"
                
        return accion_respuesta
    
    
""" **************************************************************************** """ 
""" **************************************************************************** """ 
""" **************************************************************************** """ 
  
def test():
    """
    Prueba del entorno y los agentes
    """
    print("Prueba del entorno con un agente aleatorio (entorno Seis Cuartos)")
    print("Representación del Entorno Seis Cuartos:\n\n |A|B|C| \n |D|E|F|")
    entornos_o.simulador( SeisCuartos(), doscuartos_o.AgenteAleatorio(["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]), 100 )
    print("Prueba del entorno con un agente reactivo (entorno Seis Cuartos)")
    print("Representación del Entorno Seis Cuartos:\n\n |A|B|C| \n |D|E|F|")
    entornos_o.simulador( SeisCuartos(), AgenteReactivoModeloSeisCuartos(), 100 )
    print("Prueba del entorno dos cuartos con un agente reactivo ciego")
    entornos_o.simulador( DosCuartosCiego(), AgenteReactivoCiegoModeloDosCuartos(), 100 )
    print("Prueba del entorno con agente reactivo con probabilidad de fallo") 
    entornos_o.simulador( doscuartos_o.DosCuartos(), AgenteReactivoModeloDosCuartosProbabilidadFallo(), 100)   
    
    
if __name__ == "__main__":
    test()
    
           
# Requiere el modulo entornos_o.py
# Usa el modulo doscuartos_o.py para reutilizar código
# Agrega los modulos que requieras de python
