import pickle

class LexAnalyzer:

    def __init__(self, tokenizer_file, grammar):

        with open(tokenizer_file, "rb") as f:
            result = pickle.load(f)
            self.variables = result['variables']
            self.actions = result['actions']

        with open(grammar, "rb") as f:
            self.grammar = pickle.load(f)

        self.table = []

        for token in self.actions.keys():
            if self.actions[token] not in self.grammar['tokens'] and self.actions[token] not in self.grammar['ignores']:
                print('El token ' + token + ' No se ha encontrado en la gramatica')

    def simulate_afd(self, automata, word):
        for state in automata['start']:
            for char in word:
                # Find a possible transition
                if char not in automata['symbols']:
                    return False
                flag = False
                for t in automata['transitions']:
                    if t[0] == state and t[1] == char and t[2] is not None:
                        # found a transition - go to the next state
                        state = t[2]
                        flag = True
                        break

                if flag == False:
                    return False
            if automata['acceptance'].count(state) > 0:
                return True
        return False

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
        while True:
            start_index = current_index
            end_index = -1

            element_to_add = []
            token_found = None

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
                current_index += 1

            else:

                if not_found_token != '':
                    not_found_token_list.append(not_found_token)
                    not_found_token = ''

                
                if token_found in self.actions.keys():
                    self.table.append(element_to_add)
                    tok = self.actions[token_found]
                    if tok not in self.grammar['tokens']:
                        print('El token ' + tok + ' no se ha encontrado en el analizador lexico mas no en el analizador sintactico')
                elif token_found not in self.actions.keys() and token_found not in self.grammar['tokens']:
                    print('El token ' + token_found + ' no posee accion y se encuentra en el analizador sintactico')
                if end_index == len(content)-1:
                    break

                current_index = end_index+1

        with open('tokens.txt', 'w') as f:
            for elemento in self.table:
                f.write(str(elemento) + '\n')
                

analyzer = LexAnalyzer("tokenizer.pickle","gramatica.pickle")

analyzer.analyze_code(file="code/code.txt")