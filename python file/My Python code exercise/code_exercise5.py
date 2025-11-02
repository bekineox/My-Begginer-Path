import random
import os
while True:
    names=input("Enter every body's name separated by space :")
    names_list=names.split(',')
    print(names_list)
    length=len(names_list)
    # a=random.choice(names_list)
    a=random.randint(0,length-1)
    print(f"{names_list[a]} will pay the bill")