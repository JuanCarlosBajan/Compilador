from regex import Regex
from automata import Automata



def parenthesis_manager(expression):

    """ Definimos las variables que nos van a funcionar para manejar la identificacion de parentesis """
    expression = list(expression)
    new_expression_list = []
    indexes = []
    parenthesis_stack = 0
    start_idx = -1
    end_idx = -1

    """ Debemos identificar todos los parentesis alcanzables superficialmente,
    para manejar parentesis dentro de parentesis, llamamos a la funcion read_expression.
    
    Cabe resaltar que para encontrar los parentesis superficiales generamos un pseudo_stack 
    donde sumamos y restamos unos."""
    for i in range(0,len(expression)):
        if expression[i] == "(":
            if i in [0,1] or not (i>1 and expression[i-1] == ":" and expression[i-2] == "/"):
                if start_idx == -1:
                    start_idx = i
                parenthesis_stack += 1


        if expression[i] == ")":
            if i in [0,1] or not (i>1 and expression[i-1] == ":" and expression[i-2] == "/"):
                parenthesis_stack -= 1
        
        if parenthesis_stack < 0:
            print("Error en parentesis, se ha encontrado ) antes de un (")
        
        if parenthesis_stack == 0 and start_idx != -1:
            end_idx = i
            
        if start_idx != -1 and end_idx != -1:
            indexes.append([start_idx, end_idx])
            start_idx = -1
            end_idx = -1


    """ En caso llegamos al caso mas atomico simplemente devolvemos la expresion que recibimos """
    if len(indexes) == 0:
        return ''.join(expression)


    """ Claro, puede haber un trozo de expresion regular antes del primer parentesis, entre medias
    de grupos de parentesis o al final luego del ultimo parentesis por lo que debemos manejar 
    tambien esos casos. """
    for i in range(0,len(indexes)):

        if i == 0 and indexes[0][0] > 0:
            new_expression_list += expression[0:indexes[0][0]]
        new_expression_list+= "/:(" + read_expression(''.join(expression[indexes[i][0]+1:indexes[i][1]])) +"/:)"

        if i + 1 < len(indexes):
            new_expression_list += ''.join(expression[indexes[i][1]+1:indexes[i+1][0]])
        
        elif i + 1 == len(indexes):
            new_expression_list += ''.join(expression[indexes[i][1]+1:])
        
    return ''.join(new_expression_list)
        

def concatenation_manager(expression):

    """ Dividimos la expresion en todas las concatenaciones indicadas a traves del espacio. Cabe resaltar
     que, dado que definimos a los parentesis de una importancia mayor, el manejar los parentesis antes que los
    espacios nos permite llevar un buen desarrollo del problema """
    expression = expression.split(" ")
    new_expression_list = []

    """ Por cada sub_expresion encontrada la enviamos a analizar de nuevo a read_expression """
    for sub_exp in expression:
        new_expression_list+= "/:(" + read_expression(sub_exp) + "/:)"

    return ''.join(new_expression_list)

def brackets_content_manager(content):
    content = content.split("'")
    while '' in content:
        content.remove('')

    order = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

    if '-' in content:
        chars = []
        if len(content) > 1:
            for i in range(0,len(content)):
                if '-' == content[i]:
                    start = content[i-1]
                    end = content[i+1]
                    if start not in order or end not in order:
                        print("Uno de los elementos en character-set no es aceptado")
                    else:
                        start_idx = order.index(start)
                        end_idx = order.index(end)
                        chars += order[start_idx:end_idx+1]
        else:
            pass


        new_content = ""
        if len(chars) > 1:
            new_content = "/:(" + chars[0] + "/:)" + "|"
            for ci in range(1,len(chars)):
                if ci != len(chars) -1:
                    new_content+= "/:(" + chars[ci] + "/:)" + "|"
                else:
                    new_content += "/:(" + chars[ci] + "/:)"
        else:
            new_content = "/:(" + chars[0] + "/:)"
        
        content = new_content
    else:
        new_content = ""
        if len(content) > 1:
            new_content = "/:(" + content[0] + "/:)" + "|"
            for ci in range(1,len(content)):
                if ci != len(content) -1:
                    new_content+= "/:(" + content[ci] + "/:)" + "|"
                else:
                    new_content += "/:(" + content[ci] + "/:)"
        else:
            new_content = "/:(" + content[0] + "/:)"
        
        content = new_content

    return ''.join(content)

