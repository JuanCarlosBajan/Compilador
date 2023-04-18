import pickle

class LexAnalyzer:

    def __init__(self, variables_file, actions_file):

        with open(variables_file, "rb") as f:
            self.variables = pickle.load(f)
        with open(actions_file, "rb") as f:
            self.actions = pickle.load(f)
        print(self.variables)
        self.table = []

    def mannage_expression(self, line, line_index, start, end):
        found_token = False
        #print(line[start:end])
        for token in self.variables.keys():
            if self.variables[token].simulate_afd(line[start:end]):
                found_token = True
                self.table.append([token,line_index, line[start:end]])
                break
        if not found_token:
            print("No se encontro token para la expresion '" + line[start:end] +"' ")

    def analyze_code(self, file):
        content = ""
        errors = []

        with open(file, "r") as file:
            content = file.read()
            content = content.split("\n")

        for li in range(0,len(content)):
            open_string = False
            start_index = -1
            end_index = -1
            content[li] = content[li] + " "
            line = content[li]
            line = line.replace("+", "/-")
            for ci in range(0,len(content[li])):
                if line[ci] == "(" and not open_string:
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
                    end_index = ci

        for x in self.table:
            print(x)

                

        