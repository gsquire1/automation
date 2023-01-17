# 3 Cup Monte


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