def brackets_manager(expression):
    expression = list(expression)
    new_expression_list = []
    indexes = []
    brackets_stack = 0
    start_idx = -1
    end_idx = -1

    for i in range(0,len(expression)):
        if expression[i] == "[":
            if start_idx == -1:
                start_idx = i
            brackets_stack += 1

        if expression[i] == "]":
            brackets_stack -= 1
        
        if brackets_stack < 0:
            print("Error en parentesis, se ha encontrado ] antes de un [")
        
        if brackets_stack == 0 and start_idx != -1:
            end_idx = i
            
        if start_idx != -1 and end_idx != -1:
            indexes.append([start_idx, end_idx])
            start_idx = -1
            end_idx = -1

    for i in range(0,len(indexes)):

        if i == 0 and indexes[0][0] > 0:
            new_expression_list += expression[0:indexes[0][0]]
        new_expression_list+= "/:(" + brackets_content_manager(''.join(expression[indexes[i][0]+1:indexes[i][1]])) +"/:)"

        if i + 1 < len(indexes):
            new_expression_list += ''.join(expression[indexes[i][1]+1:indexes[i+1][0]])
        
        elif i + 1 == len(indexes):
            new_expression_list += ''.join(expression[indexes[i][1]+1:])

    return ''.join(new_expression_list)


def quotation_marks_manager(expression):
    expression = list(expression)
    while '"' in expression:
        expression.remove('"')

    while "'" in expression:
        expression.remove("'")

    return ''.join(expression)

variables = {}

def read_expression(expression):


    """ Hallamos la cantidad de parentesis que hay en la expresion """
    p_count = 0
    for char in expression:
        if char in ["(",")"]:
            p_count += 1

    """ Si hay mas de un parentesis llamamos a la funcion que los maneja """
    if p_count > 1:
        expression = parenthesis_manager(expression = expression)

    """ ¿Que pasa si solo se encuentra un parentesis? """
    if p_count == 1:
        """ Manejar UN parentesis """
        pass

    """ ¿Que pasa si hay mas '(' que ')' o viceversa? """
    if p_count != 1 and p_count%2 != 0:
        print("Error de Parentesis, la cantidad de ( y ) difieren")
    
    """ Encontramos la cantidad de espacios que hay en la expresion """
    space_count = 0
    for char in expression:
        if char in [" "]:
            space_count += 1

    """ Si encontramos al menos un espacio en la expresion, lo enviamos a la funcion que los maneja """
    if space_count > 0:
        expression = concatenation_manager(expression = expression)

    bracket_count = 0
    for char in expression:
        if char in ["[","]"]:
            bracket_count += 1
    
    """ Si hay mas de un corchete llamamos a la funcion que los maneja """
    if bracket_count > 1:
        expression = brackets_manager(expression = expression)

    """ ¿Que pasa si solo se encuentra un corchete? """
    if bracket_count == 1:
        print("Error de Corchete, la cantidad de [ y ] difieren")

    is_variable = any(elemento in list(expression) for elemento in ["[","]","(",")","#","*","+","?","'",'"',"^","|"])
    variable = ''.join(expression)
    if not is_variable:
        if variable in variables.keys():
            resp = variables[variable]
            resp = resp.replace("(","/:(")
            resp = resp.replace(")","/:)")
            return resp
        else:
            print("Error de variable, '" + variable + "' no se ha instanciado anteriormente")
            return "error"

    qm_count = 0
    for char in expression:
        if char in ['"',"'"]:
            qm_count += 1

    """ ¿Que pasa si hay mas '(' que ')' o viceversa? """
    if qm_count != 1 and qm_count%2 != 0:
        print('Error de ", la cantidad de " difieren')

    """ Si hay mas de un corchete llamamos a la funcion que los maneja """
    if qm_count > 1 :
        expression = quotation_marks_manager(expression = expression)

    """ ¿Que pasa si solo se encuentra un corchete? """
    if qm_count == 1:
        print('Error de ", la cantidad de "')

    return expression

def reader(file):
    content = ""
    errors = []

    with open(file, "r") as file:
        content = file.read()
        content = content.split("\n")
    
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

        regex = read_expression(' '.join(temporal[3:]))
        regex = regex.replace("/:","")

        if not foundError:
            variables[temporal[1]] = regex
            temporal = (temporal[1],regex)
            content[i] = temporal

        regex = Regex(regex)
        automata = Automata(automata_type="afd_from_afn_from_regex",regex=regex)
        print(automata.simulate_afd("0.01"))

    #for x in content: print(x)