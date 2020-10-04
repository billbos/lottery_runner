import itertools
from .ticket import Ticket
class Participant:
    id_iter = itertools.count()

    def __init__(self, name, balance=100):
        self.id = next(self.id_iter)
        self.balance = balance
        self.lotteries = []
        self.tickets = []
        self.name = name
    
    def purchase_ticket(self, ticket:Ticket):
        self.tickets.append(ticket)
        self.balance -= ticket.cost
    
    def add_price_money(self, reward:int) -> None:
        self.balance += reward
