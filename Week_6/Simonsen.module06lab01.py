# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#1)
import random as rd
rd.seed(10)
int_list = [(rd.randint(0, 15)) for i in range(50)]
print(int_list[10], int_list[30])


#2)
import string as st
az_upper = st.ascii_uppercase
print(az_upper)


az_list=[]
for i in az_upper:
    az_list.append(i)
    
    print(az_list)
    
#3)
set_1 = {1,2,3,4,5}
set_2=set(int_list)

set_3=set_1.symmetric_difference(set_2)

print(len(set_1))
print(len(set_2))
print(len(set_3))

#4)
from collections import defaultdict as dd

def def_value():
    return 'Not Present'

dict_1=dd(def_value)
dict_1.update(int_list=int_list, set_2=set_2, set_3=set_3)

dict_2=dict({'set_1':set_1, 'az_list':az_list})

print(dict_1['az_list'])

set_4=set(dict_1['az_list'])

print(len(dict_2['az_list'])-len(set_4))

dict_2.update(dict_1)
print(dict_2['az_list'])
#The key:value pair weas overwritten in dict_2, thus printing "Not Present". New key:value pairs were added to the dictionary.