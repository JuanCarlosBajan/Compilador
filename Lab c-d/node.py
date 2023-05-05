class Node:
    first_pos = []
    last_pos = []
    follow_pos = {

    }
    def __init__(self, left_child, right_child,value, middle_child = None, position = None, root = None):
        # In the case that the node only has a middle child assign a boolean to make the calculations easier
        if middle_child is not None:
            self.single_child = True
            self.middle_child = middle_child
            self.left_child = None
            self.right_child = None
        else:
            self.single_child = False
            self.middle_child = None
            self.left_child = left_child
            self.right_child = right_child
        self.value = value
        self.position = position
        self.root = root


    def nullable(self):
        # A node is nullable if
        # It is an union and one of the children is nullable
        if self.value == "|" and (self.left_child.nullable() or self.right_child.nullable()): return True
        # It is a star
        if self.value == "*": return True
        # It is a concatenation and all the children are null
        if self.value == "@" and self.left_child.nullable() and self.right_child.nullable(): return True
        return False


