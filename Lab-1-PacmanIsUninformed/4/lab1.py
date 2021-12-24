# This is the main code file

import sys

k = 0
method = 0
fullMatrix = []
lnNum = 0
colNum = 0
class node:
    pass
input_grPH = sys.stdin.readlines()

for line in input_grPH:  
    lnNum+=1
    matrixline = []
    if k == 0 :
        k = 1
        method = int(line)
        continue
    for char in line:
        colNum+=1
        if char == ' ':
            matrixline.append(0)
        if char == '|' or char == '-' or char == '+':
            matrixline.append(1)
        if char == '*':
            goalState = (lnNum, colNum)
            matrixline.append(2)
    fullMatrix.append(matrixline)
    fullMatrix[0][0] = 0
for each_line in fullMatrix:
    print(each_line)
    

    