#s = input()
#n = int(s)

s = open("1.txt","r").read()

l = s.split("\n")
max_x = int(l[0].split(" ")[0])
max_y = int(l[0].split(" ")[1])

map = [[0] * max_x for i in range(max_y)]

n = int(l[1])

for i in range(n):
    x = int(l[2+i].split(" ")[0])
    y = int(l[2+i].split(" ")[1])
    map[y][x] = 1

for y in range(max_y):
    for x in range(max_x):
        if map[y][x] == 0:
            i = 1
            while (y - i >= 0) and (map[y - i][x] == 0):
                i = i + 1
        else:
            i = 0            
        
        if (x != max_x-1):
            print(i, end = " ")
        else:
            print(i)

'''
s = input()

if len(s) == 0:
    exit(0)

max_x = int(s.split(" ")[0])
max_y = int(s.split(" ")[1])

map = [[0] * max_x for i in range(max_y)]

n = int(input())

for i in range(n):
    s = input()
    x = int(s.split(" ")[0])
    y = int(s.split(" ")[1])
    map[y][x] = 1

for y in range(max_y):
    for x in range(max_x):
        if map[y][x] == 0:
            i = 1
            while (y - i >= 0) and (map[y - i][x] == 0):
                i = i + 1
        else:
            i = 0            
        
        if (x != max_x-1):
            print(i, end=" ")
        else:
            print(i)

'''