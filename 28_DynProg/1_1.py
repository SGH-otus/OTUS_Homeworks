s = "2/100+3/100"
#s = input()

def nod(a, b):
    while (a !=0 ) and (b != 0):
        if a >= b:
            a = a - b
        else:
            b = b - a
    return abs(a - b)

a1 = int(s.split("+")[0].split("/")[0])
a2 = int(s.split("+")[0].split("/")[1])

b1 = int(s.split("+")[1].split("/")[0])
b2 = int(s.split("+")[1].split("/")[1])

t = nod(a2, b2)
znam = (a2 * b2) // t
chisl = a1 * (znam // a2) + b1 * (znam // b2)

t = nod(chisl, znam)

print("{}/{}".format(chisl // t, znam // t))

