import itertools

class Ticket:
    id_iter = itertools.count()

    def __init__(self, competition_id:int, owner):
        self.id = next(self.id_iter)
        self.owner = owner
        self.cost = 1
        self.competition_id = competition_id
