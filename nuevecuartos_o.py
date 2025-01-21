import entornos_o
from random import choice


__author__ = 'alantorres'

class NueveCuartos(entornos_o.Entorno):

    def __init__(self, x0 = ["A", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]):
        self.x = x0
        self.costo = 0



    def accion_legal(self, action):
        if (action == "go_right" and self.x[0] in ("C", "F", "I")):
            return False
        elif (action == "go_left" and self.x[0] in ("A", "D", "G")):
            return False
        elif (action == "go_up" and self.x[0] in ("A", "B", "C")):
            return False
        elif (action == "go_down" and self.x[0] in ("G", "H", "I")):
            return False
        else:
            return action in ("go_right", "go_left", "go_up", "go_down", "clean", "nothing")

    def transicion(self, action):
        if not self.accion_legal(action):
            return


        cuartos = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "I"]]
        robot, a, b, c, d, e, f, g, h, i = self.x

        def buscar_indice(matriz, elemento):
            for i, fila in enumerate(matriz):
                if elemento in fila:
                    return i, fila.index(elemento)
            return None  
    
        index = buscar_indice(cuartos, self.x[0])

        if action != "nothing" or a == "sucio" or b == "sucio" or c == "sucio" or d == "sucio" or e == "sucio" or f == "sucio" or g == "sucio" or h == "sucio" or i == "sucio":
            self.costo += 1
        if action == "clean":
            self.x[" ABCDEFGHI".find(self.x[0])] = "limpio"
        elif action == "go_right":
            self.costo += 1
            self.x[0] = cuartos[index[0]][index[1] + 1]
        elif action == "go_left":
            self.costo += 1
            self.x[0] = cuartos[index[0]][index[1] - 1]

        elif action == "go_up":
            self.costo += 2
            self.x[0] = cuartos[index[0] - 1][index[1]]
        elif action == "go_down":
            self.costo += 2
            self.x[0] = cuartos[index[0] + 1][index[1]]
    
    def percepcion(self):
        return self.x[0], self.x[" ABCDEFGHI".find(self.x[0])]


class AgenteAleatorio(entornos_o.Agente):
    def __init__(self, actions, entorno):
        self.actions = actions
        self.entorno = entorno

    def programa(self, _): 
        acciones_legales = [action for action in self.actions if self.entorno.accion_legal(action)]
        if not acciones_legales:
            raise ValueError("No hay acciones legales disponibles.")
        return choice(acciones_legales)

class AgenteReactivoNueveCuartos(entornos_o.Agente):
    
    def __init__ (self, entorno):
        self.entorno = entorno

    def programa(self, percepcion):
         robot, situacion = percepcion
         if situacion == "sucio":
             return "clean"
         else:
             acciones_legales = [action for action in ["go_up","go_down", "go_right", "go_left", "nothing"] if self.entorno.accion_legal(action)]
             return choice(acciones_legales)
         

class AgenteReactivoModeloNueveCuartos(entornos_o.Agente):
    def __init__(self, entorno):
       self.modelo = ["A", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"] 
       self.entorno = entorno

    def programa(self, percepcion):
        robot, situacion = percepcion
        self.modelo[0] = robot
        self.modelo[' ABCDEFGHI'.find(robot)] = situacion
        a, b, c, d, e, f, g, h, i = self.modelo[1:10] 

        if all(var == "limpio" for var in [a, b, c, d, e, f, g, h, i]):
           return "nothing"
        elif (situacion == "sucio"):
           return "clean"
        else:
             acciones_legales = [action for action in ["go_up","go_down", "go_right", "go_left"] if self.entorno.accion_legal(action)]
             return choice(acciones_legales)
        

# class AgenteReactivoModeloNueveCuartosCiego(entornos_o.Agente):
    # def __init__(self, entorno):
        # self.modelo = ["?", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]
        # self.entorno = entorno
        # self.acciones_posibles = ["go_up", "go_down", "go_right", "go_left", "clean"]
   #  
    # def programa(self, percepcion):
        # cuartos = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "I"]]
        # acciones_legales = [
            # accion for accion in self.acciones_posibles
            # if accion == "clean" or self.entorno.accion_legal(accion)
        # ]
        # accion = choice(acciones_legales)

    
def test():
    x0 = ["A", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]
    print("Prueba del entorno con un agente aleatorio")
    entornos_o.simulador(NueveCuartos(x0), AgenteAleatorio(["go_up","go_down", "go_right", "go_left", "clean", "nothing"], NueveCuartos(x0)), 100)


    x1 = ["A", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]
    print("Prueba del entorno con un agente reactivo")
    entornos_o.simulador(NueveCuartos(x1),AgenteReactivoNueveCuartos(NueveCuartos(x0)),100)

    x2 = ["A", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]
    entornos_o.simulador(NueveCuartos(x2),AgenteReactivoModeloNueveCuartos(NueveCuartos(x0)),100)
if __name__ == "__main__":
    test()
