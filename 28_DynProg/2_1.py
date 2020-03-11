#s = input()
#n = int(s)

s = open("1.txt","r").read()

l = s.split("\n")
max_x = int(l[0].split(" ")[0])
max_y = int(l[0].split(" ")[1])

map = [[0] * max_x for i in range(max_y)]

for i in range(max_y):
    s = l[i+1].replace(" ", "")
    #s = input()
    #s = s.replace(" ", "")
    for j in range(len(s)):
        map[i][j] = int(s[j])

max_t = 0

for x0 in range(max_x):
    for y0 in range(max_y):
        t = 0
        if map[y0][x0] == 0:
            x = 0
            min_h = max_y + 1
            while (x0 + x < max_x) and (map[y0][x0 + x] == 0):
                y = 1
                while (y0 + y < max_y) and (map[y0 + y][x0 + x] == 0):
                    y = y + 1
                if y < min_h:
                    min_h = y
                
                x = x + 1

            t = (x + 0) * min_h
            #print x0,y0,min_h,t
        
            if t > max_t:
                max_t = t
    

print(max_t)
