import re
from regex import Regex
from automata import Automata
import networkx as nx
import matplotlib.pyplot as plt
from graphviz import Digraph


def menu():
    print('Ingresar regex')

def options():
    print('\nProyecto 1 - Teoría de la computación')
    menu()
    regex = str(input('Ingrese cadena regex: '))

    try:
        regex = Regex(regex)
        automataFromRegex = Automata.fromRegex(regex)
        G = nx.DiGraph()
        dot = Digraph()
        for state in automataFromRegex.states:
            if state in automataFromRegex.start:
                dot.node('start (' + str(state) + ')')
            elif state in automataFromRegex.acceptance:
                dot.node('end (' + str(state) + ')', shape='doublecircle')
            else:
                dot.node(str(state))
        for transition in automataFromRegex.transitions:
            dot.edge('end (' + str(transition[0])+')' if transition[0] in automataFromRegex.acceptance else 'start (' + str(transition[0])+')' if  transition[0] in automataFromRegex.start else str(transition[0]) , 'end (' + str(transition[2])+')' if transition[2] in automataFromRegex.acceptance else 'start (' + str(transition[2])+')' if  transition[2] in automataFromRegex.start else str(transition[2]) , label = transition[1])
            
        dot.render('graph')
            
    except re.error:
        print('La expresión regular es inválida')




options()


