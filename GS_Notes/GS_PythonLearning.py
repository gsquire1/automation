# Scratch file for learning
# import random
# Working with Files
import sys


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

# d = {'k1': 1, 'k2': 2, 'k3': 3}
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

# # 3 Cup Monte (Also in its own file)
# from random import shuffle
#
# mylist = [' ', 'O', ' ']
# shuffle(mylist)
# # print(mylist)
#
#
# # USER GUESS
# def player_guess():
#     guess = ''
#     while guess not in ['0', '1', '2']:
#         guess = input("Pick a number: 0, 1 or 2   ")
#     return int(guess)
#
#
# # CHECK GUESS
# def check_guess(mylist, guess):
#     if mylist[guess] == 'O':
#         print("Correct!")
#     else:
#         print("Wrong Guess")
#         print(mylist)
#
#
# guess = player_guess()
# check_guess(mylist, guess)
####################################

# *arg & **kwargs
# def myfunc1(*args):
#     # Accepts arbitrary number of arguments into func and Returns 5% of the sum of them all
#     # print(args)
#     return sum(args) * .05  # double parenthesis as you have to pass in a tuple ()
#
#
# myfunc1(40, 60, 100, 0, 250)
#
# def myfunc2(*args, **kwargs):
#     print('I would like {} {}'.format(args[0], kwargs['food']))
#
#
# myfunc2(10, 20, 30, fruit='orange', food='eggs', animal='dog')
# # print(b)

# Coding Exercise 19
# def myfunc(*args):
#     answer = []
#     for i in args:
#         if i % 2 == 0:
#             answer.append(i)
#     return answer


# x = myfunc(5, 6, 7, 8)
# print(x)
#######################

# Coding Exercise 20
# def myfunc(*args):
#     print('1111111111111111')
#     print(type(args))
#     out = []
#     args = (args[0])  # This was the missing link as it changed *args type from tuple to string
#     print('2222222222222222')
#     print(type(args))
#     print(args)
#     for i in range(len(args)):
#         # print(i)
#         if i % 2 == 0:
#             out.append(args[i].lower())
#         else:
#             out.append(args[i].upper())
#     return out
#
#
# d = myfunc('Anthropomorphism')
# print(d)
########################

# LESSER OF TWO EVENS: Write a function that returns the lesser of two given numbers if both numbers are even,
# but returns the greater if one or both numbers are odd.

# def lesser_of_two_evens(a, b):
#     if a % 2 == 0 and b % 2 == 0:
#         # Both numbers are even
#         if a < b:
#             return a
#         else:
#             return b
#     else:  # a % 2 != 0 or b % 2 != 0:
#         # One or both numbers are odd
#         if a > b:
#             return a
#         else:
#             return b

# Using the min/max function:
# def lesser_of_two_evens(a, b):
#     # Are both numbers even
#     if a % 2 == 0 and b % 2 == 0:
#         return min(a, b)
#     else:
#         return max(a, b)
#
#
# x = lesser_of_two_evens(7, 5)
# print(x)
########################

# ANIMAL CRACKERS: Write a function takes a two-word string and returns True if both words begin with same letter


# def animal_crackers(text):
#     # [i for i in text.split() if i[0] == i[0]]
#     # b = [i[0] for i in text.upper().split()]
#     # if b[0] == b[1]:
#     #     return True
#     # else:
#     #     return False
#     wordlist = text.upper().split()
#     return wordlist[0][0] == wordlist[1][0]
#
#
# x = animal_crackers('Levelheaded Llama')
# # x = animal_crackers('Crazy Kangaroo')
# print(x)
################################

# MAKES TWENTY: Given two integers, return True if the sum of the integers is 20 or if one of the integers is 20.
# If not, return False

# def makes_twenty(n1, n2):
#     if n1 + n2 == 20:
#         return True
#     elif (n1 == 20) or (n2 == 20):
#         return True
#     else:
#         return False

def makes_twenty(n1, n2):
    if n1 + n2 == 20 or n1 == 20 or n2 == 20:
        return True
    else:
        return False

# x = makes_twenty(20, 10)
# x = makes_twenty(12, 8)
# x = makes_twenty(2, 3)
# print(x)
#################################


# Level 1 Problem: OLD MACDONALD - Write a function that capitalizes the first and fourth letters of a name

# def old_macdonald(name):
# out = name.capitalize().replace('d', 'D', 1)
# return out
#     first_half = name[:3].capitalize()
#     second_half = name[3:].capitalize()
#     return first_half + second_half
#
#
# x = old_macdonald('macdonald')
# print(x)
################################

# Level 1 Problem: MASTER YODA - Given a sentence, return a sentence with the words reversed


# def master_yoda(text):
#     y = (text.split())
#     reverse_y = y[::-1]
#     z = ' '.join(reverse_y)
#     return z


# x = master_yoda('I am home')
# x = master_yoda('We are ready')
# print(x)
# master_yoda('I am home') --> 'home am I'
# master_yoda('We are ready') --> 'ready are We'
##############################

