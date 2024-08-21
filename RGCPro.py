"""
Created on Feb 7, 2019

@author: Vedha
"""
from pip._vendor.distlib.compat import raw_input


s = raw_input('Enter String:')

if __name__ == "__main__":
    arr = [0, 0, 0, 0]
    for i in range(4):
        arr[i] = input('Enter the Element:')
    print('The Distinct Elements are:')
