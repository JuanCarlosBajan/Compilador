from generador_analizador_sintactico import yapar_reader, build_lr0

tokens, ignores, productions = yapar_reader('./archivos_yapar/slr-2.yalp')
#print(productions)
build_lr0(productions)