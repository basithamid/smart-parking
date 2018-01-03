#!/bin/python3

import sys


n = int(input().strip())
unsorted = []
unsorted_i = 0
for unsorted_i in range(n):
   unsorted_t = str(input().strip())
   unsorted.append(unsorted_t)
# your code goes here
int_list = []
for item in unsorted_i:
    list.append(int(item))
int_list = sorted(int_list)
for item in int_list:
    print(item)