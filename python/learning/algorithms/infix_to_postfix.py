class Conversion:
    self.output = []
    self.presedence = {'-':1, '+':1, '*':2, '/':2, '^': 3}
    self.stack = []

    def is_operand(self, c):
        return c.isalpha()

    def peek(self):
        return self.stack[-1]

    def infix_to_postfix(self, exp):
        for c in exp:
            # if character is an operand, output it
            if is_operand(c):
                self.output.append(c)
            # If the precedence of the scanned operator is greater than the
            # precedence of the operator in the stack(or the stack is empty
            # or the stack contains a ‘(‘ ), push it.
            else:
                if not self.stack or c == '(':
                    stack.append(c)
                elif self.presedence[c] > self.presedence[self.peek()]:
                    stack.append(c)
            # Else, Pop all the operators from the stack which are greater than
            # or equal to in precedence than that of the scanned operator.
            # After doing that Push the scanned operator to the stack.
            # (If you encounter parenthesis while popping then stop there and
            # push the scanned operator in the stack.)

expression = "a+b*(c^d-e)^(f+g*h)-i"
