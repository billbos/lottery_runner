import abc
import itertools
import random
from .participant import Participant
from .ticket import Ticket

class Lottery(metaclass=abc.ABCMeta):
    id_iter = itertools.count()

    def __init__(self, creator:Participant, state:str) -> None:
        self.id = next(self.id_iter)
        self.creator = creator
        self.tickets = []
        self.participants = {}
        self.price_pool = 0
        self.state = 'open'

    @abc.abstractmethod
    def create_ticket(self):
        pass

    def print_info(self):
        print('Lottery-{}, number of participants {}, number of tickets sold {}, created by {}'.format(self.id, len(self.participants), len(self.tickets), self.creator.name))


class BalancedLottery(Lottery):

    def __init__(self, creator:Participant, state:str='running'):
        super().__init__(creator, state)

    def create_tickets(self, num_tickets:int,owner_id:int, weight:int=1, price:int=1) -> Ticket:
        tickets = []
        for i in range(0, num_tickets):
            tickets.append(self.create_ticket(owner_id, weight, price))
        return tickets
    
    def create_ticket(self, owner_id:int, weight:int=1, price:int=1) -> Ticket:
        ticket = Ticket(self.id, owner_id)
        self.price_pool += price
        self.participants.setdefault(owner_id, [])
        self.participants[owner_id].append(ticket)
        for i in range(0, weight):
            self.tickets.append(ticket)
        return ticket

    def resolve_lottery(self) -> int:
        if len(self.participants.keys()) < len(self.tickets):
            self.state = 'finished'
            random.shuffle(self.tickets)
            winner_ticket = self.tickets[0]
            price_pool = self.price_pool
            self.price_pool = 0
            return winner_ticket.owner, price_pool
        else:
            print('Need to sell more tickets first.')
            return -1, 0

class MissingShuffleLottery(Lottery):

    def __init__(self, creator:Participant, state:str='running'):
        super().__init__(creator, state)

    def create_tickets(self, num_tickets:int,owner_id:int, weight:int=1, price:int=1) -> Ticket:
        tickets = []
        for i in range(0, num_tickets):
            tickets.append(self.create_ticket(owner_id, weight, price))
        return tickets
    
    def create_ticket(self, owner_id:int, weight:int=1, price:int=1) -> Ticket:
        ticket = Ticket(self.id, owner_id)
        self.price_pool += price
        self.participants.setdefault(owner_id, [])
        self.participants[owner_id].append(ticket)
        for i in range(0, weight):
            self.tickets.append(ticket)
        return ticket

    def resolve_lottery(self) -> int:
        # forget to shuffle
        if len(self.participants.keys()) < len(self.tickets):
            self.state = 'finished'
            winner_ticket = self.tickets[0]
            price_pool = self.price_pool
            self.price_pool = 0
            return winner_ticket.owner, price_pool
        else:
            print('Need to sell more tickets first.')
            return -1, 0

class CreatingWrongNumberTicketsLottery(Lottery):

    def __init__(self, creator:Participant, state:str='running'):
        super().__init__(creator, state)

    def create_tickets(self, num_tickets:int,owner_id:int, weight:int=1, price:int=1) -> Ticket:
        tickets = []
        for i in range(0, num_tickets):
            tickets.append(self.create_ticket(owner_id, weight, price))
        return tickets
    
    def create_ticket(self, owner_id:int, weight:int=1, price:int=1) -> Ticket:
        ticket = Ticket(self.id, owner_id)
        self.price_pool += price
        self.participants.setdefault(owner_id, [])
        self.participants[owner_id].append(ticket)
        for i in range(0, weight):
            self.tickets.append(ticket)
        return ticket

    def resolve_lottery(self) -> int:
        # forget to shuffle
        if len(self.participants.keys()) < len(self.tickets):
            self.state = 'finished'
            winner_ticket = self.tickets[0]
            price_pool = self.price_pool
            self.price_pool = 0
            return winner_ticket.owner, price_pool
        else:
            print('Need to sell more tickets first.')
            return -1, 0