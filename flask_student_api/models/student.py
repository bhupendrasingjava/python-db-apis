from dataclasses import dataclass

@dataclass
class Student:
    roll_number: int
    first_name: str
    last_name: str
    age: int
    email_address: str

    def __str__(self):
        return f"{self.first_name} {self.last_name} (Roll No: {self.roll_number})"
