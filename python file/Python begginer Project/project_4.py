import random
EASY_LEVEL_ATTEMPTS=10
HARD_LEVEL_ATTEMPTS=5
def set_difficulty(level):
    if level =='easy':
        return EASY_LEVEL_ATTEMPTS
    elif level =='hard':
        return HARD_LEVEL_ATTEMPTS
    else:
        pass
def check_answer(guessed_number,answer,attempts):
    if guessed_number>answer:
        print('your guess is too high')
        return attempts-1
    elif guessed_number==answer:
        print(f'your guess is right... the answer was {answer}')
    elif guessed_number < answer:
        print('your guess is too low')
        return attempts-1
def Guess_Number_Game():
    print('let me think of a number between 1 to 50')
    level=input('choose the level of difficulty....Type "easy" or "hard":').lower()
    answer=random.randint(1,50)
    attempts=set_difficulty(level)
    if attempts != EASY_LEVEL_ATTEMPTS and attempts != HARD_LEVEL_ATTEMPTS:
        print('you have entered wrong Choice....play again')
        Guess_Number_Game()
    guessed_number=0
    while guessed_number != answer:
        print(f'you have {attempts} attempts remaining to guess the number')
        guessed_number=int(input('guess a number:'))
        attempts=check_answer(guessed_number,answer,attempts)
        if attempts == 0 :
            print('you are finished all remaining attempts, So you LOOSE')
            return 
        elif attempts !=0 and guessed_number ==answer:
            pass
        else:
            print('guess again')
Guess_Number_Game()

