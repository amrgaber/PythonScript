# Basic Usage
name = "John"
print(f"Hello, {name}!")

# Expressions
x = 10
y = 20
print(f"The sum of {x} and {y} is {x+y}.")

# Precision in Floating Point Numbers
pi = 3.14159
print(f"The value of pi to 2 decimal places is {pi:.2f}.")

# Nested f-strings
print(f"The square of {x} is {f'{x**2}'}")

# Dynamic Expressions with Functions
def greet(name):
    return f" Dear, {name}!"

print(f"{greet(name)} How are you today?")

# Using f-strings with Dictionaries
person = {"name": "John", "age": 30}
print(f"The person's name is {person['name']} and they are {person['age']} years old.")

# Multiline f-strings
print(f"""
The value of x is {x}.
The value of y is {y}.
The sum of x and y is {x+y}.
""")

# Using f-strings with Date and Time
from datetime import datetime
now = datetime.now()
print(f"The current date and time is {now:%Y-%m-%d %H:%M:%S}")

# Using f-strings with Classes
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

person = Person("John", 30)

print(f"The person's name is {person.name} and they are {person.age} years old.")

# Using f-strings with Lists
fruits = ["apple", "banana", "cherry"]
print(f"My favorite fruit is {fruits[0]}.")

# Using f-strings with Tuples
coordinates = (10, 20)
print(f"The coordinates are {coordinates[0]}, {coordinates[1]}.")

# Using f-strings with Sets
unique_numbers = {1, 2, 3, 2, 1}
print(f"The unique numbers are {unique_numbers}.")

# Using f-strings with Boolean Values
is_raining = False
print(f"Is it raining? {is_raining}.")

# Using f-strings with None
nothing = None
print(f"The value of nothing is {nothing}.")