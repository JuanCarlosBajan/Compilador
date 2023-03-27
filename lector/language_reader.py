from regex import Regex
from automata import Automata

content = ""

def define_regex(expression):
    errors = []
    if len(expression) == 1: ## El hecho que expression sea lista o un string depende de si la definicion regular en el archivo language tenia espacios
        expression = expression[0]
        special_chars = ["[","]","-","#"]
        special_chars_2 = ["*","+","|","?"]
        special_chars_3 = ["(",")"]
        found_special_chars_1 = any(elemento in expression for elemento in special_chars)
        found_special_chars_2 = any(elemento in expression for elemento in special_chars_2)
        found_special_chars_3 = any(elemento in expression for elemento in special_chars_3)
        if found_special_chars_1: ## []-'#

            ## Voy a dejar el # pendiente porque no se como utilizarlo la verdad
            expression = list(expression)
            indexes = []
            for i in range(0,len(expression)):
                indx = [-1,-1]
                if expression[i] == '[':
                    print(i)
                    indx[0] = i
                    for j in range(i,len(expression)):
                        if expression[j] == ']':
                            indx[1] = j
                            break
                    if indx[0] != -1 and indx[1] != -1:
                        indexes.append(indx)
            new_expression_list = []
            if len(indexes)>0:
                min_index = indexes[0][0]
                if min_index >0:
                    new_expression_list.append(expression[0:min_index])

                for i in range(0,len(indexes)):
                    content = expression[indexes[i][0]+1:indexes[i][1]]
                    if "-" in content:
                        pass ##logica para incluir grupos de valores de c1 - c2
                    else:
                        if len(content) >1:
                            new_content = "(" + "(" + content[0] + ")" + "|"
                            for ci in range(1,len(content)):
                                if ci != len(content) -1:
                                    new_content+= "(" + content[ci] + ")" + "|"
                                else:
                                    new_content += "(" + content[ci] + ")" +")"
                        else:
                            new_content = "(" + "(" + content[0] + ")" + ")"
                        new_expression_list.append(new_content)
                        if i+1 < len(indexes):
                            new_expression_list+=expression[indexes[i][1]+1:indexes[i+1][0] if indexes[i+1][0] < len(expression) else len(expression)-1]
                        else:
                            if indexes[i][1]+1 < len(expression):
                                new_expression_list += expression[indexes[i][1]+1:]
            expression = ''.join(new_expression_list)

        if found_special_chars_2: ## *+?|
            expression = list(expression)
            flag = True
            for i in range(0,len(expression)):
                if expression[i] == '"' and flag:
                    expression[i] = "("
                    flag = False
                elif expression[i] == '"' and not flag:
                    expression[i] = ")"
                    flag = True
            expression = ''.join(expression)
            regex = Regex(expression)
            print(regex.expression)
            automata = Automata(automata_type="afd_from_afn_from_regex", regex=regex)
        elif found_special_chars_3: ## ()
            if len(expression) == 3:
                expression = list(expression)
                while '"' in expression:
                    expression.remove('"')
                expression = ''.join(expression)
                ## Creo que esto no le compete al lector de language sino al lector del input
                """ 
                ## Verificacion de errores con respecto a los parentesis
                parenthesis_count = 0
                for char in expression:
                    if char == "(":
                        parenthesis_count += 1
                    if char == ")":
                        parenthesis_count -= 1
                    if parenthesis_count <0:
                        errors.append("El orden de los parentesis es incorrecto")
                if parenthesis_count != 0:
                    errors.append("La cantidad de parentesis no es correcta")

                ## Manejo del token """
                regex = "No regex"
                automata = Automata(automata_type=expression)
            else:
                regex = "No regex ()"
                automata ="No automata ()"
            
        else:
            expression = list(expression)
            while '"' in expression:
                expression.remove('"')
            expression = ''.join(expression)
            regex = Regex(expression)
            automata = Automata(automata_type="afd_from_regex", regex=regex)

        return errors,automata,regex
    else:
        new_expression_list = []
        new_expression_str = ""
        for x in expression:
            new_expression_list.append(define_regex([x])[2].expression)
        
        for x in new_expression_list:
            x=x.replace("@","")
            x=x.replace("#","")
            new_expression_str += "("+x+")"

        regex = Regex(new_expression_str)
        automata = Automata(automata_type="afd_from_regex", regex=regex)
        return errors,automata, regex

with open("language.ml", "r") as file:
    content = file.read()
    content = content.split("\n")

errors = []

while "" in content:
        content.remove("")

for i in range(0,len(content)):
    temporal = content[i].split(" ")

    foundError = False

    while "" in temporal:
        temporal.remove("")

    if len(temporal) < 4:
         errors.append([i,"No se declaró correctamente el token"])
    
    if temporal[0] != "let":
        errors.append([i,"No se declaró correctamente el token (missing let)"])

    if temporal[2] != "=":
        errors.append([i,"No se declaró correctamente el token (missing =)"])
    regex_errors, automata, regex = define_regex(temporal[3:])

    if not foundError and len(regex_errors) == 0:
        temporal = (temporal[1],regex)
        content[i] = temporal

for x in content: print(x)