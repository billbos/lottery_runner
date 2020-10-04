from lottery_runner.app import LotteryRunner

def print_actions():
   print("Available actions:")
   print("Create user (CU name balance)")
   print("Change active user (CA user_id)")
   print("Create lottery  (CL)")
   print("Purchase lottery tickets (PT lottery_id number_of_tickets)")
   print("Resolve lottery (RL lottery_id)")


def main():
    lottery_runner = LotteryRunner()
    print('============================')
    print('Lottery Runner System Demo!')
    print('============================')
    while True:
        try:
            lottery_runner.print_state()
            print_actions()
            action = input('[{}] Enter an action: '.format(lottery_runner.acting_user.name))

            input_params = action.split(' ')
            type_of_action = input_params[0]
            if type_of_action.upper() == 'CR':
                print('FINISHED Lottery Runner')
                break

            elif type_of_action.upper() == 'CA':
                lottery_runner.switch_acting_user(int(input_params[1]))
            elif type_of_action.upper() == 'CU':
                lottery_runner.create_user(input_params[1])
            elif type_of_action.upper() == 'CL':
                lottery_runner.create_lottery(lottery_runner.acting_user)
            elif type_of_action.upper() == 'CA':
                lottery_runner.switch_acting_user(input_params[1])
            elif type_of_action.upper() == 'PT':
                lottery_runner.purchase_lottery_tickets(int(input_params[1]),int(input_params[2]))
            elif type_of_action.upper() == 'RL':
                lottery_runner.resolve_lottery(int(input_params[1]))

        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()