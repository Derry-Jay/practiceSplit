"""
Created on Dec 21, 2018

@author: Vedha
"""
from tensorflow import *
# from scipy import *
from models.lat_long import LatLong

# lt = int(input('Enter Limit:'))
# b = int(input('Enter Count:'))
# print("Fibonacci Series:")
# for i in range(0, b + 1):
#     print(Int(i).nth_fibonacci_term())
# print("Strong Numbers:")
# for i in range(1,lt + 1):
#     if Int(i).is_strong():
#         print(i, end="" if i == lt else ", ")
# print("Prime Numbers:")
# for j in range(2, lt + 1):
#     if Int(j).is_prime():
#         print(j, end="" if j == lt else ", ")
# print("")
# print("Armstrong Numbers:")
# for j in range(1, lt + 1):
#     if Int(j).is_armstrong():
#         print(j, end="" if j == lt else ", ")
# print("")
# n = Int(int(input('Enter n:')))
# n.number_to_words()
chennai = LatLong(13.0825, 80.275)
print('Chennai: ', chennai.get_date_time_excluding_time_zone().strftime('%Y-%m-%d %H:%M:%S.%f %Z'))
mumbai = LatLong(19.076, 72.8775)
print('Mumbai: ', mumbai.get_date_time_excluding_time_zone().strftime('%Y-%m-%d %H:%M:%S.%f %Z'))
bangalore = LatLong(12.979, 77.5915)
print('Bangalore: ', bangalore.get_date_time_excluding_time_zone().strftime('%Y-%m-%d %H:%M:%S.%f %Z'))
kolkata = LatLong(22.5675, 88.37)
print('Kolkata: ', kolkata.get_date_time_excluding_time_zone().strftime('%Y-%m-%d %H:%M:%S.%f %Z'))
from extensions.custom_data_types import *

print(Int(5).is_eligible_age_to_vote())
# print(n.number_in_words())
print('hi')
print(Int(34).is_fibonacci_term())
print('hi')
print(Int(4).factorial())
print(Int(6) == 6)
print(Int(12).nth_fibonacci_term())
a = "derrick"
c = "rajasekar"
print(a + c)
print(a * 2)
print(a[0:2])
print(a[:2])
print(a[3:])
print(a[1::4])
print(a[:1:2])

m = 2
n = 3
print("total is" + str(m + n))
print(mumbai.haversine(kolkata))
print(chennai.haversine(bangalore))
print('Hello')
print(LatLong(12.9609417, 80.2567313).reverse_geocode())
print('Hello')
print(String('').is_empty())
print(String('              ').is_empty())
print(String('wert').is_not_empty())
print(String('qwerty').is_empty())
print(String('              ').is_not_empty())
print(String('').is_not_empty())
# a = ([0, 0], [0, 0]) '%Y-%m-%d %H:%M:%S.%f %Z'
#         b = ([0, 0], [0, 0])
# print("hello world")
# print("hello world")
#         for i in range(0, 2):
#             for j in range(0, 2):
#                 a[i][j] = input("enter the A-array values extensions by extensions")
#         for i in range(0, 2):
#             for j in range(0, 2):
#                 b[i][j] = input("enter the B-array values extensions by extensions")
#         print('Sum is:')
#         for i in range(0, 2):
#             for j in range(0, 2):
#                 print(a[i][j] + b[i][j])
# a = int(input("enter the no."))
#                 print(j)
#         print(digits)
#                 print(digits)
#             print(c)
#             print(c)
#         print('The no of distinct Elements is:', n)
#         print('The no of distinct Elements is:', n)
# print(7.0.__ceil__())
# print(7.0.__floor__())
# print((sqrt(7) * sqrt(7)).__ceil__())
# print(sqrt(7) * sqrt(7))
# print(2.5.__ceil__())
# print(2.5.__floor__())

a = abs(-1)

print(a)
# age = int(input("enter the age"))

# b = Int(5)
