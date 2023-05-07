import graphviz
import pickle

def cerradura(heart, productions, name):
    state=[
        heart,
        []
    ]
    for i in range(0,len(heart)):
        head = heart[i][0]
        body = list(heart[i][1])
        for ii in range(0,len(body)):
            if body[ii] == "~" and ii < len(body)-1:
                for iii in range(0,len(productions)):
                    if body[ii+1] == productions[iii][0] and tuple([productions[iii][0],['~'] + list(productions[iii][1])]) not in state[1]:
                        state[1].append(tuple([productions[iii][0],tuple(['~'] + list(productions[iii][1]))]))

    for prod in state[1]:
        for ii in range(0,len(productions)):
            if prod[1][1] == productions[ii][0] and tuple([productions[ii][0],tuple(['~'] + list(productions[ii][1]))]) not in state[1]:
                state[1].append(tuple([productions[ii][0],tuple(['~'] + list(productions[ii][1]))]))
    return (state[0],tuple(state[1]),name)


def move_point(production):
    sublist = production[1]
    index_punto = sublist.index('~')
    if index_punto < len(sublist) - 1:
        temp = sublist[index_punto]
        sublist[index_punto] = sublist[index_punto + 1]
        sublist[index_punto + 1] = temp
    return (production[0],tuple(production[1]))

def convert_state_string(state):
    string = ''
    for prod in state['heart']:
        string += prod[0] + "->" + ' '.join(prod[1]) + "\n"
    
    if len(state['productions']) > 0:
        string += "----------------------\n"

    for prod in state['productions']:
        string += prod[0] + "->" + ' '.join(prod[1]) + "\n"
    
    return string


def build_lr0(productions):

    dot = graphviz.Digraph()

    dot.graph_attr['rankdir'] = 'LR'

    productions = [(productions[0][0] + "'",(productions[0][0],))] + productions
    
    states = []
    transitions = []
    visited_groups = []
    prefijo = "I"
    index = 0
    
    initial_state = cerradura(((productions[0][0],tuple(['~'] + list(productions[0][1]))),),productions, prefijo+str(index))
    states.append(initial_state)
    visited_groups.append(initial_state[0])
    index += 1
    
    for state in states:
        dicc = {}
        for prod in list(state[1]) + list(state[0]):
            point_index = -1
            for i in range(0,len(prod[1])):
                if prod[1][i] == "~":
                    point_index = i

            if point_index < len(prod[1])-1 and point_index >= 0 and prod[1][point_index+1] not in dicc:
                dicc[prod[1][point_index+1]] = []
            if point_index >= 0 and point_index < len(prod[1])-1:
                dicc[prod[1][point_index+1]].append(prod)

        trans_dest = list(dicc.values())
        trans_op = list(dicc.keys())

        for i in range(0,len(trans_dest)):
            for ii in range(0,len(trans_dest[i])):
                trans_dest[i][ii] = move_point([trans_dest[i][ii][0],list(trans_dest[i][ii][1])])
            new_state = cerradura(tuple(trans_dest[i]), productions, prefijo+str(index))
            if new_state[0] not in visited_groups:
                visited_groups.append(new_state[0])
                states.append(new_state)
                transitions.append((state[2], trans_op[i], new_state[2]))
                index += 1
            else:
                filtrado = [tupla for tupla in states if tupla[0] == new_state[0]]
                if len(filtrado) == 0 or len(filtrado) > 1:
                    print('hmmm algo maloo D:')
                else:
                    transitions.append((state[2],trans_op[i],filtrado[0][2]))

    new_states = []
    for x in states:
        new_states.append({
            "name":x[2],
            "heart":x[0],
            "productions":x[1]
        })

    for d in new_states:
        label = d['name']
        dot.node(label, convert_state_string(d), shape="box", style="rounded")

    for t in transitions:
        dot.edge(t[0],t[2],t[1])

    automata = {
        'states':new_states,
        'transitions': transitions
    }
    dot.render('../digrafos/lr0')

    return automata

def delete_coments(string):
    new_string = ""
    indexes = []
    start_index = -1
    scope = 0
    for i in range(0,len(string)):
        if i<len(string)-2 and string[i] == "/" and string[i+1] == "*":
            start_index = i
            scope += 1
        
        if i<len(string)-1 and string[i] == "*" and string[i+1] == "/":
            scope -= 1
            if scope < 0:
                print("Error de comentarios, se halla un */ antes de un /*")
            elif start_index == -1 and scope == 0:
                print("Error de comentarios, no se halla un /* antes de un */")
            elif start_index != -1 and scope == 0:
                indexes.append([start_index,i+1])
                start_index = -1
    if len(indexes) == 0:
        return string
    for i in range(0,len(indexes)):
        if i == 0:
            if indexes[i][0] >0:
                new_string += string[:indexes[i][0]]
        elif i<len(indexes)-1:
            new_string+=string[indexes[i-1][1]+1:indexes[i][0]]
        elif i ==len(indexes)-1:
            if indexes[i][1] != len(string)-1:
                new_string += string[indexes[i][1]+1:]

    return new_string


def yapar_reader(file):
    contenido = ""
    with open(file, 'r', encoding='utf-8') as archivo:
        contenido = archivo.read()

    contenido = delete_coments(contenido)

    try:
        tokens, productions = contenido.split("%%")
    
    except:
        print("La estructura de Tokens y Producciones es incorrecta")

    tokens = tokens.split(" ")
    for i in range(0,len(tokens)):
        tokens[i] = tokens[i].split("\n")
    
    tokens = [elemento for sublista in tokens for elemento in sublista]

    while '' in tokens:
        tokens.remove('')

        
    ignores = []

    for i in range(0,len(tokens)):
        if tokens[i] == "IGNORE":
            if i == len(tokens)-1:
                break
            index = i+1
            while True and index < len(tokens):
                if tokens[index] != "IGNORE" and tokens[index] != "%token":
                    ignores.append(tokens[index])
                    index+=1
                else:
                    break

    while '%token' in tokens:
        tokens.remove('%token')

    while 'IGNORE' in tokens:
        tokens.remove('IGNORE')

    for i in ignores:
        tokens.remove(i)

    productions = productions.split(";")

    productions = productions[:-1]

    for i in range(0,len(productions)):
        definition = productions[i]
        definition = definition.split(" ")
        for ii in range(0,len(definition)):
            definition[ii] = definition[ii].split("\n")

        definition = [elemento for sublista in definition for elemento in sublista]

        while '' in definition:
            definition.remove('')

        definition = ','.join(definition)

        definition = definition.split(':,')
        definition[1] = definition[1].split(",|,")

        for ii in range(0,len(definition[1])):
            definition[1][ii] = definition[1][ii].split(',')

        productions[i] = definition


    new_productions = []

    for i in range(0,len(productions)):
        for ii in range(0,len(productions[i][1])):
            #print((productions[i][0],tuple(productions[i][1][ii])))
            new_productions.append((productions[i][0],tuple(productions[i][1][ii])))

    productions = new_productions

    automata = build_lr0(productions)

    result = {
        'tokens':tokens,
        'ignores':ignores,
        'productions':productions,
        'lr0':automata
    }

    with open("../gramatica.pickle", "wb") as f:
        pickle.dump(result, f)

## Errores implementados
## Si en la estructura del archivo hay mas de una vex %% es incorrecto pues esto se utiliza para delimitar cuando es el area de tokens y cuando es producciones.
## Errores al momento de eliminar los comentarios del codigo