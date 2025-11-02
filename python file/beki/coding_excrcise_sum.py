numbers=input("Enter a Number separated by comma:")
numbers_list=numbers.split(" ")
count=0
for i in numbers_list:
    count+=1
print(count)
sum = 0
for numbers_list in range(count+1):
    sum +=numbers_list
print(sum)