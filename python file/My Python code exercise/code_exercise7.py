def for1():
    list1=[2,3,4,5]
    for i in list1:
        print(i ** 2,end=",")
def for2():
    for i in range(5):
        f=5-i
        for j in range(f):
            print('@',end=" ")
        print()
def for3():
    num=[2,3,4,5]
    cubic=[]
    for i in num:
        b=i ** 3
        cubic.append(b)
    print(cubic)
for1()
for2()
for3()
