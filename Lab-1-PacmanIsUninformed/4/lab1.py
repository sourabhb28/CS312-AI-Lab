import sys
import numpy as np

k = 0                  # to get first line as method-input
method = 0
fullMatrix = []
lnNum = 0
colNum = 0
depthMatrix = []
flag = False
stateNum = 0

def moveGen(neighbourDict, node):
    i = node[0]
    j = node[1]

    # obstacles = {'+', '-', '|', '0'} # 0 is pre-taken-over territory, while the others are "wall".
    # node_value = outputMatrix[node[0]][node[1]]

    # check down
    if(i < m-1):
        down_node = fullMatrix[i + 1][j]
        if down_node != 1:
            neighbourDict.append((i+1 , j))

    # check up
    if(i > 0):
        up_node = fullMatrix[i - 1][j]
        if up_node != 1:
            neighbourDict.append((i-1 , j))

    # check right
    if(j < n-1):
        rt_node = fullMatrix[i][j + 1]
        if rt_node != 1:
            neighbourDict.append((i , j+1))

    # check left
    if(j > 0):
        left_node = fullMatrix[i][j - 1]
        if left_node != 1:
            neighbourDict.append((i , j-1))

    neighbourDict = reversed(neighbourDict) # before putting into stack, flip order for D->U->R->L priority
    return neighbourDict
    

def goalTest(node): # node comes as a tuple, can't be directly used to access matrix element. hence, a workaround.
    if fullMatrix[node[0]][node[1]] == 2:
        return True
    else:
        return False

def makePath(parentDict , finalState): # once we reach goal state, let's backtrack all the way to initial state using the parent dictionary
    path = []
    temp = finalState
    pathLength = 0
    while temp != None:
        path.append(temp)

        fullMatrix[temp[0]][temp[1]] = 5

        pathLength += 1
        temp = parentDict.get(temp) # go up a level
    return pathLength

def bfs(node): # node is a tuple of indices of the square
    queue = []
    visited = []
    queue.append(node)
    visited.append(node)
    parentDict = {node: None} # store nodes with their parents in a dictionary. 
    while queue:
        node = queue.pop(0)   # pop first element
        if node not in visited:
            visited.append(node)
        if (goalTest(node)):
            pathLength = makePath(parentDict, node)
            print(len(visited))
            print(pathLength)

            for i in range(0, m+1):
                for j in range(0, n):
                    if fullMatrix[i][j] != 5:
                        print(outputMatrix[i][j], end="")
                    else:
                        print(0, end="")
                print("\n", end="")
            break

        neighbourDict = []
        neighbourDict = moveGen(neighbourDict,node) # get neighbours of node, D->U->R->L priority
        for neighbour in neighbourDict:
            if neighbour not in list(parentDict.keys()):
                parentDict[neighbour] = node        # node is parent of its naighbours
                queue.append(neighbour)             # append in queue for to be visited later
    
def dfs(node):
    stack = []
    visited = []
    stack.append(node)
    visited.append(node)
    parentDict = {node: None} # maintain parents of all nodes in a dictionary 
    stateNum = 0
    while stack:
        node = stack.pop()
        stateNum += 1
        if(goalTest(node)):
            pathLength = makePath(parentDict, node)
            print(stateNum)
            print(pathLength)
            for i in range(0, m+1):
                for j in range(0, n):
                    if fullMatrix[i][j] != 5:
                        print(outputMatrix[i][j], end="")
                    else:
                        print(0, end="")
                print("\n", end="")
            break
        neighbourDict = []
        neighbourDict = moveGen(neighbourDict,node) # get neighbours of current state
        for neighbour in neighbourDict:
            if neighbour not in visited: # not visited node
                if neighbour not in list(parentDict.keys()):
                    parentDict[neighbour] = node
                stack.append(neighbour)
                visited.append(neighbour)

def dls(node, depth): # essentially the same as dfs, except we set a limit on the depth upto which we explore
    global dls_stat
    stack = []
    visited = []
    stack.append(node)
    visited.append(node)
    parentDict = {node: None}
    if(False):
        stateNum = 0
    # steNUM = 0
    # global stateNum
    global depthMatrix
    global flag
    while stack:
        node = stack.pop()
        
        # stateNum = stateNum + 1
        if(goalTest(node)):
            flag = True
            pathLength = makePath(parentDict, node)
            print(dls_stat)
            print(pathLength)
            for i in range(0, m+1): # why m+1???
                for j in range(0, n):
                    if fullMatrix[i][j] != 5:
                        print(outputMatrix[i][j], end="")
                    else:
                        print(0, end="")
                print("\n", end="")
            break
        neighbourDict = []
        neighbourDict = moveGen(neighbourDict,node) # get neighbours of current state
        for neighbour in neighbourDict:
            if (neighbour not in visited) and (depthMatrix[neighbour[0]][neighbour[1]] <= depth): # not visited node
                if neighbour not in list(parentDict.keys()):
                    parentDict[neighbour] = node
                    depthMatrix[neighbour[0]][neighbour[1]] = depthMatrix[node[0]][node[1]] + 1
                stack.append(neighbour)
                visited.append(neighbour)
        dls_stat+=len(visited)

def difs(node): # depth first iterated search is essentially recursive call of depth limited search, by increasing depth-limit
    depth = 0
    exp_states = 0
    global flag
    while not flag:
        dls(node, depth)
        depth = depth + 1


# stateNum = 0
input_graph = sys.stdin.readlines()
outputMatrix = []
k = 0
for line in input_graph:
    colNum = 0
    matrixline = []
    outputline = []
    if k == 0 :
        k = 1
        method = int(line) # for deciding method, use later
        continue
    for char in line:
        if char == ' ':
            matrixline.append(0)
            outputline.append(' ')
        if char == '|' or char == '-' or char == '+':
            matrixline.append(1)
            if char == '|':
                outputline.append('|')
            elif char == '-':
                outputline.append('-')
            elif char == '+':
                outputline.append('+')
        if char == '*':
            goalState = (lnNum, colNum)
            matrixline.append(2)
            outputline.append('*')
        colNum += 1
    fullMatrix.append(matrixline)
    outputMatrix.append(outputline)
    fullMatrix[0][0] = 0
    lnNum += 1
    depthMatrix = fullMatrix
    source = (0, 0)
    depthMatrix[source[0]][source[1]] = 0

    depthMatrix = (-1)*np.array(depthMatrix) # multiplying the matrix by a scalar for easy accessibility of depths

# for each_line in fullMatrix:
#     print(each_line)

m = lnNum - 1
n = colNum - 1
dls_stat=0
flag = False

if method == 0:
    bfs(source)
elif method == 1:
    dfs(source)
elif method == 2:
    difs(source)







    