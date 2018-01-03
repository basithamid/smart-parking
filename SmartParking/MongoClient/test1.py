import sys

def getRecord(s):
    max = min = s[0]
    count_min = count_max = 0
    for i in s:
        if i < min:
            min = i
            count_min = count_min + 1
        if i > max:
            max = i
            count_max = count_max + 1
    return [ count_max, count_min]


n = int(input().strip())
s = list(map(int, input().strip().split(' ')))
result = getRecord(s)
print (" ".join(map(str, result)))
