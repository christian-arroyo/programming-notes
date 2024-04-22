# A decorator wraps a function, modifying its behavior

def print_hello(name):
    return f"Hello, my name is {name}"


def print_we_are_awesome(name):
    return f"{name} and I are AWESOME!"


def greet_Christian(func):
    return func("Christian")

print(greet_Christian(print_hello))
print(greet_Christian(print_we_are_awesome))

def parent():
    print("Printing from parent")

    def first_child():
        print("Printing from first child")

    def second_child():
        print("Printing from second child")

    second_child()
    first_child()


def decorator(func):
    """Takes a function and returns a function"""
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

def say_whee():
    print("Whee!")

say_whee = decorator(say_whee)
say_whee()
