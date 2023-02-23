class Automata:

    def __init__(self, states=None, symbols=None, start=None, acceptance=None, transitions=None):

        if (states is None or symbols is None or start is None or acceptance is None or transitions is None):
            raise ValueError("Por favor ingresa los valores correctos")
        elif (len(states) < 0 or len(symbols) < 0 or len(start) < 0 or len(acceptance) < 0 or len(transitions) < 0):
            raise ValueError("Por favor ingresa los valores correctos")

        self.states = states
        self.symbols = symbols
        self.start = start
        self.acceptance = acceptance
        self.transitions = transitions

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

    def basic_automata(current_status, operand):
        return Automata(
            states=[f'{current_status}', f'{current_status + 1}'],
            acceptance=[f'{current_status + 1}'],
            symbols=[operand],
            start=[f'{current_status}'],
            transitions=[(f'{current_status}', operand, f'{current_status + 1}')]
        )

    def fromRegex(regex):
        posfixExpression = regex.toPosfix()
        print(f"La expresión postfix es: {posfixExpression}")
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
                        leftOperand = Automata.basic_automata(current_status, leftOperand)
                        current_status += 2
                    if not isinstance(rightOperand, Automata):
                        rightOperand = Automata.basic_automata(current_status, rightOperand)
                        current_status += 1
                    # Create the result Automata
                    result_automata = Automata(
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
                        leftOperand = Automata.basic_automata(current_status, leftOperand)
                        current_status += 2
                    if not isinstance(rightOperand, Automata):
                        rightOperand = Automata.basic_automata(current_status, rightOperand)
                        current_status += 1
                    # Create the result automata
                    current_status += 1
                    start_state = current_status
                    current_status += 1
                    end_state = current_status
                    result_automata = Automata(
                        states=list(dict.fromkeys(leftOperand.states + rightOperand.states)) + [f'{start_state}',
                                                                                                f'{end_state}'],
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
                        operand = Automata.basic_automata(current_status, operand)
                        current_status += 1
                    # Create the result automata
                    current_status += 1
                    start_state = current_status
                    current_status += 1
                    end_state = current_status
                    result_automata = Automata(
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
                        operand = Automata.basic_automata(current_status, operand)
                        current_status += 1
                    current_status += 1
                    start_state = current_status
                    current_status += 1
                    end_state = current_status
                    result_automata = Automata(
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
                        operand = Automata.basic_automata(current_status, operand)
                        current_status += 1
                    current_status += 1
                    start_state = current_status
                    current_status += 1
                    end_state = current_status
                    result_automata = Automata(
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

        stack[0].writeTxt('respuestas/FromRegex_To_AFN.txt', stack[0].states, stack[0].symbols, stack[0].start, stack[0].acceptance,
                      stack[0].transitions, 'FromRegex_To_AFN')

        return stack[0]

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
