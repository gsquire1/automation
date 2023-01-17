# Scratch file for learning
# import random
# Working with Files

# myfile = open('myfile.txt')
# # print(myfile.read())
# # myfile.seek(0)
# print(type(myfile))
# #print(a)
# #print('This the type:' + a )
# print(myfile.readlines())
# myfile.close()
#
# with open('myfile.txt', mode='r') as f:
#     contents = f.read()
#     print('print')
#     print(contents)
# d = {'k1':[{'nest_key':['this is deep',['hello']]}]}
# print(d['k1'][0]['nest_key'][1])
##################

# If, Else, Elif

# loc = 'Stor'
# if loc == 'Auto Shop':
#     print('Cars are cool!')
# elif loc == 'Bank':
#     print('Get me some cash!')
# elif loc == "Store":
#     print('Get me some food!')
# else:
#     print('I know NADA')
###################

# For Loops

# my_iterable = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# for i in my_iterable:
#     if i % 2 == 0:
#         print(i)
#     else:
#         print(f'Odd Number: {i}')
#
# list_sum = 0
# for i in my_iterable:
#     list_sum = list_sum + i
# print(list_sum)
#
# mystring = 'Hello World'
# for _ in mystring:
#     print('letter')

# mylist = [(1, 2), (3, 4), (5, 6), (7, 8)]
# print(len(mylist))
#
# for item in mylist:
#     print(item)
#####################

# Tuple Unpacking

# for a, b in mylist:
#     print(a, b)
#     print(type(b))

# Iterate through dictionary using tuple unpacking

d = {'k1': 1, 'k2': 2, 'k3': 3}
# for key, value in d.items():
#     print(key)
#     print(value)

# for key in d.keys():
#     print(key)

# for value in d.values():
#     print(value)

# for a, b in d:
#     print('X')
#     print(a, b)
#     print('Y')
#     print(a)
#     print('Z')
#     print(b)
# print('ZZ')
##################

# While Loops (break, continue, pass)
# Break: breaks out of the closest enclosing loop
# Continue: Goes to the top of the closest enclosing loop
# Pass: Does nothing at all
#
# x = 0
# while x < 5:
#     print(f'The current value of x is {x}')
#     x += 1
# else:
#     print(x)
#
# mystring = 'Sammy'
# for letter in mystring:
#     if letter == 'a':
#         continue
#     print(letter)
#
# mystring = 'Sammy'
# for letter in mystring:
#     if letter == 'a':
#         break
#     print(letter)
#####################

# Useful Operators in Python

# Range Function
# iterate through it:
# for num in range(3, 10):
#     print(num)

# Enumerate
# index_count = 0
# word = 'abcde'
# for index, letter in enumerate(word):
#     print(index)
#     print(letter)
#     print('\n')
#     index_count += 1

# Zip
# mylist1 = [1, 2, 3]
# mylist2 = ['a', 'b', 'c']
# for item in zip(mylist1, mylist2):
#     print(item)
#
# a = list(zip(mylist1, mylist2))
# print(a)

# In
# 'z' in ['x', 'y', 'z']
# a = 'mykey' in {'mykey':345}
# print(a)

# Min and Max
# my_list = [10, 20, 30, 40, 100]
# print(min(my_list))
# print(max(my_list))

# Random
# shuffle - this wasn't working when last used
# mylist3 = {1, 2, 3, 4, 5}
# from random import shuffle
# random.shuffle(mylist3)

# User Input
# name = input('What is your name: ') # This will always be a string
# print(name)
######################

# List Comprehensions
# [element for element in 'string']

# my_string = 'palisade'
# wtf = []
# for letter in my_string:
#     wtf.append(letter)
# print(wtf)
#
# wtf = [letter for letter in my_string]  # List Comprehension for above
# print(wtf)

# mylist3 = []
# for i in 'word':
#     mylist3.append(i)
#
# mylist3 = [x for x in 'word']  # List Comprehension for above
# print(mylist3)

