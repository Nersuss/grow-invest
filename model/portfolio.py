class Portfolio:
    name = ""
    def __init__(self, stocks, user):
        self.stocks = stocks
        self.user = user

    def say_hello(self):
        print("Hello")

class Stock:
    def __init__(self, symbol, quantity, date):
        self.symbol = symbol
        self.quantity = quantity
        self.date = date

    def say_hello(self):
        print("Hello")

class User:
    def __init__(self, email, password, portfolio):
        self.email = email
        self.password = password
        self.portfolio = portfolio

    def say_hello(self):
        print("Hello")
