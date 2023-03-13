class Regex:
    def __init__(self, expression):
        errors = self.verify_regex(expression)
        if errors == 0:
            tokens = list(expression)

            size = [i for i in range(0,len(tokens))]
            for i in size:
                if i<(len(tokens)-1) and tokens[i] not in ['(','|','@'] and tokens[i + 1] not in ['@','*','|',')','+','?']:
                    tokens.insert(i+1,'@')
                    size.append(size[-1]+1)
            self.expression = ''.join(tokens)
        
        else:
            print('La expresión regular ingresada tiene errores')
            self.expression = 'e@r@r@o@r'

    def verify_regex(self, expression):
        tokens = list(expression)
        parenthesis = 0
        errors = 0

        for i in range(0,len(tokens)):

            if tokens[i] not in ['*','|',')','+','?','(','&', 'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9']:
                print('Error en la expresión regular ingresada. El operador {} no es aceptado.'.format(tokens[i]))
                errors+=1
            if i == 0 and tokens[i] in ['*','|',')','+','?']:
                print('Error en la expresión regular ingresada. El operador {} no se está aplicando a ningún símbolo.'.format(tokens[i]))
                errors+=1
            elif tokens[i] in ['*','+','?'] and tokens[i-1] in ['*','|','+','?','(']:
                print('Error en la expresión regular ingresada. El operador {} no se está aplicando a ningún símbolo.'.format(tokens[i]))
                errors+=1

            elif tokens[i] in ['|'] and tokens[i-1] in ['?','|','(']:
                print('Error en la expresión regular ingresada. El operador {} no se está aplicando a ningún símbolo.'.format(tokens[i]))
                errors+=1
            
            elif tokens[i] in [')'] and tokens[i-1] in ['(','|']:
                print('Error en la expresión regular ingresada. Los operadores {}{} no se están aplicando a ningún símbolo.'.format(tokens[i-1],tokens[i]))
                errors+=1

            if tokens[i] in [')']:
                parenthesis-=1
            if tokens[i] in ['(']:
                parenthesis+=1
            
        if parenthesis != 0:
            print('Error en la expresión regular ingresada. Discrepancia en la cantidad de paréntesis abiertos y cerrados.')
            errors+=1
        
        return errors

    def toPosfix(self):
        input = [char for char in self.expression]
        operator_stack = []  # Stack for operators
        output_queue = ""    # Output expression
        # Precedences for the operations
        precedences = {
            "*": 2,
            "+": 2,
            "?": 2,
            "@": 1,
            "|": 0,
            "(": -1,
            ")": -1
        }
        # Start Shunting-Yard Algorithm
        for char in input:
            if char not in ["|", "@", "(", ")"]:
                output_queue += char
            elif char in ["|", "@"]:
                while len(operator_stack) > 0:
                    if precedences[operator_stack[0]] < precedences[char]:
                        break
                    output_queue += operator_stack.pop(0)
                operator_stack.insert(0, char)  # Insert the operator at the start of the stack
            elif char == "(":
                operator_stack.insert(0, char)
            elif char == ")":
                while len(operator_stack) > 0:
                    popped_item = operator_stack.pop(0)
                    if popped_item == "(":
                       break
                    output_queue += popped_item
        # Pop all the remaining elements
        while len(operator_stack) > 0:
            output_queue += operator_stack.pop(0)
        return output_queue
    
    def translateIndentities(self):
        expression = list(self.expression)
        # Iteramos sobre cada uno de los caracteres en la expresion regular para encontrar los ? y +
        for char in expression:
            if char in ["?","+"]:
                # Cuando encontramos estos caracteres determinamos los indices del rango de caracteres al que se refiere ese operado
                # pues, al poder referirse a un conjunto de caracteres encerrados dentro de los parentesis, debemos tomar en cuenta ese caso tambien.
                idx = expression.index(char)
                start = idx-1
                end = idx-1
                # Encontramos el rango
                if expression[end] == ")":
                    parenthesis = 1
                    for x in range(1,idx):
                        if expression[end-x] == ")":
                            parenthesis+=1
                        if expression[end-x] == "(":
                            parenthesis-=1
                            if parenthesis == 0:
                                start = end-x
                                break
                # En caso el operador encontrado sea ? debemos convertirlo a un or (elemento | epsilon)
                if char == "?":
                    expression = expression[:start] + ["("] + expression[start:end+1] + ["|"] + ["&"] + [")"] + expression[end+2:]
                # En caso el operador encontrado sea + debemos convertirlo a una cerradura de kleen y concatenacion
                # elemento* elemento
                if char == "+":
                    expression = expression[:start] + expression[start:end+1] +  ["*@"] + expression[start:end+1] + expression[end+2:]

        self.expression = ''.join(expression)

    # En esta funcion centralizamos el funcionamiento de traducir la regex y luego convertirlo a posfix
    def toPostfixIdentity(self, regex_to_afd):
        self.translateIndentities()
        if regex_to_afd:
            self.expression+= "@#"
        print(self.expression)
        return self.toPosfix()
