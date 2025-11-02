year=int(input('enter a number you want to check'))
if year%4==0:
    if year%100==0:
        if year%400==0:
            print("it is a leap year ")
        else:
            print('it is not a leap year')
    else:
        print("not a leap year")
else:
    print("not leap year")