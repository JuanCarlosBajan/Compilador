import re
from regex import Regex
from automata import Automata
import networkx as nx
import matplotlib.pyplot as plt


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
        node_colors = []
        for state in automataFromRegex.states:
            G.add_node(state)
            if state in automataFromRegex.start:
                node_colors.append('yellow')
            elif state in automataFromRegex.acceptance:
                node_colors.append('red')
            else:
                node_colors.append('blue')
        for transition in automataFromRegex.transitions:
            G.add_edge(transition[0], transition[2], label = transition[1])

        pos = nx.planar_layout(G)
        nx.draw(G, pos, with_labels=True,node_color=node_colors)
        labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        plt.show()
            
    except re.error:
        print('La expresión regular es inválida')




options()


