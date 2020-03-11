#s = input()
#n = int(s)

s = open("1.txt","r").read()

l = s.split("\n")
n = int(l[0]) 

arr = [0] * n
for i in range(n):
    arr[i] = int(l[i + 1])
    
print (0),    
    
for i in range(1, n):
    t = i - 1
    while (arr[t] >= arr[i]) and (t >= 0):
        t = t - 1
    if i != n - 1:
        print (t + 1),
    else:
        print (t + 1)

for i in range(0, n - 1):
    t = i + 0
    while (arr[t + 1] >= arr[i]):
        t = t + 1
        if (t == n - 1):
            break
    print (t),

print (n - 1)