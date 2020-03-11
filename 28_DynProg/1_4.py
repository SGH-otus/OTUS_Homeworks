#s = input()
#n = int(s)

s = open("1.txt","r").read()

l = s.split("\n")
n = int(l[0])

map = [[0] * n for i in range(n)]

for i in range(n):
    s = l[i+1].replace(" ", "")
    #s = input()
    #s = s.replace(" ", "")
    for j in range(len(s)):
        map[i][j] = int(s[j])

def walk(x,y):
    if (x < 0) or (x >= n):
        return
    if (y < 0) or (y >= n):
        return
    if map[x][y] == 0:
        return
    map[x][y] = 0
    walk(x - 1, y)
    walk(x + 1, y)
    walk(x, y - 1)
    walk(x, y + 1)
    
isl = 0    
    
for i in range(n):
    for j in range(n):
        if map[i][j] == 1:
            isl = isl + 1
            walk(i, j)
print(isl)
