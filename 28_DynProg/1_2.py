#s = input()
#c = int(s)

s = open("1.txt","r").read()

l = s.split("\n")
c = int(l[0])

d = [[0] * c for i in range(c)]

for i in range(c):
    s = l[i+1].replace(" ", "")
    #s = input()
    #s = s.replace(" ", "")
    for j in range(len(s)):
        d[i][j] = int(s[j])

for i in range(c-2,-1,-1):
    for j in range(i+1):
        d[i][j] = d[i][j] + max(d[i+1][j],d[i+1][j+1])

print(d[0][0])

