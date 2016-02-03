import entornos
from random import choice


"""
                        Seis cuartos en dos pisos:

                    D           E            F

                    A           B            C


"""

class SeisCuartosDosPisos(entornos.Entorno):

    def transicion(self, estado, accion):
        # if not self.accion_legal(estado,accion):
            # raise ValueError("La accion no es legal para este estado")
        robot,A,B,C,D,E,F = estado

        return (('A', A, B, C, D, E, F) if ((accion == 'irIzquierda' and robot == 'B') or (accion == 'bajar' and robot == 'D')) else
                ('B', A, B, C, D, E, F) if ((accion == 'irDerecha' and (robot == 'A')) or (accion == 'irIzquierda' and (robot == 'C')) or (accion == 'bajar' and robot == 'E')) else
                ('C', A, B, C, D, E, F) if ((accion == 'irDerecha' and robot == 'B') or (accion == 'bajar' and robot == 'F')) else
                ('D', A, B, C, D, E, F) if ((accion == 'irIzquierda' and robot == 'E') or (accion == 'subir' and robot == 'A')) else
                ('E', A, B, C, D, E, F) if ((accion == 'irDerecha' and (robot == 'D')) or (accion == 'irIzquierda' and (robot == 'F')) or (accion == 'subir' and robot == 'B')) else
                ('F', A, B, C, D, E, F) if ((accion == 'irDerecha' and robot == 'E') or (accion == 'subir' and robot == 'C')) else
                (robot, A, B, C, D, E, F) if accion == 'noOp' else
                ('A', 'limpio', B, C, D, E, F) if accion == 'limpiar' and robot == 'A' else
                ('B', A, 'limpio', C, D, E, F) if accion == 'limpiar' and robot == 'B' else
                ('C', A, B, 'limpio', D, E, F) if accion == 'limpiar' and robot == 'C' else
                ('D', A, B, C, 'limpio', E, F) if accion == 'limpiar' and robot == 'D' else
                ('E', A, B, C, D, 'limpio', F) if accion == 'limpiar' and robot == 'E' else
                ('F', A, B, C, D, D, 'limpio')
                )

    def sensores(self, estado):
        robot, A, B, C, D, E, F = estado
        return robot, (A if robot == 'A' else
                       B if robot == 'B' else
                       C if robot == 'C' else
                       D if robot == 'D' else
                       E if robot == 'E' else
                       F)

    def accion_legal(self, estado, accion):
        robot,A,B,C,D,E,F = estado
        if accion in ('irIzquierda', 'irDerecha', 'subir', 'bajar', 'limpiar', 'noOp'):
            return (True if (accion == 'subir' and (robot == 'A' or robot =='B' or robot == 'C')) or
                            (accion == 'bajar' and (robot == 'D' or robot == 'E' or robot == 'F')) or
                            (accion == 'irIzquierda' and (robot != 'A' and robot != 'D')) or
                            (accion == 'irDerecha' and (robot != 'C' and robot != 'F')) else
                    False)

    def desempeno_local(self, estado, accion):
        robot, A, B, C, D, E, F = estado
        return (0 if accion == 'noOp' and A == B == 'limpio' else
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


class AgenteReactivoModeloDosCuartos(entornos.Agente):
    """
    Un agente reactivo basado en modelo

    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
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
                'irDerecha' if robot == 'A' or robot == 'B' and C != 'limpio' else
                'subir' if robot == 'C' else
                'irIzquierda' if robot == 'F' or robot == 'E' else
                'bajar')


def test():
    """
    Prueba del entorno y los agentes

    """
    print "Prueba del entorno de dos cuartos con un agente aleatorio"
    entornos.simulador(SeisCuartosDosPisos(),
                       AgenteAleatorio(['irIzquierda', 'irDerecha', 'subir', 'bajar', 'limpiar', 'noOp']),
                       ('A', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio'), 20)

    print "Prueba del entorno de dos cuartos con un agente reactivo"
    entornos.simulador(SeisCuartosDosPisos(),
                       AgenteReactivoModeloDosCuartos(),
                       ('A', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio'), 20)

if __name__ == '__main__':
    test()