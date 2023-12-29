from abc import ABC
from datetime import date


class User(ABC):
    def __init__(self, first_name: str, last_name: str, address: str, email: str, date_of_birth: date, pass_hash: str, phone_number: str, id: int, ):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.email = email
        self.date_of_birth = date_of_birth
        self.pass_hash = last_name
        self.phone_number = last_name
        self.id = id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self) :
        return str(self.id)




class Customer(User):
    pass


class Staff(User):
    pass


class Admin(User):
    pass


class Manager(User):
    pass
