from copy import deepcopy as dc

f = open("200010013.txt", "r+")
line = 0
inf = float('inf')
weight = []
for i in range(5): weight.append([inf for j in range(5)])
for l in f:
    if line==0:
        v, e = [int(i) for i in l.split()]
    elif line<=e:
        a, b, w = [int(i) for i in l.split()]
        weight[a-1][b-1] = w
    line+=1
for i in range(5): weight[i][i]=0
D = dc(weight)
f.close()
f = open("output.txt", "w+")
for m in range(1, 5):
    for i in range(5):
        for j in range(5):
            s = "i" if D[i][j]==inf else str(D[i][j])
            f.write(s+" ")
        f.write("\n")
    f.write("\n")
    temp = dc(D)
    for i in range(5):
        for j in range(5):
            min_val = inf
            for k in range(5):
                min_val = min(min_val, D[i][k]+weight[k][j])
            temp[i][j] = min_val
    D = dc(temp)
f.close()