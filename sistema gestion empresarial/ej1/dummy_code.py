"""In this file you can see some dummy code where some uncovered pylint rules
appears, so that pylint can check it"""
# there is less than 8 import and the import function are used.
import random
#PYLINT RULE : NUMBER OF ATTRIBUTES
class Student:
    """Class Student"""
    def __init__(self,age,course,birthdate,dni):
        self.age=age
        self.course=course
        self.birthdate=birthdate
        self.dni=dni
    def hello(self):
        """Hello"""
        return
    def bye(self):
        """Bye"""
        return
    #PYLINT RULE: IGNORE WORDS
    def fetchUserData(self,param):
        """Dummy function"""
        print(param)
a=random.random
#There are some rules which we were unable to write additional code to prove it.
