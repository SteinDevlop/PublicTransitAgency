class Person:
    def __init__(self, name: str, age: int):
        if not name:
            raise ValueError("Name cannot be empty")
        if age < 0:
            raise ValueError("Age cannot be negative")
        
        self.name = name
        self.age = age

    def birthday(self):
        self.age += 1

    def __str__(self):
        return f"{self.name}, {self.age} years old"