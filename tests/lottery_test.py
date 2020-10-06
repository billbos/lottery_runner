# content of test_scenarios.py
from lottery_runner.models.lottery import BalancedLottery, Lottery, CreatingWrongNumberTicketsLottery, MissingShuffleLottery
from lottery_runner.models.participant import Participant
import unittest

def pytest_generate_tests(metafunc):
    idlist = []
    argvalues = []
    for scenario in metafunc.cls.scenarios:
        idlist.append(scenario[0])
        items = scenario[1].items()
        argnames = [x[0] for x in items]
        argvalues.append([x[1] for x in items])
    metafunc.parametrize(argnames, argvalues, ids=idlist, scope="class")


scenario1 = ("balanced", {"num_iteration": 1000, "threshold": 0.05, "num_participants":2, "ticket_purchase":[{'user_id':0, "num_ticket":2},{'user_id':1, "num_ticket":2}]})
scenario2 = ("balanced", {"num_iteration": 1000, "threshold": 0.05, "num_participants":2, "ticket_purchase":[{'user_id':0, "num_ticket":1},{'user_id':1, "num_ticket":2}, {'user_id':0, "num_ticket":1}]})
scenario3 = ("inbalanced_1", {"num_iteration": 1000, "threshold": 0.05, "num_participants":2, "ticket_purchase":[{'user_id':0, "num_ticket":8}, {'user_id':1, "num_ticket":2}]})
scenario4 = ("inbalanced_2", {"num_iteration": 1000, "threshold": 0.05, "num_participants":2, "ticket_purchase":[{'user_id':0, "num_ticket":2}, {'user_id':1, "num_ticket":8}]})
scenario5 = ("inbalanced_2", {"num_iteration": 1000, "threshold": 0.05, "num_participants":3, "ticket_purchase":[{'user_id':0, "num_ticket":2}, {'user_id':2, "num_ticket":2},{'user_id':1, "num_ticket":2}]})
scenario6 = ("inbalanced_2", {"num_iteration": 1000, "threshold": 0.05, "num_participants":2, "ticket_purchase":[{'user_id':0, "num_ticket":1}, {'user_id':1, "num_ticket":1}]})


class TestLottery:
    scenarios = [scenario1, scenario2, scenario3, scenario4, scenario5, scenario6]

    def test_balanced_lottery(self, num_iteration:int, threshold:float, ticket_purchase:dict, num_participants:int) -> None:
        creator = Participant('creator')
        lottery = BalancedLottery(creator=creator)
        result = self.run_lottery(lottery=lottery, ticket_purchase=ticket_purchase, num_participants=num_participants, num_iteration=num_iteration)
        self.evaluate_lottery_results(num_participants, num_iteration,threshold, result)

    # def test_not_shuffle_lottery(self, num_iteration:int, threshold:float, ticket_purchase:dict, num_participants:int) -> None:
    #     creator = Participant('creator')
    #     lottery = MissingShuffleLottery(creator=creator)
    #     result = self.run_lottery(lottery=lottery, ticket_purchase=ticket_purchase, num_participants=num_participants, num_iteration=num_iteration)
    #     self.evaluate_lottery_results(num_participants, num_iteration,threshold, result)
    
    # def test_create_wrong_number_lottery(self, num_iteration:int, threshold:float, ticket_purchase:dict, num_participants:int) -> None:
    #     creator = Participant('creator')
    #     lottery = CreatingWrongNumberTicketsLottery(creator=creator)
    #     result = self.run_lottery(lottery=lottery, ticket_purchase=ticket_purchase, num_participants=num_participants, num_iteration=num_iteration)
    #     self.evaluate_lottery_results(num_participants, num_iteration,threshold, result)

    def evaluate_lottery_results(self, num_participants:int, num_iteration:int, threshold:float, result:dict):
        if num_participants < result['total_tickets']:
            for i in range(0, num_participants):
                win_percentage = result['participants_win_counter'][i] / num_iteration
                expected_win_ratio = result['participants_to_num_tickets'][i]/result['total_tickets']
                min_win_ratio = expected_win_ratio - threshold
                max_win_ratio = expected_win_ratio + threshold
                assert min_win_ratio <= win_percentage <= max_win_ratio
        else:
            sum = 0
            for win_counter in result['participants_win_counter']:
                sum += win_counter
            assert sum == 0


    def run_lottery(self, lottery:Lottery, ticket_purchase:list, num_participants:int, num_iteration:int) -> dict:
        participants_win_counter = []
        participants_to_num_tickets = []
        total_tickets = 0
        for i in range(0, num_participants):
            participants_win_counter.append(0)
            participants_to_num_tickets.append(0)
        for tickets in ticket_purchase:
            lottery.create_tickets(num_tickets=tickets['num_ticket'], owner_id=tickets['user_id'])
            participants_to_num_tickets[tickets['user_id']] += tickets['num_ticket']
            total_tickets += tickets['num_ticket']

        for n in range(num_iteration):
            winner, reward = lottery.resolve_lottery()
            if winner == -1:
                continue
            participants_win_counter[winner] += 1
                
        return {'participants_win_counter':participants_win_counter, 'total_tickets': total_tickets, 'participants_to_num_tickets':participants_to_num_tickets}