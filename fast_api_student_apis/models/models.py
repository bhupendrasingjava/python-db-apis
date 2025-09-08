from pydantic import BaseModel, EmailStr

class Student(BaseModel):
    roll_number: int
    first_name: str
    last_name: str
    age: int
    email_address: EmailStr

    def __str__(self):
        return f"{self.first_name} {self.last_name} (Roll No: {self.roll_number})"
