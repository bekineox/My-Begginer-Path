number=int(input("enter a number \n"))
prime=True
if number ==1:
    prime = False
for i in range(2,number):
    if number % i ==0:
        prime = False
if prime:
    print('it is prime number')
else:
    print('it is not prime number')
    


