#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Tarea de desarrollo de entornos y agentes
==========================================

En esta tarea realiza las siguiente acciones:

1.- Desarrolla un entorno similar al de los dos cuartos (el cual se encuentra
    en el módulo doscuartos_o.py), pero con tres cuartos en el primer piso,
    y tres cuartos en el segundo piso.

    El entorno se llamará SeisCuartos

    Las acciones totales serán

    ["ir_Derecha", "ir_Izquierda", "Subir", "Bajar", "limpiar", "No_op"]

    La acción de "Subir" solo es legal en el piso de abajo (cualquier cuarto),
    y la acción de "Bajar" solo es legal en el piso de arriba.

    Las acciones de subir y bajar son mas costosas en término de energía
    que ir a la derecha y a la izquierda, por lo que la función de desempeño
    debe de ser de tener limpios todos los cuartos, con el menor numero de
    acciones posibles, y minimozando subir y bajar en relación a ir a los
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
__author__ = 'Temoc'

import entornos_o
from random import choice,random
import doscuartos_o

class SeisCuartos (entornos_o.Entorno):   #Aqui creamos la clase Seis Cuartos

    def __init__(self, x0=["A","sucio","sucio","sucio","sucio","sucio","sucio"]): #despues del def tienes que poner un espacio si no no servira,los dos puntitos se ponen porque asi se declara una funcion en python.
        #inicializamos las variables, los cuartos estan sucios y la posicion inicial es A
        """
        | D | E | F |    TODOS LOS CUARTOS INICIALMENTE ESTAN COCHINOS.
        | A | B | C |

        """
        self.x = x0[:] #AQUI CREAMOS EL ARREGLO ESTADO con los valores del arreglo x0 en el.
        self.desempeño = 0  #AQUI INICIALIZAMOS EL CONTADOR QUE MIDE EL DESEMPEÑO


    def acción_legal(self, accion,robot):  #PROCEDEREMOS A CREAR EL METODO QUE SIRVE PARA DEFINIR LAS ACCIONES LEGALES
        
        if robot == "A" and accion in ("Subir","ir_Derecha","No_op","limpiar"):
            return accion
        if robot == "B" and accion in ("Subir","ir_Izquierda","ir_Derecha","No_op","limpiar"):
            return accion
        if robot == "C" and accion in ("Subir","ir_Izquierda","No_op","limpiar"):
            return accion
        if robot == "D" and accion in ("Bajar","ir_Derecha","No_op","limpiar"):
            return accion
        if robot == "E" and accion in ("Bajar","ir_Izquierda","ir_Derecha","No_op","limpiar"):
            return accion
        if robot == "F" and accion in ("Bajar","ir_Izquierda","No_op","limpiar"):
            return accion
        return False
        
    def transición(self, acción): #AQUI CREAMOS EL METODO QUE SIRVE PARA DEFINIR LAS TRANSICIONES Y LO QUE HAY QUE HACER EN CONSECUENCIA 
        robot, A,B,C,D,E,F = self.x #en esta linea inicializamos los parametros cuartos y el robot limpiador 
        
        if not self.acción_legal(acción,robot): #en esta condicional se verifica si la accion no es legal mostrara error. 
            raise ValueError("Tu accion no es legal aguas!  ")
            
        if acción is not 'No_op'or A == 'sucio' or B == 'sucio' or C == 'sucio' or D == 'sucio' or E == 'sucio' or F == 'sucio' : #Si la accion es No_op osea no esta chambeando y A B C D E F estan sucios 
            self.desempeño -= 1  #aqui estoy castigando al robot por cochi y con la notacion -= quiere decir que estoy usando una especie de acumulador como el ++
                
        if acción is 'limpiar': 
            self.x[' ABCDEF'.find(self.x[0])] ='limpio' #en esta parte definimos las acciones por estado 
                
        elif acción is 'ir_Izquierda':
            if robot == 'C':
                self.x[0] = 'B'
                    
            elif robot == 'F':
                self.x[0] = 'E'
            
            elif robot == 'B':
                self.x[0] = 'A'
                
            elif robot == 'E':
                self.x[0] = 'D'
            
        elif acción is "ir_Derecha":
            if robot == 'A':
                self.x[0] = 'B'
                
            elif robot == 'D':
                self.x[0] = 'E'
                
            elif robot == 'B':
                self.x[0] = 'C'
            
            elif robot == 'E':
                self.x[0] = 'F'
        
        elif acción is 'Subir':
            self.desempeño -= 1
            
            if robot == 'A':
                self.x[0] = 'D'
            elif robot == 'B':
                self.x[0] = 'E'
            elif robot ==  'C':
                self.x[0] = 'F'
        
        elif acción is 'Bajar':
            self.desempeño -= 1
            if robot == 'D':
                self.x[0] = 'A'
            elif robot == 'E':
                self.x[0] = 'B'
            elif robot == 'F':
                self.x[0] = 'C'
                    
    def percepción(self):
        return self.x[0], self.x[' ABCDEF'.find(self.x[0])] #percepcion regresa una tupla que contiene ,la informacion donde se encuentra el robot y como se encuentran los cuartos (limpios o sucios)

