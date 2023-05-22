import pickle

class LexAnalyzer:

    def __init__(self, tokenizer_file, grammar):

        with open(tokenizer_file, "rb") as f:
            result = pickle.load(f)
            self.variables = result['variables']
            self.actions = result['actions']

        with open(grammar, "rb") as f:
            self.grammar = pickle.load(f)

            self.build_action_ira_table()

        self.table = []

        for token in self.actions.keys():
            if self.actions[token] not in self.grammar['tokens'] and self.actions[token] not in self.grammar['ignores']:
                print('El token ' + token + ' No se ha encontrado en la gramatica')
    
    def compute_follows(self):
        grammar = self.grammar['productions']
        nonterminals = []
        for production in grammar:
            nonterminals.append(production[0])

        follows = {}
        for nonterminal in nonterminals:
            follows[nonterminal] = set()

        follows[grammar[0][0]].add('$')

        for nonterminal in nonterminals:
            for production in grammar:
                if nonterminal in production[1]:
                    i = production[1].index(nonterminal)
                    if i == len(production[1]) - 1:
                        if nonterminal != production[0]:
                            follows[nonterminal] |= follows[production[0]]
                    else:
                        next_symbol = production[1][i+1]
                        if next_symbol in nonterminals:
                            follows[nonterminal] |= self.compute_firsts(grammar, [next_symbol])
                        else:
                            follows[nonterminal].add(next_symbol)


        return follows
    
    def compute_firsts(self, grammar, symbols):
        nonterminals = set()
        for production in grammar:
            nonterminals.add(production[0])

        firsts = set()

        for symbol in symbols:
            if symbol not in nonterminals:
                firsts.add(symbol)
                break
            for production in grammar:
                if production[0] == symbol:
                    if production[1][0] not in nonterminals:
                        firsts.add(production[1][0])
                    else:
                        firsts |= self.compute_firsts(grammar, [production[1][0]])
        return firsts


    def compute_all_firsts(self):
        productions = self.grammar['productions']
        grammar = {'start': productions[0][0], 'productions': productions}
        nonterminals = set()
        for production in grammar['productions']:
            nonterminals.add(production[0])

        firsts = {}
        for nonterminal in nonterminals:
            firsts[nonterminal] = set()

        changed = True
        while changed:
            changed = False
            for nonterminal in nonterminals:
                for production in grammar['productions']:
                    if production[0] == nonterminal:
                        symbols = production[1]
                        i = 0
                        while i < len(symbols):
                            symbol = symbols[i]
                            if symbol not in nonterminals:
                                if symbol not in firsts[nonterminal]:
                                    firsts[nonterminal].add(symbol)
                                    changed = True
                                break
                            else:
                                for f in firsts[symbol]:
                                    if f not in firsts[nonterminal]:
                                        firsts[nonterminal].add(f)
                                        changed = True
                                if i == len(symbols) - 1 and '' in firsts[symbol] and '' not in firsts[nonterminal]:
                                    firsts[nonterminal].add('')
                                    changed = True
                            if '' not in firsts[symbol]:
                                break
                            i += 1

        return firsts



    def simulate_afd(self, automata, word):
        for state in automata['start']:
            for char in word:
                if char not in automata['symbols']:
                    return False
                flag = False
                for t in automata['transitions']:
                    if t[0] == state and t[1] == char and t[2] is not None:
                        state = t[2]
                        flag = True
                        break

                if flag == False:
                    return False
            if automata['acceptance'].count(state) > 0:
                return True
        return False
    
    def build_action_ira_table(self):
        follows = self.compute_follows()
        names = [state['name'] for state in self.grammar['lr0']['states']]

        tokens = self.grammar['tokens']
        ignores = self.grammar['ignores']
        productions = self.grammar['productions']

        terminals = [x for x in tokens if x not in ignores]

        nonterminals = []
        for production in self.grammar['productions']:
            if production[0] not in nonterminals:
                nonterminals.append(production[0])
        
        nonterminals = list(nonterminals)

        terminals.append('$')

        action = [[None for value in terminals] for state in self.grammar['lr0']['states']]
        ir_a = [[None for value in nonterminals] for state in self.grammar['lr0']['states']]

        reduce_states = []
        for state in self.grammar['lr0']['states']:
            found_point_in_last = False
            expression_found = ()
            for exp in state['heart']:
                if exp[1][-1] == '~' and "'" not in list(exp[0]):
                    found_point_in_last = True
                    expression_found = exp
                if exp[1][-1] == '~' and "'" in list(exp[0]) and (state['name'],"acc",state['name']) not in self.grammar['lr0']['transitions']:
                    self.grammar['lr0']['transitions'].append((state['name'],"acc",state['name']))
            
            if found_point_in_last:
                reduce_states.append((expression_found, state))

        for state in reduce_states:
            state_index = names.index(state[1]['name'])

            curr_prod = (state[0][0],tuple([value for value in state[0][1] if value != "~"]))

            follow_elements = list(follows[state[0][0]])
            for f_e in follow_elements:
                if action[state_index][terminals.index(f_e)] is not None:
                    if action[state_index][terminals.index(f_e)][0:1] == "r":
                        print("Conflico Reduccion Reduccion en el estado " + str(state_index) + " y terminal " + f_e)
                    else:
                        print("Conflico Siguiente Reduccion en el estado " + str(state_index) + " y terminal " + f_e)
                action[state_index][terminals.index(f_e)] = "r" + str(productions.index(curr_prod)+1)


        for transition in self.grammar['lr0']['transitions']:
            if transition[1] in terminals:
                if action[names.index(transition[0])][terminals.index(transition[1])] is not None:
                    if action[names.index(transition[0])][terminals.index(transition[1])][0:1] == "r":
                        print("Conflico Reduccion Siguiente en el estado " + str(state_index) + " y terminal " + f_e)
                    else:
                        print("Conflico Siguiente Siguiente en el estado " + str(state_index) + " y terminal " + f_e)
                action[names.index(transition[0])][terminals.index(transition[1])] = "s" + str(names.index(transition[2]))
            if transition[1] in nonterminals:
                if ir_a[names.index(transition[0])][nonterminals.index(transition[1])] is not None:
                    print("conflicto de transicion en IR A con el estado " + str(transition[0]) + " y no terminal " + str(transition[1]))
                ir_a[names.index(transition[0])][nonterminals.index(transition[1])] = str(names.index(transition[2]))
            if transition[1] == "acc":
                action[names.index(transition[0])][terminals.index("$")] = "acc"

        self.names = names
        self.nonterminals = nonterminals
        self.terminals = terminals
        self.productions = productions
        self.action = action
        self.ir_a = ir_a


    def analyze_code(self, file):
        content = ""
        errors = []

        with open(file, "r") as file:
            content = file.read()

        content = content.replace("+", "/-")
        content = content.replace("*", "/x")
        content = content.replace(" ", "/s")
        content = content.replace("\n", "/n")

        current_index = 0
        not_found_token = ''
        not_found_token_list = []

        pila = [0]
        simbolos = []

        while True:
            start_index = current_index
            end_index = -1

            element_to_add = []
            token_found = None

            cont = True

            not_accepted = False


            for end in range(start_index,len(content)):
                for token in list(reversed(self.variables.keys())):
                    if end < len(content)-1 and self.simulate_afd(self.variables[token],content[start_index:end+1]):
                        end_index = end
                        token_found = token
                        element_to_add = {'name':token, 'content': content[start_index:end+1]}
                    if end == len(content)-1 and self.simulate_afd(self.variables[token],content[start_index:]):
                        end_index = end
                        token_found = token
                        element_to_add = {'name': token, 'content': content[start_index:]}
                
            if end_index == -1:
                not_found_token += content[current_index]
                cont = False
                if current_index == len(content)-1:
                    not_found_token_list.append(not_found_token)
                    print("el token " + not_found_token + " no se ha encontrado en el sistema, ignorando...")
                    cont = True
                    end_index = len(content)-1
                else:
                    current_index += 1

            if cont:

                if not_found_token != '' and current_index < len(content)-1:
                    not_found_token_list.append(not_found_token)
                    print("el token " + not_found_token + " no se ha encontrado en el sistema, ignorando...")
                    not_found_token = ''

                
                if token_found in self.actions.keys():
                    self.table.append(element_to_add)
                    tok = self.actions[token_found]
                    if tok not in self.grammar['tokens']:
                        print('El token ' + tok + ' no se ha encontrado en el analizador lexico mas no en el analizador sintactico')
                    
                    else:
                        if tok not in self.grammar['ignores']:
                            while True:
                                #print(pila[-1],self.terminals.index(tok))
                                el = self.action[pila[-1]][self.terminals.index(tok)]
                                #print(el)
                                if el is not None:
                                    if el[:1] == 's':
                                        pila.append(int(el[1:]))
                                        simbolos.append(tok)
                                        #print(pila)
                                        #print(simbolos)
                                        break
                                    if el[:1] == 'r':
                                        for val in self.productions[int(el[1:])-1][1]:
                                            pila.pop()
                                            simbolos.pop()
                                        simbolos.append(self.productions[int(el[1:])-1][0])
                                        pila.append(int(self.ir_a[pila[-1]][self.nonterminals.index(simbolos[-1])]))
                                        #print(pila)
                                        #print(simbolos)
                                else:
                                    print("CADENA NO ACEPTADA D:")
                                    not_accepted = True
                                    break

                if not_accepted:
                    break

                elif token_found is not None and token_found not in self.actions.keys() and token_found not in self.grammar['tokens']:
                    print('El token ' + token_found + ' no posee accion y no se encuentra en el analizador sintactico')

                if end_index == len(content)-1:
                    tok = "$"
                    while True:
                        #print(pila[-1],self.terminals.index(tok))
                        el = self.action[pila[-1]][self.terminals.index(tok)]
                        #print(el)
                        if el is not None:
                            if el[:1] == 's':
                                pila.append(int(el[1:]))
                                simbolos.append(tok)
                                #print(pila)
                                #print(simbolos)
                                break
                            elif el[:1] == 'r':
                                for val in self.productions[int(el[1:])-1][1]:
                                    pila.pop()
                                    simbolos.pop()
                                simbolos.append(self.productions[int(el[1:])-1][0])
                                pila.append(int(self.ir_a[pila[-1]][self.nonterminals.index(simbolos[-1])]))
                                #print(pila)
                                #print(simbolos)
                            elif el == "acc":
                                print("CADENA ACEPTADA YEY!!!!")
                                break
                        else:
                            print("CADENA NO ACEPTADA D:")
                            break
                    break

                current_index = end_index+1

        with open('tokens.txt', 'w') as f:
            for elemento in self.table:
                f.write(str(elemento) + '\n')
                

analyzer = LexAnalyzer("tokenizer.pickle","gramatica.pickle")


analyzer.analyze_code(file="code/code.txt")