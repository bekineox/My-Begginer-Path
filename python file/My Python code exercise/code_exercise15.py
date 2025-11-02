class Account:
    def __init__(self,name,balance):
        self.account_name=name 
        self.balance=balance
    def Deposit(self,amount):
        self.balance+=amount
        print(f'you are deposited {amount}')
    def Withdraw(self,amount):
        if amount >=self.balance:
            print("you don't have enough balance to withdraw")
        else:
            self.balance-=amount
            print(f'{amount}Birr Successfully withdrawal')
    def __str__(self):
        return f'Account name :{self.account_name}\nAccount balance :{self.balance}'
A1=Account('Bereket',20000000)
print(A1)
A1.Deposit(2000)
A1.Withdraw(300000)
print(A1)