# mylist4 = []
# for i in range(1, 11):
#     mylist4.append(i**2)
# mylist4 = [num**2 for num in range(1, 11)] # List Comprehension for above
# print(mylist4)

# mylist5 = []
# for num in range(0, 5):
#     if num % 2 == 0:
#         mylist5.append(num)
# mylist5 = [num for num in range(0, 5) if num % 2 == 0] # List Comprehension for above with if statement
# print(mylist5)

# celcius = [0, 10, 20, 34.5]
# Fahrenheit = []
# for temp in celcius:
#     Fahrenheit.append(((9/5) * temp + 32))
# fahrenheit = [((9/5) * i + 32) for i in celcius]  # List Comprehension for above auto append statement
# print(Fahrenheit)


# ASSESSMENT CODE
# st = 'Print only the words that start with s in this sentence'
# for word in st.split():
#     if word[0] == 's':
#         print(word)
# response = [i for i in st.split() if i[0] == 's'] # list comprehension adds to list auto as for loop is run
# print(response)

# even = [num for num in range(0, 11) if num % 2 == 0]
# print('even')
# print(even)

# odd = [num for num in range(0, 11) if num % 2]
# print('odd')
# print(odd)

# for num in range(0, 11, 2):
#     print(num)
#
# num = [x for x in range(0, 11) if x % 2 == 0]
# print(num)

# response = [num for num in range(0, 51) if num % 3 == 0]
# print(response)

# st = 'Print every word in this sentence that has an even number of letters'
# st1 = []
# for i in st.split():
#     if len(i) % 2 == 0:
#         st1.append(i)
# print(st1)
#
# st1 = [i for i in st.split() if len(i) % 2 == 0]
# print(st1)

# for i in range(0, 101):
#     if i % 3 == 0 and i % 5 == 0:   # This first as either of bottom 2 will resolve and loop starts over
#         print("FizzBuzz")
#     elif i % 3 == 0:
#         print('Fizz')
#     elif i % 5 == 0:
#         print("Buzz")
#     else:
#         print(i)

# st = 'Create a list of the first letters of every word in this string'
# b = []
# for a in st.split():
#     b.append(a[0])
# print(b)
#
# b = [i[0] for i in st.split()]
# print(b)
# def even_check(number):
#     return number % 2 == 0
#
#
# answer = even_check(21)
# print(answer)

# Return True if ANY number is true in a list
#
# x = check_even(my_num_list)
# print(x)
#####################################

# Tuple unpacking with Python Functions

# stock_prices = [('AAPL', 200), ('GOOG', 400), ('MSFT', 100 )]
#
# for ticker, price in stock_prices:
#     print(ticker, (price+(.1*price)))
#    # print(price+(.1*price))

# work_hours = [('Abbey', 100), ('Billy', 400), ('Cassie', 800)]
#
#
# def employee_check(work_hours):
#
#     current_max = 0
#     employee_of_the_month = ''
#
#     for emp, hours in work_hours:
#         if hours > current_max:
#             current_max = hours
#             employee_of_the_month = emp
#     return employee_of_the_month, current_max
#
# # tuple unpacking with a function call
#
#
# name, hours = employee_check(work_hours)
# print(name)
# print(hours)
##################################

# 3 Cup Monte (Also in its own file)
from random import shuffle

mylist = [' ', 'O', ' ']
shuffle(mylist)
# print(mylist)


# USER GUESS
def player_guess():
    guess = ''
    while guess not in ['0', '1', '2']:
        guess = input("Pick a number: 0, 1 or 2   ")
    return int(guess)


# CHECK GUESS
def check_guess(mylist, guess):
    if mylist[guess] == 'O':
        print("Correct!")
    else:
        print("Wrong Guess")
        print(mylist)


guess = player_guess()
check_guess(mylist, guess)
