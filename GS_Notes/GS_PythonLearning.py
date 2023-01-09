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
mylist1 = [1, 2, 3]
mylist2 = ['a', 'b', 'c']
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

mystring = 'hello'
mylist = []
for letter in mystring:
    mylist.append(letter)
print(mylist)

mylist = [letter for letter in mylist]
print(mylist)

mylist = [x for x in "word"]
print(mylist)
