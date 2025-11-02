#calculater project
import os
def add(num1,num2):
    Addtion=num1+num2
    print(f'The addition of numbers {Addtion}')
def sub(num1,num2):
    subtraction=num1-num2
    print(f'the subtraction of numbers are {subtraction}')
def multi(num1,num2):
    multiplication=num1*num2
    print(f'the multiplication of numbers are {multiplication}')
def division(num1,num2):
    division=num1/float(num2)
    print(f'the division of numbers are {division}')
def modulo(num1,num2):
    remainder = num1%num2
    print(f'the remainder of numbers are {remainder}')

          

calculator_off=False
while not calculator_off:
    num1=input('Enter First number or if u want to off the calculator type "off":')
    if num1 == 'off':
        calculator_off =True
    else:
        operator=input('Choose ur operator,+,-,*,/,% :')
        num2=int(input('Enter second number :'))
        
        num1=int(num1)
        if operator=="+":
            add(num1,num2)
        elif operator =="-":
            sub(num1,num2)
        elif operator =="*":
            multi(num1,num2)
        elif operator =="/":
            division(num1,num2)
        elif operator == '%':
            modulo(num1,num2)
        else:
            print('you Entered wrong operator')
    

