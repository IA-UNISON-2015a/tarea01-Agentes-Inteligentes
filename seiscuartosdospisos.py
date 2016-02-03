import entornos
from random import choice


"""
                        Seis cuartos en dos pisos:

                    D           E            F

                    A           B            C


"""

class SeisCuartosDosPisos(entornos.Entorno):

    def transicion(self, estado, estado_anterior, accion):
        if not self.accion_legal(estado,accion):
            raise ValueError("La accion no es legal para este estado")
        ant,a,b,c,d,e,f = estado_anterior
        robot,A,B,C,D,E,F = estado

        return (('A', A, B, C, D, E, F) if ((accion == 'irIzquierda' and ant == 'B') or (accion == 'bajar' and ant == 'D')) else
                ('B', A, B, C, D, E, F) if ((accion == 'irDerecha' and (ant == 'A')) or (accion == 'irIzquierda' and (ant == 'C')) or (accion == 'bajar' and ant == 'E')) else
                ('C', A, B, C, D, E, F) if ((accion == 'irDerecha' and ant == 'B') or (accion == 'bajar' and ant == 'F')) else
                ('D', A, B, C, D, E, F) if ((accion == 'irIzquierda' and ant == 'E') or (accion == 'subir' and ant == 'A')) else
                ('E', A, B, C, D, E, F) if ((accion == 'irDerecha' and (ant == 'D')) or (accion == 'irIzquierda' and (ant == 'F')) or (accion == 'subir' and ant == 'B')) else
                ('F', A, B, C, D, E, F) if ((accion == 'irDerecha' and ant == 'E') or (accion == 'subir' and ant == 'C')) else
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
        robot, A, B = estado
        return (0 if accion == 'noOp' and A == B == 'limpio' else
                -2 if accion == 'subir' or accion == 'bajar' else
                -1)
