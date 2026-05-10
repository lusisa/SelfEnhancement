from ast import Lambda
from typing import TypedDict
from typing import Union
from typing import Optional
from typing import Any

#1. Type Dict is a dictionary that has a fixed set of keys and values
class Movie(TypedDict):
    name : str
    year : int
movie = Movie(name="The Dark Knight", year=2008)
print(movie['name'])

#2. Union is a type that can be one of the types in the union
def square(x: Union[int, float]) -> Union[int, float]:
    return x * x

x = 5 # This is fine because it is an integer
x = 5.0 # This is fine because it is a float
x = "5" # This is not fine because it is a string
x = True # This is not fine because it is a boolean
x = None # This is not fine because it is None
x = [1, 2, 3] # This is not fine because it is a list
x = {1, 2, 3} # This is not fine because it is a set
x = (1, 2, 3) # This is not fine because it is a tuple
x = {1: 2, 3: 4} # This is not fine because it is a dictionary
x = {1: 2, 3: 4} # This is not fine because it is a dictionary

#3. Optional is a type that can be None
# In this case "name" can be either String or None! It cannot be anything else!
def nice_message(name: Optional[str]) -> None:
    if name is None:
        print("Hello, world!")
    else:
        print(f"Hello, {name}!")

#4. Any is a type that can be any type
def print_value(x: Any) -> None:
    print(x)
print_value("I pretend to be Batman in the shower sometimes")

#5. Lambda Function
square = lambda x: x * x
print(square(5))

nums = [1, 2, 3, 4]
# map() is a built-in function that applies a function to each item in a list, and it returns a Iterator.
squares = list(map(lambda x: x * x, nums))
print(squares)


def main():
    print("Hello from proj-impl!")


if __name__ == "__main__":
    main()
