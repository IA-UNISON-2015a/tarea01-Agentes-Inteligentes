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
import random

class NueveCuartos(entornos_f.Entorno):
    def accion_legal(self,_,accion):                       
        
        return accion in ("ir_Derecha","ir_Izquierda","Subir","Bajar", "Limpiar", "Nada")
    
    def transicion(self, estado, accion):
        robot,a,b,c,d,e,f,g,h,i = estado
        
        if accion in ["ir_Derecha", "ir_Izquierda"]:
            c_local = 1
        elif accion in ["Limpiar","Nada"]:
            c_local = 0
        else:
            c_local = 2
        
        return ((estado, c_local) if a == "Nada" else
                (("B",a,b,c,d,e,f,g,h,i),c_local) if robot == 'C' and accion == 'ir_Derecha' or robot == 'A' and accion ==  'ir_Izquierda' else
                (("E",a,b,c,d,e,f,g,h,i),c_local) if robot == 'D'  and accion == 'ir_Izquierda' or robot == 'F' and accion == 'ir_Derecha' else
                (("H",a,b,c,d,e,f,g,h,i),c_local) if robot =='G' and accion ==  'ir_Izquierda' or robot == 'I' and accion == 'ir_Derecha'else
                (("C",a,b,c,d,e,f,g,h,i),c_local) if robot == 'F' and accion == 'Bajar' or robot  == 'B' and accion == 'ir_Izquierda'else
                (("F",a,b,c,d,e,f,g,h,i),c_local) if robot == 'I' and accion == 'Bajar' or robot == 'E' and accion ==  'ir_Izquierda'else
                (("D",a,b,c,d,e,f,g,h,i),c_local) if robot == 'A' and accion == 'Subir' or robot == 'E' and accion == 'ir_Derecha'else
                (("G",a,b,c,d,e,f,g,h,i),c_local) if robot == 'D' and accion == 'Subir' or robot == 'H' and accion == 'ir_Derecha'else
                (("I",a,b,c,d,e,f,g,h,i),c_local) if robot == 'H' and accion == 'ir_Izquierda' else
                (("A",a,b,c,d,e,f,g,h,i),c_local) if robot == 'B' and accion == 'ir_Derecha'else
                ((robot,"limpio",b,c,d,e,f,g,h,i),c_local)if robot == "A" else
                ((robot,a,"limpio",c,d,e,f,g,h,i),c_local)if robot == "B" else
                ((robot,a,b,"limpio",d,e,f,g,h,i),c_local)if robot == "C" else
                ((robot,a,b,c,"limpio",e,f,g,h,i),c_local)if robot == "D" else
                ((robot,a,b,c,d,"limpio",f,g,h,i),c_local)if robot == "E" else
                ((robot,a,b,c,d,e,"limpio",g,h,i),c_local)if robot == "F" else
                ((robot,a,b,c,d,e,f,"limpio",h,i),c_local)if robot == "G" else
                ((robot,a,b,c,d,e,f,g,"limpio",i),c_local)if robot == "H" else
                ((robot,a,b,c,d,e,f,g,h,"limpio"),c_local))
                        
        
                
    def percepcion(self, estado):
        return estado[0], estado[" ABCDEFGHI".find(estado[0])] 
    
class NueveCuartosCiego(NueveCuartos): 

    def accion_legal(self, _, accion):
        return super().accion_legal(_, accion)
    
    def transicion(self, estado, accion):
       return super().transicion(estado,accion)
    
    def percepcion(self, estado):
        return super().percepcion(estado)    

