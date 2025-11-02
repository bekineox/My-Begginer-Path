love=True
while love:
    name1=input('Enter first name :')
    name2=input("Enter second name :")
    if name1 == 'off' :
        love=False
    else:
        L_name1=name1.lower()
        L_name2=name2.lower()
        combine_name=L_name1 + L_name2
        t=combine_name.count('t')
        r=combine_name.count('r')
        u=combine_name.count('u')
        e=combine_name.count('e')

        true=t+r+u+e

        l=combine_name.count('l')
        o=combine_name.count('o')
        v=combine_name.count('v')
        e=combine_name.count('e')

        love=l+o+v+e

        total =str(true) +str(love)
        print(total)
