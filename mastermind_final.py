import itertools
import random
from itertools import permutations
import numpy as np
import pandas as pd


# For our permutation we reduce from 9 to 6 "colors" representede by digits and no duplicates  
def givenum(num_colors, duplicate=False):
    if duplicate:
        num = np.random.choice(range(0,num_colors), 4, replace=True)
    else:
        num = random.sample(range(0,num_colors), 4)
    return list(num)

# Returns the result of the number of A and B
# A = Correct Color + Correct position
# B = Correct Color + wrong position
# Changed logic of calculation to factor in for duplicate scenario not originally present in the code 
def playresult(notknow, guess):
    A = 0
    B = 0
    temp_notknow = []
    temp_guess = []
    
    for i in range(len(notknow)): # checking for blacks only, and remove them from the list
        if notknow[i] == guess[i]:
            A = A + 1      
        else:
            temp_notknow.append(notknow[i])
            temp_guess.append(guess[i])
    for guess in temp_guess:
        if guess in temp_notknow:
            B = B + 1 
            idx = temp_notknow.index(guess)
            del temp_notknow[idx]

    return A, B


def chooseone(code_set):
    remain_table = np.zeros(len(code_set))
    # print(remain_table)
    for idx, val in enumerate(code_set):
        code_idx = [j for j in range(len(code_set))]
        code_idx.remove(idx)
        # if there is more than 100 combinations in the code set, we randomly sample 100
        if (len(code_idx) > 100):
            S = random.sample(code_idx, 100)
        # else we take all? 
        else:
            S = random.sample(code_idx, len(code_idx))
        remain = 0
        for idxx in S:   #  each idxx acts like answer, we play it out again and see how many remaining eligible one remains
            A, B = playresult(code_set[idxx], code_set[idx])
            print(code_set[idxx], code_set[idx], A, B)
            for k in S:
                a, b = playresult(code_set[k], code_set[idx])
                if (a == A and b == B):
                    remain = remain + 1
        #stores the number of remaining combinations for each c in S
        remain_table[idx] = remain

    #returns the index of the lowest value in remain_table
    mindex = np.argmin(remain_table)
    # the one with least average remaining eligible code is selected from the original codeset
    return list(code_set[mindex])

#initialize the code set from with al the possible permutations with 6 different "colors"
def ini_population(num_colors,duplicate=False):
    if duplicate:
        population = itertools.product(list(range(0,num_colors)), repeat=4)
    else:
        population = permutations(list(range(0,num_colors)),4)

    return list(population)

def format_state_list(state_list):
    formatted_state_list = []
    
    for each_state in state_list:
        new_state_list =[]
        blacks = each_state[0]
        whites = each_state[1]
        default = 4 - (blacks+whites)
        for i in range(blacks):
            new_state_list.append("black")
        for i in range(whites):
            new_state_list.append("white")
        for i in range(default):
            new_state_list.append("default")
            
        formatted_state_list.append(new_state_list)
    return formatted_state_list
#####################################################
# code: list of 4-digit integers
# duplicate: boolean
# num_colors: integer
def start(code, duplicate=False, num_colors=5 ):
    guess_list=[]
    state_list=[]

    code_set = ini_population(num_colors,duplicate)  # Initialize a set of code set containing possible answer

    # Create a first guess randomly
    guess = givenum(num_colors,duplicate)

    # Get the feedback value with guess and code
    A, B = playresult(code, guess) 

    play_count = 1  # store the value of the number of guessing in this play
    
    guess_list.append(guess)
    state_list.append((A,B))

    while (A < 4):  # Still cleaning the code_set until we find the real answer
        play_count = play_count + 1
        code_set = [t for t in code_set if playresult(t, guess) == (A, B)] 
        
        guess = chooseone(code_set) 
        A, B = playresult(code, guess)     
        guess_list.append(guess)
        state_list.append((A,B))
            
    state_list = format_state_list(state_list)
    return guess_list, state_list 

