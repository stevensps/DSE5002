# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 11:47:02 2024

@author: steve
"""
"""
if the iteration of i is equal to the reverse iteration of i, then print
the string is a palindrome 
"""
#1
def palindrome(word): #function definition, no default value one string argument
     #code block that converts all string to lower, eliminates space, iterates over the word, appends to list
    word=word.lower().replace(" ","")
    forward=[]
    for i in word:
        forward.append(i)
    #If statement compares forward and backwards spelling and prints whether word is a palindrome    
    if(forward == list(reversed(forward))):
        print('The selected word or phrase is a palindrome')
    else:
        print('The selected word or phrase is not a palindrome')

palindrome(word='Racecar')

#2

def wpalendrome(word): #function definition, no default value one string argument
     #code block converts all string to lower, eliminates space, creates reverse version of the string
    clean_word=word.lower().replace(" ","")
    reversed_word=clean_word[::-1]
    #if the forward version doesn't equal reverse version, print no palendrome then break to exit loop.
    #Otherwise, print that it is a palendrome
    while clean_word != reversed_word:
        print("The selected word or phrase is not a palendrome")
        break
    else:
        print("The selected word or phrase is a palendrome")
        
        
        
        
wpalendrome(word='racecar')

wpalendrome(word='Racecar')

wpalendrome(word='Race car')

wpalendrome(word='Steven')

#3
list_1 = [2,7,11,15]
target=9

from collections import defaultdict 

def two_sum(list_1, target): #function definition, no default value and two arguments
    #Code block - assign hashmap to 0, iterate over list. Add value to hash if not already present
    hash_map=defaultdict(int)
    work_on = 0
    for i, num in enumerate(list_1):
        work_on += 1
        complement = target - num
        if complement in hash_map:
            #Print complement which is index in hash and i which is orig index.
            print(hash_map[complement],i)
        else:
            hash_map[num]=i
            
two_sum(list_1, target)

#4
"""
Here is an example as used from Question 2 above. The reversed word variable uses the syntax [::-1], whichs slices in reverse order.
- The first argument indicates the starting index where the slice begins
- The second argument indicates the ending index where the slice ends
- The third argument (-1 in this example), is the step size. Typically this is defaulted to 1, but -1 indicates that we want to reverse the order of the iteration sequence.
"""
"""
clean_word=word.lower().replace(" ","")
    reversed_word=clean_word[::-1]
"""


#5
def isomorph(str1, str2): #function definition, no default value and two arguments
    #Code block 1 - check length of string to ensure equality
    if len(str1) != len(str2):
        return False
    
    #Code block 2 - create set from strings, iterate over both using zip and each character within strings.
    #Ord converts unicode to integer values. Differences should only be length 1 if isomorphic
    differences = set(ord(char1) - ord(char2) for char1, char2 in zip(str1, str2))
    return len(differences) == 1 

print(isomorph("aab", "xxy"))

print(isomorph("adb", "xxy"))
      
















