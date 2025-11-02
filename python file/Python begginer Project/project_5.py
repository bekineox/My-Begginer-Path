profit=0
Menu={
    "latte":{
        'ingredients':{
            'water':200,
            'milk':150,
            'coffee':24,
        },
        'cost':150
    },
    'esperesso':{
        'ingredients':{
            'water':50,
            'coffee':18,
        },
        'cost':100,
    },
    "cappuccino":{
        "ingredients":{
            'water':258,
            'milk':100,
            "coffee":24,
        },
        'cost':200,
    },
}
resources={
    "water":500,
    "milk":550,
    "coffee":120
}
def check_resources(order_ingredient):
    for item in order_ingredient:
        if order_ingredient[item] > resources[item]:
            print(f'there is no enough {item} resource is available.')
            return False
        else:
            return True
def process_coins():
    print('please insert coins')
    total=0
    coins_five=int(input('how many 5Br coins:'))
    coins_ten=int(input('how many 10Br coins:'))
    coins_twenty=int(input('How many 20Br coins:'))
    total=coins_five*5+coins_ten*10+coins_twenty*20
    return total
def payment_check(money_received,coffee_cost):
    if money_received >= coffee_cost:
        global profit
        profit+=coffee_cost
        change=money_received-coffee_cost
        print(f'Here is your Br{change} in change.')
        return True
    else:
        print('sorry that is not enough money.Money Refunded.')
        return False
def make_coffee(coffee_name,coffee_ingredient):
    for item in coffee_ingredient:
        resources[item]-=coffee_ingredient[item]
    print(f'here is your {coffee_name} ...Enjoy !!!')

    
is_on=True
while is_on:
    print('what would you like to have? latte/esperesso/cappuccino')
    choice=input('Enter your choice:').lower()
    if choice == "report":
        print(f"water={resources['water']}")
        print(f"milk={resources['milk']}")
        print(f"coffee={resources['coffee']}")
        print(f'money={profit}ETB')
    elif choice=='off':
        is_on=False
    else:
        coffee_type=Menu[choice]
        checked=check_resources(coffee_type['ingredients'])
        if checked:
            payment=process_coins()
            payment_checked=payment_check(payment,coffee_type['cost'])
            if payment_checked:
                make_coffee(choice,coffee_type['ingredients'])


