# "Guess the number" mini-project
# Sebastiano Tognacci
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random
import math

range_max = 100
max_tries = 7
num_tries = 7

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global secret_number, num_tries
    num_tries = max_tries
    secret_number = random.randrange(0, range_max) 
    print "New game. Range is from 0 to",range_max
    print "Number of remaining guesses is", num_tries,"\n"


# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global range_max, max_tries
    range_max = 100
    max_tries = 7
    new_game()

def range1000():
    # button that changes the range to [0,100) and starts a new game 
    global range_max, max_tries
    range_max = 1000
    max_tries = 10  
    new_game()
    
def input_guess(guess):
    # main game logic goes here	
    global secret_number, num_tries
    # remove this when you add your code
    if guess.isdigit():
        guess = int(guess)
        print "Guess was",int(guess)
        num_tries -= 1
        print "Number of remaining guesses is",num_tries
        
        if num_tries > 0:
            if guess > secret_number:
                print "Lower!\n"
            elif guess < secret_number:
                print "Higher!\n"
            else:
                print "Correct!\n"
                new_game()
            
        elif num_tries == 0:
            print "You ran out of guesses.  The number was", secret_number,"\n"
            new_game()            
    else:
        print "Invalid input, enter an integer number"
    
    
# create frame
frame = simplegui.create_frame('GuessTheNumber', 200, 200)

# register event handlers for control elements and start frame
bn_range100 = frame.add_button('Range: 0 - 100', range100,150)
bn_range1000 = frame.add_button('Range: 0 - 1000', range1000,150)
inp_guess = frame.add_input('Guess the number:', input_guess, 150)

# call new_game 
new_game()
frame.start()

# always remember to check your completed program against the grading rubric