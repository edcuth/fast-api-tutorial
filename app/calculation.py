# this is a dummy file used as an intro to pytest

def add(num1: int, num2: int):
    return num1 + num2

class InsufficientFunds(Exception):
    pass

class BankAccount():
    def __init__(self, starting_balance=0):
        self.balance = starting_balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFunds("Not enough funds")
        self.balance -= amount

    def collect_interest(self):
        self.balance *= 1.1
        self.balance = round(self.balance, 2)
