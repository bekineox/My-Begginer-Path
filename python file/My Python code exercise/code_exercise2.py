size=input('Hey Man,choose your type of piza (s/m/l)?')
size.lower
print(type(size))
bill=0
if size == 's':
    bill += 100
    print('small size pizza price is 100')
elif size == 'm':
    bill += 200
    print('medium size pizza price is 200')
elif size == 'l':
    bill += 300
    print('large size pizza price is 300')
pepperoni=input('Do u want pepperoni(Y OR N)')
pepperoni.lower
if pepperoni == 'y':
    if size == 's':
        bill += 30
    else:
        bill += 50
extra_chess=input('Do u want Extra Chess(Y or N)')
if extra_chess == 'y':
    bill += 20
print(f'your total  bill is {bill}')