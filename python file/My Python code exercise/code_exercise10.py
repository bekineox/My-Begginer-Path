list_of_numbers=input("Enter a number separated by space :")
all_numbers=list_of_numbers.split()

count=0
for i in all_numbers:
    count+=1
print(f'count :{count}')

for i in range(count):
    all_numbers[i]=int(all_numbers[i])
print(f'All number are :{all_numbers}')

max=all_numbers[0]
for i in all_numbers:
    if i >= max:
        max=i

print(max)


