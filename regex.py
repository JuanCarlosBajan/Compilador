from node import Node


class Regex:
    def __init__(self, expression):
        errors = self.verify_regex(expression)
        if errors == 0:
            tokens = list(expression)

            for i in range(0,len(tokens)):
                if i<(len(tokens)-1) and tokens[i] not in ['(','|','@'] and tokens[i + 1] not in ['@','*','|',')','+','?']:
                    tokens.insert(i+1,'@')
            self.expression = ''.join(tokens)
        
        else:
            print('La expresión regular ingresada tiene errores')
            self.expression = 'e@r@r@o@r'

    def verify_regex(self, expression):
        tokens = list(expression)
        parenthesis = 0
        errors = 0

        for i in range(0,len(tokens)):
            if i == 0 and tokens[i] in ['*','|',')','+','?']:
                print('Error en la expresión regular ingresada. El operador {} no se está aplicando a ningún símbolo.'.format(tokens[i]))
                errors+=1
            elif tokens[i] in ['*','+','?'] and tokens[i-1] in ['*','|','+','?','(']:
                print('Error en la expresión regular ingresada. El operador {} no se está aplicando a ningún símbolo.'.format(tokens[i]))
                errors+=1

            elif tokens[i] in ['|'] and tokens[i-1] in ['?','|','(']:
                print('Error en la expresión regular ingresada. El operador {} no se está aplicando a ningún símbolo.'.format(tokens[i]))
                errors+=1
            
            elif tokens[i] in [')'] and tokens[i-1] in ['(','|']:
                print('Error en la expresión regular ingresada. Los operadores {}{} no se están aplicando a ningún símbolo.'.format(tokens[i-1],tokens[i]))
                errors+=1

            if tokens[i] in [')']:
                parenthesis-=1
            if tokens[i] in ['(']:
                parenthesis+=1
            
        return errors
        
        if parenthesis != 0:
            print('Error en la expresión regular ingresada. Discrepancia en la cantidad de paréntesis abiertos y cerrados.')
            errors+=1

    def toPosfix(self):
        input = [char for char in self.expression]
        operator_stack = []  # Stack for operators
        output_queue = ""    # Output expression
        # Precedences for the operations
        precedences = {
            "*": 2,
            "@": 1,
            "|": 0,
            "(": -1,
            ")": -1
        }
        # Start Shunting-Yard Algorithm
        for char in input:
            if char not in ["|", "@", "+", "(", ")"]:
                output_queue += char
            elif char in ["|", "@", "+"]:
                while len(operator_stack) > 0:
                    if precedences[operator_stack[0]] < precedences[char]:
                        break
                    output_queue += operator_stack.pop(0)
                operator_stack.insert(0, char)  # Insert the operator at the start of the stack
            elif char == "(":
                operator_stack.insert(0, char)
            elif char == ")":
                while len(operator_stack) > 0:
                    popped_item = operator_stack.pop(0)
                    if popped_item == "(":
                       break
                    output_queue += popped_item
        # Pop all the remaining elements
        while len(operator_stack) > 0:
            output_queue += operator_stack.pop(0)
        return output_queue

    def sintax_tree(self):
        posfix = self.toPosfix()
        tree_stack = [] # Stack to keep the operations
        position = 1
        for item in posfix:
            if item not in ["*", "@", "|"]:
                # It is a character, append to the tree_stack
                tree_stack.insert(0, item)
            elif item in ["*", "@", "|"]:
                if item in ["@", "|"]:
                    rightOperand = tree_stack.pop(0)
                    leftOperand = tree_stack.pop(0)
                    # Create the nodes if the item is a character
                    if not isinstance(leftOperand, Node):
                        leftOperand = Node(value=leftOperand, right_child=None, left_child=None, position=position)
                        leftOperand.first_pos = [position]
                        leftOperand.last_pos = [position]
                        position += 1
                    if not isinstance(rightOperand, Node):
                        rightOperand = Node(value=rightOperand, right_child=None, left_child=None, position=position)
                        rightOperand.first_pos = [position]
                        rightOperand.last_pos = [position]
                        position += 1
                    new_node = Node(left_child=leftOperand, right_child=rightOperand, value=item)
                    leftOperand.root = new_node

                    # If the operator is an union then the first pos is the union of the two childs
                    if item == "|":
                        new_node.first_pos = leftOperand.first_pos + rightOperand.first_pos
                        new_node.last_pos = leftOperand.last_pos + rightOperand.last_pos
                    elif item == "@":
                        new_node.first_pos = leftOperand.first_pos
                        new_node.last_pos = rightOperand.last_pos
                        if leftOperand.nullable():
                            new_node.first_pos = new_node.first_pos + rightOperand.first_pos
                        if rightOperand.nullable():
                            new_node.last_pos = new_node.last_pos +  leftOperand.last_pos


                else:
                    # It is a * only has one middle child
                    operand = tree_stack.pop(0)
                    # Create the nodes if the item is a character
                    if not isinstance(operand, Node):
                        operand = Node(operand, value=rightOperand, position=position)
                        position += 1
                    new_node = Node(middle_child=operand,value=item, left_child=None, right_child=None)
                    new_node.first_pos = operand.first_pos
                    new_node.last_pos = operand.last_pos


                # Add the new node to the tree stack
                tree_stack.insert(0, new_node)

        curr_node = tree_stack[0]
        follow_pos = {}
        visit_queue = [curr_node.left_child]
        visited = []
        for i in range(1, position + 1):
            follow_pos[str(i)] = []

        while len(visit_queue) != 0:
            visit_node = visit_queue.pop()
            if visit_node in visited:
                continue

            if visit_node.middle_child is None:
                if visit_node.left_child is not None and visit_node.left_child.value == "@":
                    for fp in visit_node.left_child.last_pos:
                        for lp in visit_node.right_child.first_pos:
                            follow_pos[str(fp)].append(lp)
            if visit_node.middle_child is not None:
                if visit_node.value == "*":
                    for fp in visit_node.last_pos:
                        for lp in visit_node.first_pos:
                            follow_pos[str(fp)].append(lp)

            if visit_node.single_child and visit_node.middle_child is not None:
                visit_queue.append(visit_node.middle_child)
            elif not visit_node.single_child and visit_node.left_child is not None:
                visit_queue.append(visit_node.left_child)
                visit_queue.append(visit_node.right_child)
            visited.append(visit_node)


        return tree_stack[0]

