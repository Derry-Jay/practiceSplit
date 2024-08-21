"""
Created on Feb 1, 2019

@author: Vedha
"""


class Test:
    x = 0

    def __init__(self):
        self.x = 1


class DerivedTest(Test):
    def __init__(self):
        super().__init__()
        self.y = 1

    def put(self):
        print(Test.x, self.y)


b = DerivedTest()
b.put()



