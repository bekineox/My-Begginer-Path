import os
class Human:
    def __init__(self,num_heart):
        # print('calling from human')
        self.eye=2
        self.nose=1
        self.heart=num_heart
    def eat(self):
        print('i can eat')
    def work(self):
        print('i can work')
class Male: 
    def __init__(self,name):
        self.name=name
    def flirt(self):
        print('i can flirt')
    def work(self):
        print('i can code')
class Boy(Human,Male):
    def __init__(self,name,num_heart,language):
        Male.__init__(self,name)
        Human.__init__(self,num_heart)
        self.language=language
    def sleep(self):
        print('i can sleep')
    def work(self):
        super().work()
        print('i can test')
boy_1= Boy('beki',1,'python')
os.system('cls')
# print(boy_1.name)
# print(boy_1.eye)
# boy_1.work()
# Male.work(boy_1)
# print(boy_1.heart)
# print(boy_1.language)