class DosCuartosCiego(doscuartos_o.DosCuartos):
        
    def percepción(self):
        return self.x[0]

class DosCuartosEstocastico(doscuartos_o.DosCuartos):

    def transición(self, acción):
        if not self.acción_legal(acción):
            raise ValueError("La acción no es legal para este estado")

        robot, a, b = self.x
        if acción is not "No_op" or a is "sucio" or b is "sucio":
            self.desempeño -= 1
        if acción is "limpiar":
            if random() <= .80:
                self.x[" AB".find(self.x[0])] = "limpio"
        elif acción is "ir_A":
            self.x[0] = "A"
        elif acción is "ir_B":
            self.x[0] = "B"
# Requiere el modulo entornos_o.py
# Usa el modulo doscuartos_o.py para reutilizar código
# Agrega los modulos que requieras de python

class AgenteAleatorio(entornos_o.Agente):
    #el agente aleatorio es aquel que solo regresa una accion al azar, entre el conjunto de acciones legales
    """
        RECORDANDO EL DIAGRAMA INICIAL PARA ILUSTRAR MEJOR LO QUE PUEDEN HACER
        | D | E | F |    
        | A | B | C |
        
        acciones posibles
        'ir_Izquierda'
        'ir_Derecha'
        'Bajar'
        'Subir'  
        'limpiar'
        'No_op'
    """
    def __init__(self, acciones):
        self.acciones = acciones
    
    def programa(self, percepcion):  #aqui definimos lo que se pueden hacer iniciando en cierto cuarto. 
        robot = percepcion[0]
        
        if robot == 'A' :
            self.acciones= ('ir_Derecha','Subir','limpiar','No_op')
        elif robot == 'B' :
            self.acciones= ('ir_Derecha','ir_Izquierda','Subir','limpiar','No_op')
        elif robot == 'C' : 
            self.acciones= ('ir_Izquierda','Subir','limpiar','No_op')
        elif robot == 'D' :
            self.acciones= ('ir_Derecha','Bajar','limpiar','No_op')
        elif robot == 'E' : 
            self.acciones= ('ir_Izquierda','ir_Derecha','Bajar','limpiar','No_op')
        elif robot == 'F' : 
            self.acciones= ('ir_Izquierda','Bajar','limpiar','No_op')
        return choice(self.acciones)
    
