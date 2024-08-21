"""
Created on Nov 27, 2018

@author: Vedha
"""


if __name__ == "__main__":
    a = "DERRICK"
    b = "DERRICK"
    print(a.capitalize())
    print(a.lower())
    print(a.upper())
    print(a.islower())
    print(a.isupper())
    print(b.endswith('e'))
    print(b.startswith('l'))
    print(b.__len__())
    print(b.replace(b, "rajasekar"))
    print(b.count('e'))
    print(a.title())
    print(a.__eq__("DERRICK"))
    print(a.swapcase())
    print("enter string")
    a = input()
    print(a)
    print(b.__contains__(a))
    a = "derrick"
    b = "rajasekar"
    print(a.center(1))
    print(a.find('e'))
    print(a.index('i'))
    print(a.__add__(b))
    print(a.join("ra"))
    print(a.isspace())
    print(a.ljust(24, 'e'))
    print(a.rjust(24, 'd'))
    print(a.__sizeof__())
    print(b.__sizeof__())
    print(a.__ne__("raja"))
    print(b.__mul__(4))
    x = 12
    y = 13
    print(x.__mod__(y))
