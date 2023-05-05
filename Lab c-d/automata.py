from node import Node
from graphviz import Digraph
from itertools import groupby


class Automata:

    def __init__(self, automata_type, regex = None, states=None, symbols=None, start=None, acceptance=None, transitions=None):

        if automata_type == "from_definitions":
            if (states is None or symbols is None or start is None or acceptance is None or transitions is None):
                raise ValueError("Por favor ingresa los valores correctos")
            elif (len(states) < 0 or len(symbols) < 0 or len(start) < 0 or len(acceptance) < 0 or len(transitions) < 0):
                raise ValueError("Por favor ingresa los valores correctos")
            self.states = states
            self.symbols = symbols
            self.start = start
            self.acceptance = acceptance
            self.transitions = transitions
        
        elif automata_type == "afn_from_regex":
            if regex == None:
                raise ValueError("Por favor ingresa los valores correctos")
            self.afn_from_regex(regex)

        elif automata_type == "basic_automata":
            self.states=[f'{states}', f'{states + 1}']
            self.acceptance=[f'{states + 1}']
            self.symbols=[symbols]
            self.start=[f'{states}']
            self.transitions=[(f'{states}', symbols, f'{states + 1}')]

        elif automata_type == "afd_from_regex":
            if regex == None:
                raise ValueError("Por favor ingresa los valores correctos")
            self.afd_from_regex(regex)

        elif automata_type == "afd_from_afn_from_regex":
            if regex == None:
                raise ValueError("Por favor ingresa los valores correctos")
            self.AFD = []
            self.afn_from_regex(regex)
            self.toAFD()
            #self.represent_graph()
        
        elif automata_type == "(":
            self.states=["s1","s2"]
            self.acceptance=["s2"]
            self.symbols=["("]
            self.start=["s1"]
            self.transitions=[("s1","(","s2")]

        elif automata_type == ")":
            self.states=["s1","s2"]
            self.acceptance=["s2"]
            self.symbols=[")"]
            self.start=["s1"]
            self.transitions=[("s1",")","s2")]
        
        elif automata_type == "char":
            self.states=["s1","s2"]
            self.acceptance=["s2"]
            self.symbols=[regex]
            self.start=["s1"]
            self.transitions=[("s1",regex,"s2")]
            #self.represent_graph()



    def represent_graph(self):
        dot = Digraph()
        for state in self.states:
            if state in self.start and state not in self.acceptance:
                dot.node('start (' + str(state) + ')')
            if state in self.acceptance and state not in self.start:
                dot.node('end (' + str(state) + ')', shape='doublecircle')
            if state in self.acceptance and state in self.start:
                dot.node('start/end (' + str(state) + ')', shape='doublecircle')
            if state not in self.acceptance and state not in self.start:
                dot.node(str(state))
        for transition in self.transitions:
            if transition[0] != None and transition[2] != None:
                dot.edge('end (' + str(transition[0])+')' if transition[0] in self.acceptance and transition[0] not in self.start
                        else 'start (' + str(transition[0])+')' if  transition[0] in self.start and transition[0] not in self.acceptance 
                        else 'start/end (' + str(transition[0])+')' if transition[0] in self.start and transition[0] in self.acceptance
                        else str(transition[0]) , 
                        'end (' + str(transition[2])+')' if transition[2] in self.acceptance and transition[2] not in self.start 
                        else 'start (' + str(transition[2])+')' if  transition[2] in self.start and transition[2] not in self.acceptance
                        else 'start/end (' + str(transition[2])+')' if  transition[2] in self.start and transition[2] in self.acceptance
                        else str(transition[2])
                        , label = transition[1])
        dot.render('graph')

    """
    Funcion para escribir archivos de texto con las respuestas.
    """
    def writeTxt(self, fileName, states, symbols, start, accepting, transitions, type, dict={}):
        f = open(fileName, "w+")
        f.write("ESTADOS = " + str(states) + '\n')
        f.write("SIMBOLOS = " + str(symbols) + '\n')
        f.write("INICIO = " + str(start) + '\n')
        f.write("ACEPTACION = " + str(accepting) + '\n')
        f.write("TRANSICIONES = [")
        for indx in range(len(transitions)):
            if indx < 1:
                f.write(str(transitions[indx]) + ',\n')
            if indx == len(transitions) - 1:
                f.write('\t\t\t\t' + str(transitions[indx]) + ']')
            elif indx >= 1:
                f.write('\t\t\t\t' + str(transitions[indx]) + ',\n')

        f.write('\n')

        if type == 'mini':
            f.write("NUEVA REPRESENTACION DE ESTADOS = {")
            for index, (k, v) in enumerate(dict.items()):
                if index < 1:
                    f.write("'" + str(k) + "': " + str(v) + ',\n')
                if index == len(dict) - 1:
                    f.write('\t\t\t\t\t\t\t\t' + "   '" + str(k) + "': " + str(v) + '}')
                elif index >= 1:
                    f.write('\t\t\t\t\t\t\t\t' + "   '" + str(k) + "': " + str(v) + ',\n')
        f.close()
        return

    def afn_from_regex(self,regex):
        posfixExpression = regex.toPosfix()
        print(f"La expresión es: {regex.expression}")
        regex_splitted = [char for char in posfixExpression]
        stack = []
        current_status = 0
        for item in regex_splitted:
            # Algorithm
            # 1. If it is an item, append to the stack
            # 2. If it is an operation, do the calculation and append result to the stack.
            # 3. Finish when there is only one element left on the stack and is an automata.
            if item not in ["*", "@", "|", "+", "?"]:
                # It is a character
                stack.insert(0, item)
            elif item in ["*", "@", "|", "+", "?"]:
                if item == "@":
                    # Concat
                    rightOperand = stack.pop(0)
                    leftOperand = stack.pop(0)
                    if not isinstance(leftOperand, Automata):
                        leftOperand = Automata(automata_type="basic_automata",states=current_status, symbols=leftOperand)
                        current_status += 2
                    if not isinstance(rightOperand, Automata):
                        rightOperand = Automata(automata_type="basic_automata",states=current_status, symbols=rightOperand)
                        current_status += 1
                    # Create the result Automata
                    result_automata = Automata(
                        automata_type="from_definitions",
                        states=list(dict.fromkeys(leftOperand.states + rightOperand.states)),
                        acceptance=rightOperand.acceptance,
                        start=leftOperand.start,
                        symbols=list(dict.fromkeys(leftOperand.symbols + rightOperand.symbols + ["&"])),
                        transitions=leftOperand.transitions + rightOperand.transitions + [
                            (leftOperand.acceptance[0], "&", rightOperand.start[0])]
                    )
                    stack.insert(0, result_automata)
                    current_status += 1
                elif item == "|":
                    # Union
                    rightOperand = stack.pop(0)
                    leftOperand = stack.pop(0)
                    if not isinstance(leftOperand, Automata):
                        leftOperand = Automata(automata_type="basic_automata",states=current_status, symbols=leftOperand)
                        current_status += 2
                    if not isinstance(rightOperand, Automata):
                        rightOperand = Automata(automata_type="basic_automata",states=current_status, symbols=rightOperand)
                        current_status += 1
                    # Create the result automata
                    current_status += 1
                    start_state = current_status
                    current_status += 1
                    end_state = current_status
                    result_automata = Automata(
                        automata_type="from_definitions",
                        states=list(dict.fromkeys(leftOperand.states + rightOperand.states)) + [f'{start_state}',f'{end_state}'],
                        acceptance=[f'{end_state}'],
                        start=[f'{start_state}'],
                        symbols=list(dict.fromkeys(leftOperand.symbols + rightOperand.symbols + ["&"])),
                        transitions=leftOperand.transitions + rightOperand.transitions + [
                            (f'{start_state}', "&", leftOperand.start[0]),
                            (f'{start_state}', "&", rightOperand.start[0]),
                            (leftOperand.acceptance[0], "&", f'{end_state}'),
                            (rightOperand.acceptance[0], "&", f'{end_state}'),
                        ]
                    )
                    stack.insert(0, result_automata)
                    current_status += 1

                elif item == "*":
                    # Kleene
                    operand = stack.pop(0)
                    if not isinstance(operand, Automata):
                        operand = Automata(automata_type="basic_automata",states=current_status, symbols=operand)
                        current_status += 1
                    # Create the result automata
                    current_status += 1
                    start_state = current_status
                    current_status += 1
                    end_state = current_status
                    result_automata = Automata(
                        automata_type="from_definitions",
                        states=list(dict.fromkeys(operand.states)) + [f'{start_state}',
                                                                      f'{end_state}'],
                        acceptance=[f'{end_state}'],
                        start=[f'{start_state}'],
                        symbols=list(dict.fromkeys(operand.symbols + ["&"])),
                        transitions=operand.transitions + [
                            (operand.acceptance[0], "&", operand.start[0]),
                            (f'{start_state}', "&", f'{end_state}'),
                            (f'{start_state}', "&", operand.start[0]),
                            (operand.acceptance[0], "&", f'{end_state}'),
                        ]
                    )
                    stack.insert(0, result_automata)
                    current_status += 1
                    
                
                elif item == "?":
                    operand = stack.pop(0)
                    if not isinstance(operand, Automata):
                        operand = Automata(automata_type="basic_automata",states=current_status, symbols=operand)
                        current_status += 1
                    current_status += 1
                    start_state = current_status
                    current_status += 1
                    end_state = current_status
                    result_automata = Automata(
                        automata_type="from_definitions",
                        states=list(dict.fromkeys(operand.states)) + [f'{start_state}',
                                                                      f'{end_state}'],
                        acceptance=[f'{end_state}'],
                        start=[f'{start_state}'],
                        symbols=list(dict.fromkeys(operand.symbols + ["&"])),
                        transitions=operand.transitions + [
                            (f'{start_state}', "&", f'{end_state}'),
                            (f'{start_state}', "&", operand.start[0]),
                            (operand.acceptance[0], "&", f'{end_state}'),
                        ]
                    )
                    stack.insert(0, result_automata)
                    current_status += 1

                elif item == "+":
                    operand = stack.pop(0)
                    if not isinstance(operand, Automata):
                        operand = Automata(automata_type="basic_automata",states=current_status, symbols=operand)
                        current_status += 1
                    current_status += 1
                    start_state = current_status
                    current_status += 1
                    end_state = current_status
                    result_automata = Automata(
                        automata_type="from_definitions",
                        states=list(dict.fromkeys(operand.states)) + [f'{start_state}',
                                                                      f'{end_state}'],
                        acceptance=[f'{end_state}'],
                        start=[f'{start_state}'],
                        symbols=list(dict.fromkeys(operand.symbols + ["&"])),
                        transitions=operand.transitions + [
                            (operand.acceptance[0], "&", operand.start[0]),
                            (f'{start_state}', "&", operand.start[0]),
                            (operand.acceptance[0], "&", f'{end_state}'),
                        ]
                    )
                    stack.insert(0, result_automata)
                    current_status += 1

        #stack[0].writeTxt('respuestas/FromRegex_To_AFN.txt', stack[0].states, stack[0].symbols, stack[0].start, stack[0].acceptance,
        #              stack[0].transitions, 'FromRegex_To_AFN')

        print(stack[0])
        self.states = stack[0].states
        self.symbols = stack[0].symbols
        self.start = stack[0].start
        self.acceptance = stack[0].acceptance
        self.transitions = stack[0].transitions

    def e_closure(self, state):
        closure = [state]
        # Get index for starting state
        idx = self.states.index(state)
        # Start building the closure
        for i in range(0,len(self.matrix[idx])):
            if self.matrix[idx][i].count("&") > 0 and i != idx:
                closure = closure + self.e_closure(self.states[i])
        return closure

    def e_closures(self, states):
        for state in states:
            c = self.e_closure(state)
            states = states + c
        return list(dict.fromkeys(states))

    def move(self, s, c):
        end_states = []
        for state in s:
            # Get the index on the state
            idx = self.states.index(state)
            for i in range(0, len(self.matrix[idx])):
                if self.matrix[idx][i].count(c) > 0:
                    end_states.append(self.states[i])
        return end_states

    def simulate_afn(self, word):
        s = self.e_closure(self.start[0])
        for char in word:
            s = self.e_closures(self.move(s, char))
        for state in s:
            if self.acceptance.count(state) > 0: return True
        return False

    def afd_from_regex(self,regex):
        self.follow_pos(regex)
        self.build_transition_table_from_follow_pos()
        self.represent_graph()
        #self.writeTxt("AFD_FROM_REGEX",self.states,self.symbols, self.start, self.acceptance, self.transitions, "asd")

    # Para poder implementar el algoritmo de conversion directa de regex a AFD debemos construir un arbol sintactico
    def follow_pos(self,regex):
        posfix = regex.toPostfixIdentity(True)
        # El stack mantiene el orden de los elementos para unirlos a sus respectivos nodos
        tree_stack = []
        # Guardamos la ultima posicion almacenada para llevar un buen control de los nodos, esta posicion
        # se almacena en el nodo y nos sirve para el algoritmo
        position = 1
        # por cada elemento en la expresion posfix realizamos la asignacion de elementos a sus respectivos nodos
        # tambien opbtenemos nullable, la primera posicion y ultima posicion
        for item in posfix:
            # Si el elemento pertenece al alfabeto se inserta en el stack
            if item not in ["*", "@", "|"]:
                tree_stack.insert(0, item)
            
            # Si el elemento pertenece a los operadores realizamos la asignacion de las variables en el algoritmo
            elif item in ["*", "@", "|"]:

                if item in ["@", "|"]:

                    # En caso el operador pertenece a concatenacion o seleccion obtenemos los elementos tanto
                    # de la izquierda como de la derecha
                    rightOperand = tree_stack.pop(0)
                    leftOperand = tree_stack.pop(0)
                    
                    # verificamos que el elemento izquierdo sea un caracter o un nodo
                    if not isinstance(leftOperand, Node):
                        # en caso sea caracter, sea un elemento, esto quiere decir que encontramos una hoja
                        # del arbol por lo que colocamos su primera y ultima posicion como si mismo(su sposicion actual).
                        leftOperand = Node(value=leftOperand, right_child=None, left_child=None, position=position)
                        leftOperand.first_pos = [position]
                        leftOperand.last_pos = [position]
                        # aumentamos uno en el registro de posiciones que llevamos
                        position += 1
                    
                    # verificamos que el elemento derecho sea un caracter o un nodo
                    if not isinstance(rightOperand, Node):
                        # en caso sea caracter, sea un elemento, esto quiere decir que encontramos una hoja
                        # del arbol por lo que colocamos su primera y ultima posicion como si mismo(su sposicion actual).
                        rightOperand = Node(value=rightOperand, right_child=None, left_child=None, position=position)
                        rightOperand.first_pos = [position]
                        rightOperand.last_pos = [position]
                        # aumentamos uno en el registro de posiciones que llevamos
                        position += 1
                    
                    # instanciamos el nuevo nodo y le introducimos tanto el operando izquierdo como el derecho.
                    # en este caso se colocaria como izquiero o derecho otro nodo. Dependiendo de si se encontro en el
                    # stack un elemento o no, los nodos hijos serian hojas u otros caminos.
                    new_node = Node(left_child=leftOperand, right_child=rightOperand, value=item)
                    leftOperand.root = new_node

                    # Ahora, es distinto como funciona el algoritmo para concatenacion y seleccion por lo que
                    # definimos las instrucciones para cada escenario
                    if item == "|":
                        # En caso el operador sea de seleccion definimos la primera posicion de ese nodo
                        # como la union de la primera posicion de sus dos nodos hijos. Y la ultima posicion de
                        # ese nodo como la union de la ultima posicion de sus dos nodos hijos.
                        new_node.first_pos = leftOperand.first_pos + rightOperand.first_pos
                        new_node.last_pos = leftOperand.last_pos + rightOperand.last_pos
                    
                    elif item == "@":
                        # En caso el operador sea de concatenacion debemos hacer otras validaciones
                        new_node.first_pos = leftOperand.first_pos
                        new_node.last_pos = rightOperand.last_pos

                        # Si el operador izquierdo es anulable, la primera posicion del nodo sera la union de
                        # la primera posicion de sus dos nodos hijos, en caso contrario sera unicamente la
                        # primera posicion de su nodo izquierdo.
                        if leftOperand.nullable():
                            new_node.first_pos = new_node.first_pos + rightOperand.first_pos

                        # Si el operador derecho es anulable, la ultima posicion del nodo en cuestion sera la
                        # union de la ultima posicion de sus dos nodos hijos, en caso contrario sera unicamente
                        # la ultima posicion de su nodo derecho
                        if rightOperand.nullable():
                            new_node.last_pos = new_node.last_pos +  leftOperand.last_pos

                else:
                    # En caso el operador encontrado sea la estrella de kleen debemos extraer unicamente
                    # un elemento del stack
                    operand = tree_stack.pop(0)
                    # Si el siguiente elemento es un caracter, creamos la hoja sobre un nodo y lo definimos
                    # como nuestro elemento.
                    if not isinstance(operand, Node):
                        operand = Node(value=operand, right_child=None, left_child=None, position=position)
                        operand.first_pos = [position]
                        operand.last_pos = [position]
                        position += 1

                    # Instanciamos el nuevo nodo con un solo hijo 
                    new_node = Node(middle_child=operand,value=item, left_child=None, right_child=None)
                    # La primera y ultima posicion son la primera y ultima posicion de su unico hijo
                    new_node.first_pos = operand.first_pos
                    new_node.last_pos = operand.last_pos


                # Add the new node to the tree stack
                tree_stack.insert(0, new_node)

        curr_node = tree_stack[0]
        follow_pos = {}
        node_symbol = {}
        visit_queue = [curr_node]
        visited = []
        for i in range(1, position):
            follow_pos[str(i)] = []

        while len(visit_queue) != 0:
            visit_node = visit_queue.pop()

            left_child = visit_node.left_child
            right_child = visit_node.right_child
            middle_child = visit_node.middle_child

            if visit_node.value not in ["@","*","|"]:
                node_symbol[str(visit_node.last_pos[0])] = visit_node.value[0]

            if visit_node in visited:
                continue

            if visit_node.value == "@" and left_child and right_child:
                for lp in left_child.last_pos:
                    for fp in right_child.first_pos:
                        follow_pos[str(lp)].append(fp)

            if visit_node.value == "*" and middle_child:
                for lp in middle_child.last_pos:
                    for fp in middle_child.first_pos:
                        follow_pos[str(lp)].append(fp)

            if visit_node.single_child and visit_node.middle_child is not None:
                visit_queue.append(visit_node.middle_child)
            elif not visit_node.single_child and visit_node.left_child is not None:
                visit_queue.append(visit_node.left_child)
                visit_queue.append(visit_node.right_child)
            visited.append(visit_node)


        self.start = curr_node.first_pos
        self.acceptance = curr_node.last_pos
        self.follow_pos_table = follow_pos
        self.node_symbol = node_symbol


    def build_transition_table_from_follow_pos(self):
        nodes = [int(x) for x in list(self.node_symbol)]
        nodes.sort()
        node_index = 0
        symbols = list(set(self.node_symbol.values()))
        symbols.remove('#')
        transition_table = [[[] for x in range(0,len(symbols)+2)]]
        transition_table[0][0] = self.start
        transition_table[0][0].sort()
        transition_table[0][1] = 's' + str(node_index)
        self.start = ['s' + str(node_index)]
        new_acceptance = []
        new_names = {}
        symbols.sort()
        for transition in transition_table:
            for node in transition_table[transition_table.index(transition)][0]:
                for n in self.follow_pos_table[str(node)]:
                    if self.node_symbol[str(node)] == "&":
                        b = transition_table[transition_table.index(transition)][0]
                        b.append(n)
                        b = list(set(b))
                        b.sort()
                        transition_table[transition_table.index(transition)][0] = b

                    a = transition_table[transition_table.index(transition)][symbols.index(self.node_symbol[str(node)]) + 2]
                    a.append(n)
                    a = list(set(a))
                    a.sort()
                    transition_table[transition_table.index(transition)][symbols.index(self.node_symbol[str(node)]) + 2] = a
            new_names[str(transition[0])] = transition[1]
            for acceptance_state in self.acceptance:
                if acceptance_state in transition[0]:
                    new_acceptance.append(transition[1])
            for symbol in range(2, len(symbols)+2):
                possible_transition = transition_table[transition_table.index(transition)][symbol]
                possible_transition.sort()
                if possible_transition != [] and possible_transition not in [t[0] for t in transition_table]:
                    node_index += 1
                    new_transition = [[] for x in range(0,len(symbols)+2)]
                    new_transition[0] = possible_transition
                    new_transition[1] = 's' + str(node_index)
                    transition_table.append(new_transition)

        self.acceptance = new_acceptance

        for transition in transition_table:
            for i in range(2, len(symbols)+2):
                if transition_table[transition_table.index(transition)][i] != []:
                    transition_table[transition_table.index(transition)][i] = new_names[str(transition_table[transition_table.index(transition)][i])]
                else:
                    transition_table[transition_table.index(transition)][i] = ""
        
        
        for i in range(0,len(transition_table)):
            if "&" in symbols:
                del transition_table[i][symbols.index("&") + 2]
            del transition_table[i][0]

        if "&" in symbols:
            symbols.remove("&")

        self.symbols = symbols
        self.states = list(new_names.values())
        self.transitions = []
        for transition in transition_table:
            for s in range(1,len(symbols) + 1):
                if transition[s] != "" and type(transition[0]) is not list:
                    self.transitions.append((transition[0],symbols[s-1],transition[s]))
                elif transition[s] != "" and type(transition[0]) is list:
                    self.transitions.append((new_names[str(transition[0])],symbols[s-1],transition[s]))

    """
    Esta funcion fue disenada para determinar la matriz que se utilizara posteriormente para algunos calculos
    de la conversion de AFN a AFD.. Cabe mencionar que genera una matriz cubica estados x estados x simbolos
    """
    def createMatrix(self):
        self.matrix = [[[0 for _ in range(len(self.symbols))] for _ in range(len(self.states))] for _ in
                       range(len(self.states))]

        for _ in range(len(self.transitions)):
            self.matrix[self.states.index(self.transitions[_][0])][self.states.index(self.transitions[_][2])][
                self.symbols.index(self.transitions[_][1])] = self.transitions[_][1]
    

    """
    Esta funcion en otras ocasiones tambien es llamada e-closure, la cual tiene como objetivo reunir el alcance
    de todos los estados que tiene un estado con epsilon.
    """
    def find3scope(self, state, transitions=[]):
        if type(state) != list:
            if state not in transitions:
                transitions.append(state)
                for _ in self.transitions:
                    if _[0] == state and _[1] == "&":
                        transitions = self.find3scope(_[2], transitions=transitions)
        else:
            for x in state:
                if x not in transitions:
                    transitions.append(x)
                for _ in self.transitions:
                    if _[0] == x and _[1] == "&":
                        if _[2] not in transitions:
                            transitions = self.find3scope(_[2], transitions=transitions)

        return transitions

    """
    Esta funcion tiene como objetivo reunir todos los estados que procede dependiendo del simbolo que se elije.
    """
    def getState(self, state=[], symbol=None):
        if state == []:
            return []

        if state == [None]:
            return None

        if symbol == None:
            raise ValueError("Ha ocurrido un problema al momento de obtener el AFD")

        newState = []

        if type(state) == list:
            for _ in state:
                res = self.transitionTable[self.states.index(_)][self.symbols.index(symbol)]
                if res is not None:
                    if type(res) is list:
                        for i in res:
                            if i not in newState:
                                newState.append(i)
                    else:
                        if self.transitionTable[self.states.index(_)][self.symbols.index(symbol)] not in newState:
                            newState.append(self.transitionTable[self.states.index(_)][self.symbols.index(symbol)])
        else:
            res = self.transitionTable[self.states.index(state)][self.symbols.index(symbol)]
            if res is not None:
                if type(res) is list:
                    for i in res:
                        if i not in newState:
                            newState.append(i)
                else:
                    if self.transitionTable[self.states.index(state)][self.symbols.index(symbol)] not in newState:
                        newState.append(self.transitionTable[self.states.index(state)][self.symbols.index(symbol)])

        if len(newState) >= 1:
            return newState
        else:
            return None

    """
    En esta funcion se define el AFD, aqui se llaman a las dos funciones anteriores pues el nuevo AFD debe
    contener todos los resultados posibles

    El formato en que se almacena es el siguiente

    [  [ Estado/s de Inicio ], [ por cada simbolo se agrega una lista [ contiene todos los estados a los que transiciona con ese simbolo ], ...  ]  ]
    """
    def defineAFD(self):
        start = [self.start if type(self.start) == list else [self.start], [_ for _ in self.transitionTable[self.states.index(self.start[0])]]]

        self.AFD.append(start)

        actualIndex = 0
        while True:
            actualState = self.AFD[actualIndex][1]
            for _ in range(len(self.symbols)):
                actualSymbol = actualState[_]

                itsOnAFD = False

                for afdStatus in self.AFD:
                    if type(actualSymbol) is list and actualSymbol == afdStatus[0]:
                        itsOnAFD = True
                    elif type(actualSymbol) != list and [actualSymbol] == afdStatus[0]:
                        itsOnAFD = True

                if actualSymbol == None:
                    continue

                elif itsOnAFD == False:
                    newState = [actualSymbol if type(actualSymbol) == list else [actualSymbol],
                                [self.getState(actualSymbol, x) for x in self.symbols]]
                    self.AFD.append(newState)
            actualIndex += 1
            notFound = False
            for _ in self.AFD:
                for x in _[1]:
                    if type(x) != list: x = [x]
                    if x != [None] and x not in [y[0] for y in self.AFD]:
                        notFound = True

            if notFound == False:
                break


    """
    Los procedimientos anteriores generan muchos estados sucios por los que se debe limpiar el AFD
    """
    def cleanAFD(self):
        # Esta funcion debe limpiar el AFD resultante de las funciones para convertir de AFN a AFD
        index = -1
        if '&' in self.symbols:
            index = self.symbols.index('&')
        if index != -1:
            self.changeState(index=index)

    """
    En caso un estado x tenga como unica transicion epsilon, entonces ese epsilon toma el lugar de todos los estados donde se menciona x
    asi se reducen la cantidad de estados y se eliminan algunos problemas que pueden llegar a ocurrir.
    """
    def changeState(self, index):
        remove = []

        for x in self.AFD:
            for i in self.acceptance:
                if i in x[0]:
                    self.AFD.remove(x)
                    self.AFD.append(x)
        for x in self.AFD:
            flag = False
            containsAcceptance = False
            for i in x[1]:
                if i != None and x[1].index(i) != index:
                    flag = True
            if flag == False and x[0] == self.start:
                self.start = x[1][index]

            for i in self.acceptance:
                if i in x[0]:
                    containsAcceptance = True

            if flag == False and x[1][index] != None and containsAcceptance is False:
                for i in range(len(self.AFD)):
                    for ii in range(len(self.AFD[i][1])):
                        if type(self.AFD[i][1][ii]) == list and sorted(self.AFD[i][1][ii]) == sorted(x[0]):
                            self.AFD[i][1][ii] = sorted(x[1][index])
                        elif type(self.AFD[i][1][ii]) != list and sorted([self.AFD[i][1][ii]]) == sorted(x[0]):
                            self.AFD[i][1][ii] = sorted(x[1][index])
                        else:
                            pass
                remove.append(x)
            if flag == False and x[1][index] != None and containsAcceptance is True:
                for i in range(len(self.AFD)):

                    if self.AFD[i][0] == x[1][index]:
                        for ii in range(len(self.symbols)):
                            self.AFD[self.AFD.index(x)][1][ii] = self.AFD[i][1][ii]


        for x in remove:
            self.AFD.remove(x)

    """
    Esta es la funcion madre para el sistema de AFN a AFD, aqui se crea la tabla de transiciones, depende completamente de los indices de las listas
    de los valores de simbolos y estados.

    Tambien se llaman otras funciones como la de defineAFD o modifyStructure, entre otras.
    """
    def toAFD(self):
        self.createMatrix()
        self.transitionTable = [[None for _ in range(len(self.symbols))] for _ in range(len(self.states))]


        for _ in range(len(self.transitions)):

            startStatus = self.transitions[_][0]
            transition = self.transitions[_][1]
            endStatus = self.transitions[_][2]

            if transition == "&":
                endStatus = self.find3scope(endStatus, transitions=[])
                #endStatus.append(startStatus)

            if type(endStatus) is list:
                endStatus = sorted(endStatus)

            symbolIndex = self.symbols.index(transition)
            statusIndex = self.states.index(startStatus)
            if self.transitionTable[statusIndex][symbolIndex] is None:
                self.transitionTable[statusIndex][symbolIndex] = endStatus
            else:
                if type(endStatus) is list:
                    for i in endStatus:
                        if i not in self.transitionTable[statusIndex][symbolIndex]:
                            self.transitionTable[statusIndex][symbolIndex] += endStatus
                else:
                    self.transitionTable[statusIndex][symbolIndex] += endStatus
        self.defineAFD()
        self.cleanAFD()


        newAcceptance = []

        for x in self.AFD:
            for i in self.acceptance:
                if i in x[0] or i == self.acceptance:
                    newAcceptance.append(x[0])



        self.acceptance = newAcceptance
        self.modifyStateStructure()

        newStates = []
        newTransitions = []
        for x in self.AFD:
            newStates.append(x[0])
            for i in self.symbols:
                if i != '&' and i != None:
                    newTransitions.append((x[0], i, x[1][self.symbols.index(i)]))
                else:
                    for ii in self.symbols:
                        if ii != '&' and ii != None and (x[0], ii, x[1][self.symbols.index(ii)]) not in newTransitions:
                            newTransitions.append((x[0], ii, x[1][self.symbols.index(ii)]))

        self.transitions = list(set(newTransitions))
        self.states = list(set(newStates))

        lastreceive = []
        while True:
            clean_transitions = list(filter(lambda t: t[0] != t[2], self.transitions))
            receive = list(set([t[2] for t in clean_transitions]))
            receive = list(filter(lambda r: r != None, receive))
            self.transitions = list(filter(lambda t: (t[0] in receive or t[0] in self.start) and t[2] != None, self.transitions ))
            self.states = list(filter(lambda t: t in receive or t in self.start, self.states ))
            if len(lastreceive) == 0:
                lastreceive.append(len(receive))
            else:
                if lastreceive[-1] == len(receive):
                    break
                lastreceive.append(len(receive))
        #self.writeTxt('respuestas/Conversion_AFN_AFD.txt', self.states, self.symbols, self.start, self.acceptance,
        #              self.transitions, 'conversion')

    """
    Ahora, para trabajar de forma mas ordenada se deben cambiar todos los esados a un mismo formato, en este caso decidimos SX
    se debe determinar si contiene epsilon o no, pues la forma de trabajar es distinta dependiendo del escenario y luego se
    """
    def modifyStateStructure(self):
        prefix = 'S'
        index = 0
        for x in range(len(self.AFD)):
            state = self.AFD[x][0]
            if state in self.acceptance:
                self.acceptance[self.acceptance.index(state)] = prefix + str(index)

            if state == self.start:
                self.start = [prefix + str(index)]

            for i in range(len(self.AFD)):
                for ii in range(len(self.AFD[i][1])):
                    if self.AFD[i][1][ii] is not None and self.AFD[x][0] is not None and sorted(self.AFD[i][1][ii]) == sorted(self.AFD[x][0]):
                        self.AFD[i][1][ii] = prefix + str(index)

                    if type(self.AFD[i][1][ii]) != list and len(self.AFD[x][0]) == 1 and self.AFD[i][1][ii] == \
                            self.AFD[x][0][0]:
                        self.AFD[i][1][ii] = prefix + str(index)

            self.AFD[x][0] = prefix + str(index)

            index += 1

    """
    Funcion que se encarga de realizar o partir los grupos dependiendo a cual correspondan.
    """
    def setMaker(self, dict):

        statesSets, u_vals = [], []
        for i in range(len(list(dict.items()))):
            sT = list(dict.items())[i]  # sT => Tuple of state and its transitions
            statesSets.append(list(sT))
            u_vals.append(list(sT[1]))

        # r_vals => repeated values
        # u_vals => unique values (r_vals)
        r_vals = list(set([tuple(t) for t in u_vals]))
        r_vals = [list(t) for t in r_vals]

        result = []
        for value in r_vals:
            new_group = [lst[0] for lst in statesSets if lst[1] == value and len(lst[1]) > 1]
            if len(new_group) > 0:
                result.append(new_group)

        return result


    """
    Esta funcion tiene el objetivo de realizar de establecer a que grupo corresponde cada estado y con ello poder hacer la
    particion de grupos posteriormente.
    """
    def grouping(self, subGroups, nonAccepting, symbols, transitions):

        newGroups = []
        dict = {key: [] for key in nonAccepting}

        for group in subGroups:
            if len(group) == 1: continue
            for indx in range(len(group)):
                for sym in symbols:
                    for t in transitions:
                        if group[indx] == t[0] and sym == t[1]:
                            if t[2] in group and group[indx] in dict.keys():
                                #print(dict)
                                dict[group[indx]] += [subGroups.index(group)]
                            else:
                                for grp in subGroups:
                                    if t[2] in grp and group[indx] in dict.keys():
                                        #print(dict)
                                        dict[group[indx]] += [subGroups.index(grp)]
        #print(subGroups)
        for subSet in self.setMaker(dict):
            newGroups.append(subSet)

        for group in subGroups:
            for state in group:
                if state not in [state for group in newGroups for state in group]:
                    newGroups.append(group)

        return newGroups


    """
    Esta funcion se encarga de hacer la particion de grupos hasta que se cumpla condicion en la cual la particion de grupos
    no tenga ningún cambio y para el while loop. Obteniendo de esta forma la particion de grupos.
    """
    def partition(self):
        # Start with initial partition accepting and non-accepting states
        accepting = self.acceptance
        acc = []
        for a in accepting:
            if len(acc) == 0:
                acc.append([a])
            else:
                found = False
                for a2 in acc:
                    transitions_satisfied = list(filter(lambda x: x[0] in a2,self.transitions))
                    state_transitions = list(filter(lambda x: x[0] == a,self.transitions))
                    state_symbols = [t[1] for t in state_transitions]
                    flag = False
                    for t in transitions_satisfied:
                        if t[1] in state_symbols:
                            flag = True
                    if flag == False:
                        acc[acc.index(a2)].append(a)
                        found = True
                if found == False:
                    acc.append([a])


        nonAccepting = [i for i in self.states if i not in accepting]

        # Making subsets
        subSets = []
        for a in acc:
            subSets.append(a)
        subSets.append(nonAccepting)

        """ ind = 0
        for s in subSets:
            for s1 in s:
                for s2 in s:
                    if s1 != s2:
                        remove = False
                        for t in self.transitions:
                            if t[0] == s1 and t[2] == s2 and not remove:
                                added = False
                                for s3 in subSets:
                                    if s3 != s and s3[0] not in self.acceptance and added == False and s2 not in s3 and subSets.index(s3) > ind:
                                        subSets[subSets.index(s3)].append(s2)
                                        subSets[subSets.index(s)].remove(s2)
                                        print(subSets)
                                        remove = True
                                        added = True
                                if not added:
                                    subSets.append([s2])
                                    subSets[subSets.index(s)].remove(s2)
                                    remove = True
            ind+= 1 """
        print(subSets)
        bandera = True
        while bandera:
            prevGroups = subSets
            prevSyms = nonAccepting
            subSets = self.grouping(subSets, prevSyms, self.symbols, self.transitions)

            #print(sorted(prevGroups),sorted(subSets))

            if sorted(prevGroups) == sorted(subSets):
                bandera = False

        newSD = {key: [] for key in range(len(subSets))}

        for indx in range(len(subSets)):
            newSD[indx] += subSets[indx]

        for indx in range(len(newSD.keys())):
            lastSVal = self.states[-1][-1]
            newVal = int(lastSVal) + indx + 1
            newState = 'S' + str(newVal)
            newSD[newState] = newSD.pop(indx)
        return newSD
    
    def min(self):
        # Creamos una tabla de equivalencia para los estados
        states = sorted(self.states)
        acceptance = self.acceptance
        transitions = self.transitions
        symbols = self.symbols
        start = self.start
        
        table = [[False for x in states] for i in states]

        for i in range(0,len(states)):
            for j in range(i+1,len(states)):
                des = 0
                des += 1 if states[i] in acceptance else 0
                des += 1 if states[j] in acceptance else 0
                if des == 1:
                    table[i][j] = True

        while True:
            new_table = [x.copy() for x in table]

            for i in range(0,len(states)):
                for j in range(i+1,len(states)):
                    if not new_table[i][j]:
                        for s in symbols:
                            t = [x[2] for x in list(filter(lambda x: (x[0] == states[i] or x[0] == states[j]) and x[1] == s, transitions))]
                            t = sorted(t)
                            print(t)
                            if len(t) == 2:
                                indexes = []
                                indexes.append(states.index(t[0]))
                                indexes.append(states.index(t[1]))
                                indexes.sort()
                                if indexes[1] > indexes[0] and new_table[indexes[0]][indexes[1]]:
                                    new_table[i][j] = True
            if new_table != table:
                table = [x.copy() for x in new_table]
            else:
                break
        equiv = []
        
        for i in range(0,len(states)):
                e = [states[i]]
                for j in range(i+1,len(states)):
                    if not new_table[i][j]:
                        e.append(states[j])
                if len(e)>1:
                    equiv.append(e)
        equiv.sort(key=len)
    
        # Recorrer las sublistas y eliminar los subconjuntos
        for i in range(len(equiv)-1):
            for j in range(i+1, len(equiv)):
                if set(equiv[i]).issubset(set(equiv[j])):
                    equiv[i] = []
                    break
        
        # Devolver la equiv sin los subconjuntos
        equiv = [subequiv for subequiv in equiv if subequiv]


        ind = 0
        for eq in equiv:
            new_state = "eq"+str(ind)
            states.append(new_state)
            for s in eq:
                for t in transitions:
                    if t[0] in s and t[2] not in s:
                        transitions.append((new_state,t[1],t[2]))
                    elif t[2] in s and t[0] not in s:
                        transitions.append((t[0],t[1],new_state))
                    elif t[2] in s and t[0] in s:
                        transitions.append((new_state,t[1],new_state))
                transitions = list(filter(lambda t: t[0] != s and t[2] != s, transitions))
                if s in acceptance:
                    acceptance.remove(s)
                    acceptance.append(new_state)
                if s in start:
                    start.remove(s)
                    start.append(new_state)
                states.remove(s)
            ind += 1
        #self.transitions = list(set(transitions))
        #self.acceptance = list(set(acceptance))
        #self.start = list(set(start))
        #self.states = list(set(states))

        


    def simulate_afd(self, word):
        acceptance = False
        state = self.start[0]
        for char in word:
            # Find a possible transition
            if char not in self.symbols:
                return False
            flag = False
            for t in self.transitions:
                if t[0] == state and t[1] == char and t[2] is not None:
                    # found a transition - go to the next state
                    state = t[2]
                    flag = True
                    break

            if flag == False:
                return False
        if self.acceptance.count(state) > 0:
            acceptance = True

        return acceptance
    
    def simulate_afn(self, word):
        self.createMatrix()
        s = self.e_closure(self.start[0])
        for char in word:
            s = self.e_closures(self.move(s, char))
        for state in s:
            if self.acceptance.count(state) > 0: return True
        return False

    def minimizeAFD(self, statesD):
        # Replacing states in list by new states
        newStates = []  # Creating new states list
        for k, v in statesD.items():
            newStates.append(k)

        # Replacing by new start state
        newStart = []  # Creating new start list
        for k, v in statesD.items():
            if self.start[0] in v:
                newStart.append(k)

        #Verifying states 
        newSyms = []
        for sym in self.symbols:
            if (sym == '&'): continue 
            newSyms.append(sym)

        # Creating new aceptance list
        newAcceptance = []
        for element in self.acceptance:
            newAcceptance.append(element)

        # Replacing new acceptance states
        for k, v in statesD.items():
            for indx in range(len(newAcceptance)):
                if newAcceptance[indx] in v:
                    newAcceptance[indx] = k
        newAcceptance = list(dict.fromkeys(newAcceptance))  # In case elements are duplicated

        # Creating new transition list
        newTransitions = []
        for element in self.transitions:
            if(element[2] == None): continue
            newTransitions.append(element)

        # Converting lists to tuples
        cList = [list(i) for i in newTransitions]

        # Replacing new states in transitions list
        for transition in cList:
            for k, v in statesD.items():
                if transition[0] in v:
                    if transition[2] == None: continue
                    transition[0] = k
                if transition[2] in v:
                    if transition[2] == None: continue
                    transition[2] = k

        # Removing duplicates
        noDuplicatesList = sorted(set(tuple(l) for l in cList))
        newTransitions = noDuplicatesList

        #self.writeTxt('respuestas/Minimizacion_AFD.txt', newStates, newSyms, newStart, newAcceptance,
        #              newTransitions, 'mini', statesD)
        
        self.states = newStates
        self.symbols = newSyms
        self.start = newStart
        self.acceptance = newAcceptance
        self. transitions = newTransitions