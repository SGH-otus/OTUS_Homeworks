import random, math

size_1 = 12 # number of values in range
size_2 = 10000 # how many times to repeat

arr = [0] * size_2 # array of values
n = {} # counter of occurrences

for j in range(size_2):
    for i in range(size_1):
        arr[j] = arr[j] + (random.random()) # generates floats in range [0;1)
    arr[j] = (math.sqrt(12 / size_1)) * (arr[j] - (size_1 / 2)) # corresponding to CLT and Habr :)
    
for j in set(arr):
    n[j] = 0 # reset counter of occurrences

for j in range(size_2):
    n[arr[j]] = n[arr[j]] + 1 # calculate occurrences

M = 0    
for j in set(arr):
    M = M + j * n[j] 
M = M / size_2

D = 0 
for j in set(arr):
    D = D + (n[j] * (j - M)**2)
D = D / size_2

print "min = ", sorted(arr)[0]
print "max = ", sorted(arr)[-1]
print "M = ", M 
print "D = ", D
print "SD = ", math.sqrt(D)
