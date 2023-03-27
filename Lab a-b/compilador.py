import re
from regex import Regex
from automata import Automata


def menu():
    print('Ingresar regex')

def afn_from_regex():
    print('\nProyecto 1 - Teoría de la computación')
    menu()
    regex = str(input('Ingrese cadena regex: '))

    try:
        regex = Regex(regex)
        automata = Automata(automata_type="afn_from_regex", regex=regex)
        automata.represent_graph()

        cadena = str(input('Ingrese cadena para simular afn :'))
        if automata.simulate_afn(cadena):
            print("Cadena aceptada")
        else:
            print("Cadena no aceptada")
            
    except re.error:
        print('La expresión regular es inválida')

def afd_from_afn_from_regex():
    print('\nProyecto 1 - Teoría de la computación')
    menu()
    regex = str(input('Ingrese cadena regex: '))

    try:
        regex = Regex(regex)
        automata = Automata(automata_type="afd_from_afn_from_regex", regex=regex)
        automata.min()
        automata.represent_graph()
        cadena = str(input('Ingrese cadena para simular afd :'))
        if automata.simulate_afd(cadena):
            print("Cadena aceptada")
        else:
            print("Cadena no aceptada")
            
    except re.error:
        print('La expresión regular es inválida')

def afd_from_regex():
    print('\nProyecto 1 - Teoría de la computación')
    menu()
    regex = str(input('Ingrese cadena regex: '))
    try:
        regex = Regex(regex)
        automata = Automata(automata_type="afd_from_regex", regex=regex)
        automata.represent_graph()

        cadena = str(input('Ingrese cadena para simular afd :'))
        if automata.simulate_afd(cadena):
            print("Cadena aceptada")
        else:
            print("Cadena no aceptada")
    
    except re.error:
        print('La expresión regular es inválida')


afd_from_afn_from_regex()


