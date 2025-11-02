#game project
import random
user_choice=int(input('enter a number 0 for rock,1 for paper,2 for scissor :'))
computer_choice=random.randint(0,2)
#print(f'computer choose :{computer_choice}')
if user_choice == 0 or user_choice == 1 or user_choice == 2:
    if user_choice == 0 and computer_choice ==2:
        print('You Win')
    elif user_choice == 2 and computer_choice == 0:
        print('You Loose')
    elif user_choice == computer_choice:
        print('it is a Draw')
    elif user_choice > computer_choice:
        print('You Win')
    else:
        print('You Loose')
else:
    print('You Entered invalid Number so, You Loose')
    