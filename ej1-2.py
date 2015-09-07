es (162 sloc)  8.22 kB
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import entornos
from random import choice


class DosCuartos(entornos.Entorno):
    """
    -------------------------
    Ejercicios 1 y 2
    -------------------------
    Problema de 6 cuartos (2 pisos, 3 cuartos en cada uno)
    Los cuartos se encuentran distribuidos de la siguiente forma:

    |D|E|F|
    |A|B|C|

    Los cuartos A, B y C en el piso de abajo, D, E y F en el piso de arriba.
    
    El costo por limpiar, cambiar de cuarto en el mismo piso o no hacer nada cuando
    falten cuartos de limpiar, es de 1.
    El costo por cambio de piso es de 2.
    No realizar una acción cuando se terminó de limpiar todos los pisos tiene costo 0.


    -------------------------
    Agente reactivo
    -------------------------
    El agente reactivo recorrerá los cuartos en el orden: A -> B -> C -> F -> E -> D -> A
    Si el cuarto en el que se encuentra está sucio, lo limpia. Si está limpio, cambia de cuarto
    según la secuencia dada.
    
    (no se pedía en la tarea, pero fue incluído por ser parecido al
    basado en modelo)
    
    -------------------------
    Agente reactivo basado en modelo
    -------------------------
    El agente reactivo basado en modelo limpiará los cuartos del piso en el que se encuentra antes
    de pasar al otro piso, minimizando el costo por cambio de piso.

    
    -------------------------
    Notas
    -------------------------
    Comparando el agente reactivo basado en modelo con el agente aleatorio,
    el reactivo basado en modelo es el más racional, pues llega un punto
    en el que deja de consumir energía.
    
    Como dato curioso, el agente reactivo es más costoso que el agente aleatorio.
    
    """
    def transicion(self, estado, accion):
        if not self.accion_legal(estado, accion):
            raise ValueError("La accion no es legal para este estado")

        robot, A, B, C, D, E, F = estado

        if estado[0] == 'A':
            return (('A', A, B, C, D, E, F) if accion == 'noOp' else
                    ('A', 'limpio', B, C, D, E, F) if accion == 'limpiar' else
                    ('B', A, B, C, D, E, F) if accion == 'irDerecha' else
                    ('D', A, B, C, D, E, F))

        if estado[0] == 'B':
            return (('B', A, B, C, D, E, F) if accion == 'noOp' else
                    ('B', A, 'limpio', C, D, E, F) if accion == 'limpiar' else
                    ('C', A, B, C, D, E, F) if accion == 'irDerecha' else
                    ('A', A, B, C, D, E, F) if accion == 'irIzquierda' else
                    ('E', A, B, C, D, E, F))

        if (estado[0]=='C'):
            return (('C', A, B, C, D, E, F) if accion == 'noOp' else
                    ('C', A, B, 'limpio', D, E, F) if accion == 'limpiar' else
                    ('B', A, B, C, D, E, F) if accion == 'irIzquierda' else
                    ('F', A, B, C, D, E, F))

        if (estado[0]=='D'):
            return (('D', A, B, C, D, E, F) if accion == 'noOp' else
                    ('D', A, B, C, 'limpio', E, F) if accion == 'limpiar' else
                    ('E', A, B, C, D, E, F) if accion == 'irDerecha' else
                    ('A', A, B, C, D, E, F))

        if (estado[0]=='E'):
            return (('E', A, B, C, D, E, F) if accion == 'noOp' else
                    ('E', A, B, C, D, 'limpio', F) if accion == 'limpiar' else
                    ('F', A, B, C, D, E, F) if accion == 'irDerecha' else
                    ('D', A, B, C, D, E, F) if accion == 'irIzquierda' else
                    ('B', A, B, C, D, E, F))

        if (estado[0]=='F'):
            return (('F', A, B, C, D, E, F) if accion == 'noOp' else
                    ('F', A, B, C, D, E, 'limpio') if accion == 'limpiar' else
                    ('E', A, B, C, D, E, F) if accion == 'irIzquierda' else
                    ('C', A, B, C, D, E, F))


                    
    def sensores(self, estado):
        robot, A, B, C, D, E, F = estado
        return robot, (A if robot == 'A' else
                       B if robot == 'B' else
                       C if robot == 'C' else
                       D if robot == 'D' else
                       E if robot == 'E' else
                       F)
        

    def accion_legal(self, estado, accion):
        if estado[0] == 'A':
            return accion in ('irDerecha', 'subir', 'limpiar', 'noOp')
        elif estado[0] == 'B':
            return accion in ('irDerecha', 'irIzquierda', 'subir', 'limpiar', 'noOp')
        elif estado[0] == 'C':
            return accion in ('irIzquierda', 'subir', 'limpiar', 'noOp')
        elif estado[0] == 'D':
            return accion in ('irDerecha', 'bajar', 'limpiar', 'noOp')
        elif estado[0] == 'E':
            return accion in ('irDerecha', 'irIzquierda', 'bajar', 'limpiar', 'noOp')
        else:
            return accion in ('irIzquierda', 'bajar', 'limpiar', 'noOp')
            
    def desempeno_local(self, estado, accion):
        robot, A, B, C, D, E, F = estado

        
        return (0 if accion == 'noOp' and A == B == C == D == E == F =='limpio' else
                -2 if accion == 'subir' or accion == 'bajar' else
                -1)


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
                'irDerecha' if robot == 'A' else
                'irDerecha' if robot == 'B' else
                'subir' if robot == 'C' else
                'bajar' if robot == 'D' else
                'irIzquierda' if robot == 'E' else
                'irIzquierda')


class AgenteReactivoModeloDosCuartos(entornos.Agente):
    
##  Un agente reactivo basado en modelo
    
    def __init__(self):
          
        self.modelo = ['A', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio']
        self.lugar = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6}

    def programa(self, percepcion):
        robot, situacion = percepcion

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[self.lugar[robot]] = situacion

        # Decide sobre el modelo interno
        A, B, C, D, E, F = self.modelo[1], self.modelo[2], self.modelo[3], self.modelo[4], self.modelo[5], self.modelo[6]


                    


        
        return ('noOp' if A == B == C == D == E == F == 'limpio' else
                'limpiar' if situacion == 'sucio' else
                'subir' if ((robot == 'A' or robot == 'B' or robot == 'C') and (A == 'limpio' and B == 'limpio' and C == 'limpio')) else
                'bajar' if ((robot == 'D' or robot == 'E' or robot == 'F') and (D == 'limpio' and E == 'limpio' and F == 'limpio')) else
                'irDerecha' if ((robot == 'A' or robot == 'D') or (robot == 'B' and A == 'limpio') or (robot == 'E' and D == 'limpio')) else
                'irIzquierda')


def test():
    """
    Prueba del entorno y los agentes
    """

    #Número de pruebas
    n = 100
    #Cuarto inicial
    cuarto = 'B'
    
    print "Prueba del entorno de dos cuartos con un agente aleatorio"
    entornos.simulador(DosCuartos(),
                       AgenteAleatorio(['irDerecha', 'irIzquierda', 'subir', 'bajar', 'limpiar', 'noOp']),
                       (cuarto, 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio'), n)

    print "Prueba del entorno de dos cuartos con un agente reactivo"
    entornos.simulador(DosCuartos(),
                       AgenteReactivoDoscuartos(),
                       (cuarto, 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio'), n)

    print "Prueba del entorno de dos cuartos con un agente reactivo"
    entornos.simulador(DosCuartos(),
                       AgenteReactivoModeloDosCuartos(),
                       (cuarto, 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio'), n)

if __name__ == '__main__':
    test()
