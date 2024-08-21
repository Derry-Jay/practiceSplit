"""
Created on Nov 27, 2018

@author: Vedha
"""


class Cons:
    area = 0

    def __init__(self):
        pi = 3.14
        r = 2.0
        Cons.area = pi * r * r

    def __del__(self):
        print("constructor destroyed")


if __name__ == "__main__":
    a = Cons()
    del a
    del a
