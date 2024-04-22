import functools

# A decorator wraps a function, modifying its behavior

def print_hello(name):
    return f"Hello, my name is {name}"


def print_we_are_awesome(name):
    return f"{name} and I are AWESOME!"


def greet_Christian(func):
    return func("Christian")

print(greet_Christian(print_hello))
print(greet_Christian(print_we_are_awesome))


def decorator(func):
    """Takes a function and returns a function"""
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

@decorator
def say_whee():
    print("Whee!")

say_whee()


# Decorator with arguments
def do_twice(func):
    # this line allows the wrapped function to preserve its identity
    @functools.wraps(func)
    def wrapper_do_twice(*args, **kwargs):
        func(*args, **kwargs)
        func(*args, **kwargs)
    return wrapper_do_twice

@do_twice
def say_whoo_to_person(name):
    print(f"Hey {name}, whoooooo!")

say_whoo_to_person("Christian")
say_whoo_to_person("Chuy")