# Level 1 Problem: ALMOST THERE - Given an integer n, return True if n is within 10 of either 100 or 200
# NOTE: abs(num) returns the absolute value of a number

# def almost_there(n):
#     x = (abs(100-n) <= 10) or (abs(200-n) <= 10)
#     return x
#
#
# z = almost_there(209)
# print(z)
# almost_there(90)  # --> True
# almost_there(104)  # --> True
# almost_there(150)  # --> False
# almost_there(209)  # --> True
############################

# Level 2 Problem: Given a list of ints, return True if the array contains a 3 next to a 3 somewhere

# def has_33(nums):
#     for i in range(0, len(nums)-1):
#         if nums[i] == 3 and nums[i+1] == 3:
#             return True
#     return False

# Check
# x = has_33([1, 3, 3])
# Check
# x = has_33([1, 2, 3, 3])
# Check
# x = has_33([3, 1, 3, 1, 2, 3, 3])
# print(x)
##########################

# Level 2 Problem: PAPER DOLL: Given a string, return a string where for every character in the original there are
# three characters

# def paper_doll(text):
#     out = ''
#     for i in text:
#         out += i * 3
#     return out

# Check
# x = paper_doll('Hello')
# x = paper_doll('Mississippi')
# print(x)
############################

# Level 2 Problem:BLACKJACK: Given three integers between 1 and 11, if their sum is less than or equal to 21, return
# their sum. If their sum exceeds 21 and there's an eleven, reduce the total sum by 10. Finally, if the sum
# (even after adjustment) exceeds 21, return 'BUST'

# def blackjack(a, b, c):
#     if sum([a, b, c]) <= 21:
#         return sum([a, b, c])
#     elif 11 in [a, b, c] and sum([a, b, c]) - 10 <= 21:
#         return sum([a, b, c]) - 10
#     else:
#         return 'BUST'


# x = blackjack(5, 6, 7)
# x = blackjack(9, 9, 9)
# x = blackjack(9, 9, 11)
# print(x)
##########################
# Nested For Loop with "WHILE" LOOPS, "WHILE NOT" LOOPS
# Level 2 Problem: SUMMER OF '69: Return the sum of the numbers in the array, except ignore sections of numbers
# starting with a 6 and extending to the next 9 (every 6 will be followed by at least one 9). Return 0 for no numbers.

# def summer_69(arr):
#     total = 0  # total number placeholder (start at 0)
#     add = True  # Set up condition for while loop
#     for num in arr:
#         # print(num)
#         while add:  # While add is true
#             if num != 6:
#                 total += num
#                 break  # Breaks you out of WHILE loop returning you to FOR loop. Only connected to this while loop
#             else:
#                 add = False  # Sets add to FALSE thereby dropping into second while loop
#         while not add:  # add Set to FALSE now
#             if num != 9:  # Waiting for the next number to be 9. While still set to FALSE
#                 break  # if not 9, break out of WHILE loop and continue with ???. Only connected to this while loop
#             else:
#                 add = True  # Reset to TRUE
#                 break
#         return total

# summer_69([1, 3, 5]) --> 9
# summer_69([4, 5, 6, 7, 8, 9]) --> 9
# summer_69([2, 1, 6, 9, 11]) --> 14
# def summer_69(arr):
#     pass
# # Check
# x = summer_69([1, 3, 5])
# x = summer_69([4, 5, 6, 7, 8, 9])
# x = summer_69([2, 1, 6, 9, 11])
# print(x)
###########################
# Challenging Problems:
# SPY GAME: Write a function that takes in a list of int and ret True if it contains 007 in order


# def spy_game(nums):
#
#     code = [0, 0, 7, 'x']   # use an outside data structure. Concurrent int ends with string 'x'
#     for num in nums:        # iterate through
#         if num == code[0]:  # looking for 1st int in list
#             code.pop(0)     # once found, pop it off the list
#
#     return len(code) == 1   # made it thru looking for and found 0,0,7 in list. Return F if any int are still in list


# spy_game([1,2,4,0,0,7,5]) --> True
# spy_game([1,0,2,4,0,5,7]) --> True
# spy_game([1,7,2,0,4,5,0]) --> False

# x = spy_game([1,2,4,0,0,7,5])
# x = spy_game([1,0,2,4,0,5,7])
# x = spy_game([1,7,2,0,4,5,0])
# print(x)
##########################
# COUNT PRIMES: Write a function that returns the number of prime numbers that exist up to and including a given number.
# Treat 0 and 1 as not prime


def count_primes(num):

    # Check that the number is not a 0 or 1
    if num < 2:
        return 0
    # Now we know the number is 2 or greater

    # store our prime numbers
    primes = [2]
    # Counter going up to the input num
    x = 3

    # x is going through every number up to input num
    while x <= num:
        # Checks if x is prime
        for y in range (3,x,2):
            if x%y == 0:
                x += 2
                break
        else:
            primes.append(x)
            x += 2
    print(primes)
    return len(primes)


# Check
z = count_primes(100)
print(z)

