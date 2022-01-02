import sys
import copy
import time
from queue import PriorityQueue

class state:
    def __init__(self, stack1, stack2, stack3):
        self.stack1 = stack1
        self.stack2 = stack2
        self.stack3 = stack3
        self.heuristic = None
        self.parent = None


def goalTest(curr_state, goal_state):

    if(curr_state.stack1 == goal_state.stack1):
        if(curr_state.stack2 == goal_state.stack2 and curr_state.stack3 == goal_state.stack3):
            return True
        # elif(curr_state.stack2 == goal_state.stack3 and curr_state.stack3 == goal_state.stack2):
        #         return True
        else:
            return False
    
    # elif(curr_state.stack2 == goal_state.stack2):
    #     if(curr_state.stack1 == goal_state.stack1 and curr_state.stack3 == goal_state.stack3):
    #             return True
    #     elif(curr_state.stack1 == goal_state.stack3 and curr_state.stack3 == goal_state.stack1):
    #             return True
    #     else:
    #         return False

    # elif(curr_state.stack3 == goal_state.stack3):
    #     if(curr_state.stack1 == goal_state.stack1 and curr_state.stack2 == goal_state.stack2):
    #             return True
    #     elif(curr_state.stack1 == goal_state.stack2 and curr_state.stack2 == goal_state.stack1):
    #             return True
    #     else:
    #         return False

    # elif(curr_state.stack1 == goal_state.stack2 and curr_state.stack2 == goal_state.state3 and curr_state.stack3 == goal_state.stack1):
    #     return True

    # elif(curr_state.stack1 == goal_state.stack3 and curr_state.stack2 == goal_state.state1 and curr_state.stack3 == goal_state.stack2):
    #     return True

    else:
        return False

def moveGen(curr_state):
    # moveGen() populates neighbours for the current state and returns a list or array of neighbours
    neighbours = []
    
    if curr_state.stack1:                     # if stack1 is non-empty, we can pop an element and push to other two stacks
        state_copy = copy.deepcopy(curr_state)
        top_1 = state_copy.stack1.pop()
        state_copy.stack2.append(top_1)
        neighbours.append(state_copy)

        state_copy = copy.deepcopy(curr_state)
        top_1 = state_copy.stack1.pop()
        state_copy.stack3.append(top_1)
        neighbours.append(state_copy)

    if curr_state.stack2:                     # if stack2 is non-empty, we can pop an element and push to other two stacks
        state_copy = copy.deepcopy(curr_state)
        top_2 = state_copy.stack2.pop()
        state_copy.stack1.append(top_2)
        neighbours.append(state_copy)

        state_copy = copy.deepcopy(curr_state)
        top_2 = state_copy.stack2.pop()
        state_copy.stack3.append(top_2)
        neighbours.append(state_copy)

    if curr_state.stack3:                     # if stack2 is non-empty, we can pop an element and push to other two stacks
        state_copy = copy.deepcopy(curr_state)
        top_3 = state_copy.stack3.pop()
        state_copy.stack1.append(top_3)
        neighbours.append(state_copy)

        state_copy = copy.deepcopy(curr_state)
        top_3 = state_copy.stack3.pop()
        state_copy.stack2.append(top_3)
        neighbours.append(state_copy)

    return neighbours

def h_fun1(curr_state, goal_state):
    h = 0
    for curr, goal in zip([curr_state.stack1, curr_state.stack2, curr_state.stack3], [goal_state.stack1, goal_state.stack2, goal_state.stack3]):
        height = 0
        struct_below = False
        for block in curr:
            try:
                goal_block = goal[height]
            except:
                goal_block = None
            
            if block == goal_block and struct_below == False:
                h = h + (len(curr) - height)
            else:
                h = h - (len(curr) - height)
                struct_below = True
            height+=1
    return h

def backTrack(path, curr_state):
    path.append(curr_state)
    if curr_state.parent == None:
        return
    else:
        backTrack(path, curr_state.parent)

def bestFirstSearch(init_state, goal_state):
    open = PriorityQueue()
    explored = []
    h_value = h_fun1(goal_state, goal_state) - h_fun1(init_state, goal_state)
    open.put((h_value, init_state))
    while not open.empty():
        h_curr, state_curr = open.get()
        
        explored.append(state_curr)
        if goalTest(state_curr, goal_state):
            path = []
            backTrack(path, state_curr)
            print("No. of states in path: "+ (len(path)))
            print("No. of explored states: "+ (len(explored)))
        
            for stat in reversed(path):
                for block in stat.stack1:
                    print(str(block))
                print("")
            return True

        for neighbour_state in moveGen(state_curr):
            visited = 0
            for stat in explored:
                if stat.stack1 == state_curr.stack1 and stat.stack2 == state_curr.stack2 and stat.stack3 == state_curr.stack3:
                    visited = 1
            for (h_val, stat) in open.queue:
                if stat.stack1 == state_curr.stack1 and stat.stack2 == state_curr.stack2 and stat.stack3 == state_curr.stack3:
                    visited = 1

            if visited == 0:
                h_val = h_fun1(goal_state, goal_state) - h_fun1(neighbour_state, goal_state)
                neighbour_state.parent = state_curr
                open.put((h_val, neighbour_state))
    return False

file = open("input1.txt", "r")

method = int(file.readline())

s1 = file.readline().strip().split() #remove readline and get values into stacks
s2 = file.readline().strip().split()
s3 = file.readline().strip().split()

initial_state = state(s1, s2, s3)

g1 = file.readline().strip().split()
g2 = file.readline().strip().split()
g3 = file.readline().strip().split()

goal_state = state(g1, g2, g3)

if method == 1:
    timestamp_0 = time.time()
    bestFirstSearch(initial_state, goal_state)
    timestamp_t = time.time()
    print("Time taken (via best first search) is: ", timestamp_t-timestamp_0)