class NueveCuartosEstocastico(NueveCuartos):

    def accion_legal(self, estado, accion):
        return super().accion_legal(estado, accion)

    def transicion(self, estado, accion):       
        robot,a,b,c,d,e,f,g,h,i = estado       
        aleatorio = random.random()
        if accion in ["ir_Derecha", "ir_Izquierda"]:
            c_local = 1
        elif accion in ["Limpiar","Nada"]:
            c_local = 0
        else:
            c_local = 2          

            if aleatorio < 0.8:
                return ((estado, c_local) if a == "Nada" else
                (("B",a,b,c,d,e,f,g,h,i),c_local) if robot == 'C' and accion == 'ir_Derecha' or robot == 'A' and accion ==  'ir_Izquierda' else
                (("E",a,b,c,d,e,f,g,h,i),c_local) if robot == 'D' and accion == 'ir_Izquierda' or robot == 'F' and accion == 'ir_Derecha' else
                (("H",a,b,c,d,e,f,g,h,i),c_local) if robot == 'G' and accion ==  'ir_Izquierda' or robot == 'I' and accion == 'ir_Derecha'else
                (("C",a,b,c,d,e,f,g,h,i),c_local) if robot == 'F' and accion == 'Bajar' or robot  == 'B' and accion == 'ir_Izquierda'else
                (("F",a,b,c,d,e,f,g,h,i),c_local) if robot == 'I' and accion == 'Bajar' or robot == 'E' and accion ==  'ir_Izquierda'else
                (("D",a,b,c,d,e,f,g,h,i),c_local) if robot == 'A' and accion == 'Subir' or robot == 'E' and accion == 'ir_Derecha'else
                (("G",a,b,c,d,e,f,g,h,i),c_local) if robot == 'D' and accion == 'Subir' or robot == 'H' and accion == 'ir_Derecha'else
                (("I",a,b,c,d,e,f,g,h,i),c_local) if robot == 'H' and accion == 'ir_Izquierda' else
                (("A",a,b,c,d,e,f,g,h,i),c_local) if robot == 'B' and accion == 'ir_Derecha'else
                ((robot,"limpio",b,c,d,e,f,g,h,i),c_local)if robot == "A"  and accion == 'Limpiar' else
                ((robot,a,"limpio",c,d,e,f,g,h,i),c_local)if robot == "B"  and accion == 'Limpiar' else
                ((robot,a,b,"limpio",d,e,f,g,h,i),c_local)if robot == "C"  and accion == 'Limpiar' else
                ((robot,a,b,c,"limpio",e,f,g,h,i),c_local)if robot == "D"  and accion == 'Limpiar' else
                ((robot,a,b,c,d,"limpio",f,g,h,i),c_local)if robot == "E"  and accion == 'Limpiar' else
                ((robot,a,b,c,d,e,"limpio",g,h,i),c_local)if robot == "F"  and accion == 'Limpiar' else
                ((robot,a,b,c,d,e,f,"limpio",h,i),c_local)if robot == "G"  and accion == 'Limpiar' else
                ((robot,a,b,c,d,e,f,g,"limpio",i),c_local)if robot == "H"  and accion == 'Limpiar' else
                ((robot,a,b,c,d,e,f,g,h,"limpio"),c_local) and accion == 'Limpiar')
            else: 
                return 'Nada'
        
        
    def percepcion(self, estado):
        return super().percepcion(estado)
    

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
        #Cambiar las acciones que regresa, aqui esta el error del bucle
        a, b, c, d, e, f, g, h, i = (self.modelo[1], self.modelo[2], self.modelo[3],
                                 self.modelo[4], self.modelo[5], self.modelo[6],
                                 self.modelo[7], self.modelo[8], self.modelo[9]) 
      
                                                                                                                                                            
        if a == b == c == d == e == f == g == h == i == 'limpio':
            return 'Nada' 
        if situación == 'sucio': 
            return 'Limpiar'  
        if robot in 'A' and (b == c != 'limpio') or robot in 'B' and (c == 'sucio') or robot in 'D' and (e == f != 'limpio') or robot in 'E' and (f == 'sucio') or robot in 'G' and (h == i != 'limpio') or robot in 'H' and (i == 'sucio'):
         return 'ir_Izquierda'  
        elif robot in 'A' and (b == c != 'sucio') and (d == e == f != 'limpio') or robot in 'D' and (e == f != 'sucio') and (g == h == i != 'limpio'):
            return 'Subir'        
        if robot in 'C' and (a == b != 'limpio') or (a == b == 'limpio') or robot in 'B' and (a == 'sucio') or robot in 'F' and (e == d != 'limpio') or robot in 'E' and (d == 'sucio') or robot in 'I' and (h == g != 'limpio') or robot in 'H' and (g == 'sucio'): 
            return 'ir_Derecha'
        if robot in 'I' and (h == g != 'sucio') and (d == e == f != 'limpio') or robot in 'F' and (e == d != 'sucio') and (a == b == c != 'limpio'):
            return 'Bajar'
        