class AgenteReactivoModeloSeisCuartos(entornos_o.Agente):
    #UN AGENTE REACTIVO BASADO EN MODELO
    
    def __init__(self): # metodo que Inicializa el modelo interno en el peor de los casos
        
        #INCIANDO EN A con todos los demas cuartos sucios :C
        self.modelo = ["A","sucio","sucio","sucio","sucio","sucio","sucio"]
        
    def programa(self, percepcion):
        robot, situacion = percepcion 
        
        #Esta parte Actualiza el arreglo modelo interno
        self.modelo[0] = robot 
        self.modelo[' ABCDEF'.find(robot)]= situacion
        
        #Esta parte asigna el valor al modelo llenando estados
        a=self.modelo[1]
        b=self.modelo[2]
        c=self.modelo[3]
        d=self.modelo[4]
        e=self.modelo[5]
        f=self.modelo[6]

        if a == 'limpio' and b == 'limpio' and c == 'limpio' and d == 'limpio' and e == 'limpio' and f == 'limpio' :
            return 'No_op'
        # :C pls dont kill me profe. me imagine que podia ser a==b==c==d==e==f == 'limpio' pero se ve horrible.
            """
            RECORDANDO EL DIAGRAMA INICIAL PARA ILUSTRAR MEJOR LO QUE PUEDEN HACER
            | D | E | F |    
            | A | B | C |
        
            acciones legales y situacionales
            'ir_Izquierda'
            'ir_Derecha'
            'Bajar'
            'Subir'  
            'limpiar'
            'sucio'
            'limpiar'
            """
        else:
            if situacion == 'sucio':
                return 'limpiar'
            else:
                if robot == 'A':
                    return('ir_Derecha' if 'sucio' in [b,c] else 'Subir')
                    
                if robot == 'B': 
                    return('ir_Derecha' if c == 'sucio' else 'ir_Izquierda' if a == 'sucio' else 'Subir')
                
                if robot == 'C':
                    return('ir_Izquierda' if 'sucio' in [a,b] else 'Subir' )
                    
                if robot == 'D' :
                    return('ir_Derecha' if 'sucio' in 'sucio' else 'ir_Izquierda' if d == 'sucio' else 'Bajar')
                
                if robot == 'E' : 
                    return('ir_Derecha' if f == 'sucio' else 'ir_Izquierda' if d== 'sucio' else 'Bajar')
                
                if robot == 'F' : 
                    return ('ir_Izquierda' if 'sucio' in [d,e] else 'Bajar')
                
class AgenteRacionalDosCuartos(entornos_o.Agente):
    
    def __init__(self):
        self.contador = 0 
        
        
    def programa(self,percepcion):
        robot = percepcion
        self.contador += 1
        
        if self.contador == 1 or self.contador == 3:
            return 'limpiar'
        
        if self.contador == 2:
            return('ir_A' if robot == 'B' else 'ir_B')
        else:
            return 'No_op'
        
            
print("Prueba del entorno con un agente aleatorio Seis Cuartos")
entornos_o.simulador(SeisCuartos(),
                     AgenteAleatorio(['ir_Izquierda', 'ir_Derecha','subir','bajar','limpiar', 'No_op']),
                         100)
print("Prueba del entorno con un agente Reactivo Seis Cuartos")
entornos_o.simulador(SeisCuartos(),
                     AgenteReactivoModeloSeisCuartos(),
                     100)
"""
    Para el agente aleatorio tiene un desempeño peor que el modelo
    Para el modelo de seis cuartos el agente Reactivo basado en modelo lo limpia todo
    para el paso 12 con un desempeño de -12
"""

print("Prueba del entorno con un agente racional Modelo Ciego")
entornos_o.simulador(DosCuartosCiego(), AgenteRacionalDosCuartos(),50)

print("Prueba del entorno con un agente aleatorio Modelo Ciego")
entornos_o.simulador(DosCuartosCiego(), doscuartos_o.AgenteAleatorio(['ir_A', 'ir_B', 'limpiar', 'No_op']),50)
"""
    Para el modelo dos cuartos Ciego siempre para el paso 4 ya tenia todo limpia con
    un desempeño de -3
    y con el aleatorio por el paso 20 con un desempeño de -19 fue la menor de las
    pasadas hechas
"""

print("Prueba del entorno con un agente racional Modelo Estocastico")
entornos_o.simulador(DosCuartosEstocastico(),doscuartos_o.AgenteReactivoModeloDosCuartos(),
                     50)

print("Prueba del entorno con un agente aleatorio Modelo Estocastico")
entornos_o.simulador(DosCuartosEstocastico(), doscuartos_o.AgenteAleatorio(['ir_A', 'ir_B', 'limpiar', 'No_op']),
                     50)
"""
    Con el Agente racional obtuve un minimo de -3 en desempeño y un maximo de -6 en las pasadas obtenidas
    y el aleatorio se limpio todo para la pasada 16 con un desempeño de -16
"""
            
            

            
        
             
            
            
