from analizador_lexico import LexAnalyzer

analyzer = LexAnalyzer(variables_file="variables.pickle", actions_file="actions.pickle")

analyzer.analyze_code(file="codeYalex3.txt")