class ComplexNumber:
    def __init__(self,r,i):
        self.real=r
        self.imagginary=i
    def __add__(self,other):
        return f'{self.real+other.real}+{self.imagginary+other.imagginary}i'
    def __sub__(self,other):
        return f'{self.real-other.real}+{self.imagginary-other.imagginary}i'

        
c1=ComplexNumber(4,5)
c2=ComplexNumber(5,6)
print(c1-c2)
print(c1+c2)




    