import pickle

class LexAnalyzer:

    def __init__(self, variables_file, actions_file):

        with open(variables_file, "rb") as f:
            self.variables = pickle.load(f)
        with open(actions_file, "rb") as f:
            self.actions = pickle.load(f)
        self.table = []

        self.minusculas = ['a','b','c','d','e','f','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        self.mayusculas = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        self.numeros = ['0','1','2','3','4','5','6','7','8','9']
        self.sepcials = ['#','$','%','&','']

    def mannage_expression(self, line, line_index, start, end):
        found_token = False
        for token in self.variables.keys():

            if end !=-1 and  self.variables[token].simulate_afd(line[start:end]):
                found_token = True
                self.table.append([token,line_index, line[start:end]])
                if token in self.actions.keys():
                    exec(self.actions[token])
                break
            if end ==-1 and  self.variables[token].simulate_afd(line[start:]):
                found_token = True
                self.table.append([token,line_index, line[start:]])
                if token in self.actions.keys():
                    exec(self.actions[token])
                break
        if not found_token:
            print("No se encontro token para la expresion '" + line[start:end] +"' en la linea " + str(line_index))

    def analyze_code(self, file):
        content = ""
        errors = []

        with open(file, "r") as file:
            content = file.read()
            content = content.split("\n")

        for li in range(0,len(content)):
            open_string = False
            start = -1
            end = -1
            content[li] = content[li] + "  "
            line = content[li]
            line = line.replace("+", "/-")
            line = line.replace("*", "/x")
            line = line.replace(" ", "/s")
            used_index = []
            for ci in range(0,len(content[li])):
                current_index = ci
                found_token = False
                if ci not in used_index:
                    while True:
                        if start == -1:
                            start = current_index
                        
                        found_token = False
                        end = current_index
                        print("'" + line[start:end] + "'")

                        for token in self.variables.keys():
                            if self.variables[token].simulate_afd(line[start:end+1]):
                                found_token = True
                                     
                        
                        if line[start:end] == "" and not found_token:
                            break

                        if end == len(line):
                            self.mannage_expression(line=line, line_index=li, start=start, end=-1)
                            start = -1
                            end = -1
                        
                        if not found_token:
                            self.mannage_expression(line=line, line_index=li, start=start, end=end)
                            start = -1
                            end = -1
                        else:
                            used_index.append(current_index)   
                            current_index += 1


                """ if line[ci] == "(" and not open_string:
                    if start_index >=0 and end_index >=0:
                        self.mannage_expression(line=line, line_index=li, start=start_index, end=end_index+1)
                    start_index = -1
                    end_index = -1
                    self.table.append(["open-parenthesis",li, "("])

                elif line[ci] == ")" and not open_string:
                    if start_index >=0 and end_index >=0:
                        self.mannage_expression(line=line, line_index=li, start=start_index, end=end_index+1)
                    start_index = -1
                    end_index = -1
                    self.table.append(["close-parenthesis",li, ")"])
                
                elif line[ci] == "{" and not open_string:
                    if start_index >=0 and end_index >=0:
                        self.mannage_expression(line=line, line_index=li, start=start_index, end=end_index+1)
                    start_index = -1
                    end_index = -1
                    self.table.append(["open-key",li, "{"])

                elif line[ci] == "}" and not open_string:
                    if start_index >=0 and end_index >=0:
                        self.mannage_expression(line=line, line_index=li, start=start_index, end=end_index+1)
                    start_index = -1
                    end_index = -1
                    self.table.append(["close-key",li, "}"])

                elif line[ci] == " " and not open_string:
                    if start_index >=0 and end_index >=0:
                        self.mannage_expression(line=line, line_index=li, start=start_index, end=end_index+1)
                    start_index = -1
                    end_index = -1
                    self.mannage_expression(line=line, line_index=li, start=start_index, end=end_index+1)
                    self.table.append(["space",li, " "])

                elif line[ci] == "=" and not open_string:
                    if start_index >=0 and end_index >=0:
                        self.mannage_expression(line=line, line_index=li, start=start_index, end=end_index+1)
                    start_index = -1
                    end_index = -1
                    self.table.append(["equal",li, "="])

                elif line[ci] == '"':
                    if not open_string:
                        open_string = True
                    else:
                        open_string = False
                        if start_index >=0 and end_index >=0:
                            self.table.append(["string",li, line[start_index:end_index+1]])
                        start_index = -1
                        end_index = -1
                        
                
                else:
                    if start_index <0:
                        start_index = ci
                    end_index = ci """

            #self.table.append(["newLine",li, "/n"])
        
        
        #for x in self.table:
        #    print(x)

        self.table = [elemento for elemento in self.table if elemento[0] != 'space']

        with open('tokens.txt', 'w') as f:
            for elemento in self.table:
                f.write(str(elemento) + '\n')
                

        