"""
Created on Nov 26, 2018

@author: Vedha
"""


class Poly:
    def get(self):
        print("hello")


class Poly1(Poly):
    def get(self):
        oa = Poly()
        oa.get()
        print("derrick")


if __name__ == "__main__":
    ob = Poly1()
    ob.get()
