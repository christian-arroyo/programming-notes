from typing import List

def evalRPN(tokens: List[str]) -> int:
    number_stack = []
    for token in tokens:
        if token == '+':
            number_stack.append(number_stack.pop() + number_stack.pop())
        elif token == '-':
            a, b, = number_stack.pop(), number_stack.pop()
            number_stack.append(b - a)
        elif token == '*':
            number_stack.append(number_stack.pop() * number_stack.pop())
        elif token == '/':
            a, b, = number_stack.pop(), number_stack.pop()
            number_stack.append(int(b / a))
        else:
            number_stack.append(int(token))
    return number_stack.pop()

# tokens = ["10","6","9","3","+","-11","*","/","*","17","+","5","+"]
tokens = ["10","6","9","3","+","-11","*","/","*","17","+","5","+"]


print(evalRPN(tokens))