class AgenteEstocastico(entornos_f.Agente):
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = ['A', 'sucio', 'sucio','sucio','sucio','sucio','sucio','sucio','sucio','sucio']

    def programa(self, percepción):
        robot, situación = percepción     
        aleatorio = random.random()
        acciones = ['ir_Derecha','ir_Izquierda','Subir','Bajar','Limpiar','Nada']
        accion = random.choice(acciones)
        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[' ABCDEFGHI'.find(robot)] = situación
        
        
        # Decide sobre el modelo interno
        #Cambiar las acciones que regresa, aqui esta el error del bucle
        a, b, c, d, e, f, g, h, i = (self.modelo[1], self.modelo[2], self.modelo[3],
                                 self.modelo[4], self.modelo[5], self.modelo[6],
                                 self.modelo[7], self.modelo[8], self.modelo[9]) 
      
                                                                                                                                                            
        if a == b == c == d == e == f == g == h == i == 'limpio':
            return 'Nada' 
        if aleatorio < 0.8:
            if situación == 'sucio':
                return 'Limpiar'       
            if robot in 'A' and (b == c != 'limpio') or robot in 'B' and (c == 'sucio') or robot in 'D' and (e == f != 'limpio') or robot in 'E' and (f == 'sucio') or robot in 'G' and (h == i != 'limpio') or robot in 'H' and (i == 'sucio'):
                return 'ir_Izquierda'      
            elif robot in 'A' and (b == c != 'sucio') and (d == e == f != 'limpio') or robot in 'D' and (e == f != 'sucio') and (g == h == i != 'limpio'):
                 return 'Subir'        
            if robot in 'C' and (a == b != 'limpio') or (a == b == 'limpio') or robot in 'B' and (a == 'sucio') or robot in 'F' and (e == d != 'limpio') or robot in 'E' and (d == 'sucio') or robot in 'I' and (h == g != 'limpio') or robot in 'H' and (g == 'sucio'): 
                return 'ir_Derecha'
            if robot in 'I' and (h == g != 'sucio') and (d == e == f != 'limpio') or robot in 'F' and (e == d != 'sucio') and (a == b == c != 'limpio'):
                return 'Bajar'
        elif aleatorio <0.9:
            return 'Nada'
        else:
            return accion    
class AgenteReactivo(entornos_f.Agente):
        
    def __init__(self):
        self.modelo = ['A','?','?','?','?','?','?','?','?','?'] 
    
    def programa(self, persepcion):
        robot,situación = persepcion         
        
        self.modelo[0] = robot
        self.modelo[' ABCDEFGHI'.find(robot)] = situación

        a,b,c,d,e,f,g,h,i = (self.modelo[1], self.modelo[2], self.modelo[3],
                             self.modelo[4], self.modelo[5], self.modelo[6],
                             self.modelo[7], self.modelo[8], self.modelo[9])
        
        if a == b == c == d == e == f == g == h == i == 'limpio':
            return 'Nada'
        if situación == '?': 
            return 'Limpiar'  
        if robot in 'A' and (b == c != 'limpio') or robot in 'B' and (c == '?') or robot in 'D' and (e == f != 'limpio') or robot in 'E' and (f == '?') or robot in 'G' and (h == i != 'limpio') or robot in 'H' and (i == '?'):
         return 'ir_Izquierda'  
        elif robot in 'A' and (b == c != '?') and (d == e == f != 'limpio') or robot in 'D' and (e == f != '?') and (g == h == i != 'limpio'):
            return 'Subir'        
        if robot in 'C' and (a == b != 'limpio') or (a == b == 'limpio') or robot in 'B' and (a == '?') or robot in 'F' and (e == d != 'limpio') or robot in 'E' and (d == '?') or robot in 'I' and (h == g != 'limpio') or robot in 'H' and (g == '?'): 
            return 'ir_Derecha'
        if robot in 'I' and (h == g != '?') and (d == e == f != 'limpio') or robot in 'F' and (e == d != '?') and (a == b == c != 'limpio'):
            return 'Bajar'


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
            100
        ),
        ["A", "sucio", "sucio","sucio","sucio","sucio","sucio","sucio","sucio","sucio"]
    )

def prueba_agente_ciego(agente): 
        entornos_f.imprime_simulacion(
        entornos_f.simulador(
            NueveCuartos(),
            agente,
            ["A","?","?","?","?","?","?","?","?","?"],
            100
        ),
        ["A","?","?","?","?","?","?","?","?","?",]
    )
  
def test():
    """
    Prueba del entorno y los agentes

    """   

    print("Prueba del entorno con un agente aleatorio")
    prueba_agente(AgenteAleatorio(['ir_Izquierda','ir_Derecha','Bajar','Subir','Limpiar','Nada']))
    
    print("Prueba del entorno con un agente reactivo con modelo")
    prueba_agente(AgenteReactivoModeloNueveCuartos())

    print("---------------------------------------ENTRONO CIEGO----------------------------------------------")

    print("Prueba del entorno ciego con un agente Aleatorio")
    prueba_agente_ciego(AgenteAleatorio(['ir_Izquierda','ir_Derecha','Bajar','Subir','Limpiar','Nada']))

    print("Prueba del entorno ciego con un agente racional")
    prueba_agente_ciego(AgenteReactivo())

    print("------------------------------------ENTORNO ESTOCASTICO--------------------------------------------")

    print("Prueba del entrono estocastico con un agente aleatorio")
    prueba_agente(AgenteAleatorio(['ir_Izquierda','ir_Derecha','Bajar','Subir','Limpiar','Nada']))

    print("Prueba del entorno estocastico con un agente racional")
    prueba_agente(AgenteEstocastico())
   
    

if __name__ == "__main__":
    test()

# Requiere el modulo entornos_f.py o entornos_o.py
# Usa el modulo doscuartos_f.py para reutilizar código
# Agrega los modulos que requieras de python

