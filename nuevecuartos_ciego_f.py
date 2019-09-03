from nuevecuartos_f import *

class NueveCuartosCiego(NueveCuartos):
        
    
    def percepcion(self, estado):
        # regresa en donde se encuentra el robot
        return estado[0]


class AgenteReactivoModeloNueveCuartosCiego(AgenteReactivoModeloNueveCuartos):
    """
        Este robot ciego en el mejor de los casos hace 15 acciones, de las cuales 7 son movimientos, 8 limpiezas.
        Para que siempre realice su trabajo racionalmente, haremos que siga un patron de movimiento en espiral.
        Si el entorno se puede ver asi:
            G H I
            D E F
            A B C
        entonces habra de ir, en el mejor de los casos, por A, B, C, F, I, H, G, D, E.

        El factor clave sera el numero de movimientos que ha realizado cuando llegue a D. Si es menos de 7, significa que no limpio
        al menos un cuarto. Por lo tanto, la accion regresada sera 'bajar' en vez de 'ir_derecha' hacia E.
        Una vez estando en E, si el numero de movimientos es menor a 8, significa tambien que dejo al menos un cuarto sucio.
    """

    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos
        """

        # solo sabe donde se encuentra y si va llegando. Si ya limpio, se cambia a True el segundo valor del modelo
        # y por ultimo, el tercer valor es el numero de veces que se ha movido
        self.modelo = ['A', False, 0]

    def programa(self, percepcion):
        robot = percepcion

        # Actualiza el modelo interno
        self.modelo[0] = robot

        limpiado = self.modelo[1]
        movimientos = self.modelo[2]
        # siempre limpia puesto que es ciego
        if not limpiado:
            self.modelo[1] = True   # indicamos que ya ha limpiado
            return 'limpiar'

        # con cada movimiento, indicamos que no sabe si ha limpiado en el cuarto siguiente
        # asi como aumentar el numero de movimientos
        # despues de limpiar
        elif robot in 'AB':
            self.modelo[1] = False
            self.modelo[2] += 1
            return 'ir_derecha'
        elif robot in 'C':
            self.modelo[1] = False
            self.modelo[2] += 1
            return 'subir'
        elif robot in 'F':
            self.modelo[1] = False
            self.modelo[2] += 1
            return 'subir'
        elif robot in 'HI':
            self.modelo[1] = False
            self.modelo[2] += 1
            return 'ir_izquierda'
        elif robot in 'G':
            self.modelo[1] = False
            self.modelo[2] += 1
            return 'bajar'
        elif robot in 'D' and movimientos < 7:
            self.modelo[1] = False
            self.modelo[2] += 1
            return 'bajar'
        elif robot in 'D' and movimientos >= 7:
            self.modelo[1] = False
            self.modelo[2] += 1
            return 'ir_derecha'
        elif robot in 'E' and movimientos < 8:
            self.modelo[1] = False
            self.modelo[2] += 1
            return 'ir_derecha'
        elif robot in 'E' and movimientos >= 8:
            return 'nada'

def prueba_agente_ciego(agente):
    cuartos = {}
    for char in 'ABCDEFGHI':
        cuartos[char] = 'sucio'
    entornos_f.imprime_simulacion(
        entornos_f.simulador(
            NueveCuartosCiego(),
            agente,
            ["B", cuartos.copy()],
            50
        ),
        ["B", cuartos]
    )


def test_ciego():
    """
    Prueba del entorno y los agentes
    """

    print("Prueba del entorno con un agente reactivo con modelo")
    prueba_agente_ciego(AgenteReactivoModeloNueveCuartosCiego())

    # print("Prueba del entorno con un agente aleatorio")
    # prueba_agente(AgenteAleatorio(['ir_izquierda', 'ir_derecha', 'limpiar', 'subir', 'bajar', 'nada']))

if __name__ == "__main__":
    test_ciego()