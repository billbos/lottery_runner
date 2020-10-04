
from lottery_runner.models.participant import Participant
from lottery_runner.models.lottery import BalancedLottery

class LotteryRunner:
    def __init__(self):
        self.open_lotteries = {}
        self.closed_lotteries = []
        self.users = {}
        self.acting_user = self.create_user('test-user', 100)

        
    def create_user(self, name:str, init_balance:int=100) -> Participant:
        participant = Participant(name, init_balance)
        self.users[participant.id] = participant
        return participant

    def switch_acting_user(self, user_id:int) -> None:
        self.acting_user = self.users[user_id]
        print('Changed the acting user to {} (User-{})'.format(self.users[user_id].name), user_id)

    def create_lottery(self, user:Participant) -> BalancedLottery:
        lottery = BalancedLottery(creator=user, state='open')
        self.open_lotteries[lottery.id] = lottery
        return lottery

    def purchase_lottery_tickets(self, lottery_id:int, number_of_tickets:int) -> None:
        lottery = self.open_lotteries.get(lottery_id)
        if self.acting_user.balance >= number_of_tickets:
            if lottery:
                for i in range(0, number_of_tickets):
                    ticket = lottery.create_ticket(owner_id=self.acting_user.id)
                    self.acting_user.purchase_ticket(ticket)
            print('Bought {} tickets for lottery-{}.'.format(number_of_tickets, lottery_id))
        else:
            print('Not enough money to buy tickets.')

    def resolve_lottery(self, lottery_id:int) -> None:
        lottery = self.open_lotteries.pop(lottery_id)
        if lottery.creator == self.acting_user:
            winner_id, reward = lottery.resolve_lottery()
            winner = self.users.get(winner_id)
            winner.add_price_money(reward)
            print('{} is the winner of lottery {}, he gains {} coins.'.format(winner.name, lottery.id, reward))
            self.closed_lotteries.append(lottery)
        else:
            print('Only creator can resolve lottery.')

    def print_state(self):
        print('============================')
        print('Open Lotteries:')
        if not self.open_lotteries:
            print('No open lottery found.')
        for lottery_id, lottery in self.open_lotteries.items():
            lottery.print_info()
        print('============================')
        print('Users: ')
        for user_id, user in self.users.items():
            print('{} (ID-{})'.format(user.name, user_id))
        print('============================')
