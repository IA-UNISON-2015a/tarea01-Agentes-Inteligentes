import copy

class Environment:
    def __init__(self, x0=None):
        if x0 is None:
            x0 = {'state': 4, 'house': ['nasty']*6}
        self.x = x0
        self.performance = 0

    '''def copyCat(self):
        newdict = self.x
        newdi
'''

    def legalAction(self, action):
        if not action in ("left", "right", "down", "up", "clean", "nuthin"):
            return False
        elif self.x['state'] in (4, 5, 6) and action == 'down':
            return False
        elif self.x['state'] in (1, 2, 3) and action == 'up':
            return False
        else:
            return True

    ''' [1][2][3] <--- rooms        My house.
            H     <--- stairs
        [4][5][6] <--- rooms   
    '''

    def transition(self, action):
        if not self.legalAction(action):
            raise ValueError("Epale, acción no legal.")

        if action == 'left':
            self.performance -= 1
            self.x['state'] -= 1 if not self.x['state'] in (1,4) else 0
        elif action == 'right':
            self.performance -= 1
            self.x['state'] += 1 if not self.x['state'] in (3,6) else 0
        elif action == 'clean':
            self.performance -= 1
            self.x['house'][self.x['state']-1] = 'clean'
        elif action == 'down':
            self.performance -= 2 if self.x['state'] == 2 else 3
            self.x['state'] = 5
        elif action == 'up':
            self.performance -= 2 if self.x['state'] == 5 else 3
            self.x['state'] = 2
        elif 'nasty' in self.x['house']:
            self.performance -= 1
        else:
            pass

    def perception(self):
        return self.x['state'], self.x['house'][self.x['state']-1]

class ReactiveAgent:
        def __init__(self):
            self.memory = ['nasty']*6   #self.memory[0:1, 1:2 , 2:3, 3:4, 4:5, 5:6]
        def program(self, perception):
            robot, state = perception
            print(state)
            if 'nasty' not in self.memory:
                return 'nuthin'
            elif state == 'nasty':
                self.memory[robot-1] = 'clean'
                return 'clean'
            elif robot in (1, 2, 3) and 'nasty' not in self.memory[:3]:
                return 'down'
            elif robot in (4, 5, 6) and 'nasty' not in self.memory[4:]:
                return 'up'
            elif state == 'clean' and robot == 2:
                return 'left' if self.memory[2] == 'clean' else 'right'
            elif state == 'clean' and robot == 5:
                return 'left' if self.memory[5] == 'clean' else 'right'
            elif state == 'clean':
                return 'right' if robot in (1, 4) else 'left'
            else:
                print('Epale.')


def simulator(environment, agent, steps=100, verbose=True):
    history_performance = [environment.performance]
    history_states = [copy.deepcopy(environment.x)]
    history_actions = []

    for step in range(steps):
        p = environment.perception()
        a = agent.program(p)
        environment.transition(a)

        history_performance.append(environment.performance)
        history_states.append(copy.deepcopy(environment.x))
        history_actions.append(a)

    history_actions.append(None)

    if verbose:
        print(u"\n\nSimulación de entorno tipo " +
              str(type(environment)) +
              " con el agente tipo " +
              str(type(agent)) + "\n")

        print('Paso'.center(10) +
              'Estado'.center(40) +
              u'Acción'.center(25) +
              u'Desempeño'.center(15))

        print('_' * (10 + 40 + 25 + 15))

        for i in range(steps):
            print(str(i).center(10) +
                  str(history_states[i]).center(40) +
                  str(history_actions[i]).center(25) +
                  str(history_performance[i]).rjust(12))

        print('_' * (10 + 40 + 25 + 15) + '\n\n')

    return history_states, history_actions, history_performance

env = Environment()
ra =  ReactiveAgent()

simulator(env, ra)