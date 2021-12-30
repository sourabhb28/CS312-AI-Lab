import sys
import copy
import time

class state:
    def __init__(self, stack1, stack2, stack3):
        self.stack1 = stack1
        self.stack2 = stack2
        self.stack3 = stack3
        self.heuristic = None
        self.parent = None

def goalTest(curr_state, goal_state): # six different permutations need to be considered since the order of the stacks shouldn't matter

    if(curr_state.stack1 == goal_state.stack1):
        if(curr_state.stack2 == goal_state.stack2 and curr_state.stack3 == goal_state.stack3):
                return True
        elif(curr_state.stack2 == goal_state.stack3 and curr_state.stack3 == goal_state.stack2):
                return True
        else:
            return False
    
    elif(curr_state.stack2 == goal_state.stack2):
        if(curr_state.stack1 == goal_state.stack1 and curr_state.stack3 == goal_state.stack3):
                return True
        elif(curr_state.stack1 == goal_state.stack3 and curr_state.stack3 == goal_state.stack1):
                return True
        else:
            return False

    elif(curr_state.stack3 == goal_state.stack3):
        if(curr_state.stack1 == goal_state.stack1 and curr_state.stack2 == goal_state.stack2):
                return True
        elif(curr_state.stack1 == goal_state.stack2 and curr_state.stack2 == goal_state.stack1):
                return True
        else:
            return False

    elif(curr_state.stack1 == goal_state.stack2 and curr_state.stack2 == goal_state.state3 and curr_state.stack3 == goal_state.stack1):
        return True

    elif(curr_state.stack1 == goal_state.stack3 and curr_state.stack2 == goal_state.state1 and curr_state.stack3 == goal_state.stack2):
        return True

    else:
        return False

def moveGen(curr_state):
    # moveGen() always populates neighbours for the current state and returns a list or array of neighbours
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

def bestFirstSearch():
    pass

file = open(sys.argv[1], "r")

method = int(file.readline())

s1 = file.readline().split(" ")
s2 = file.readline().split(" ")
s3 = file.readline().split(" ")

initial_state = state(s1, s2, s3)

g1 = file.readline().split(" ")
g2 = file.readline().split(" ")
g3 = file.readline().split(" ")

goal_state = state(g1, g2, g3)

if method == 1:
    timestamp_0 = time.time()
    bestFirstSearch(initial_state, goal_state)
    timestamp_t = time.time()
    print("Time taken (via best first search) is: ", timestamp_t-timestamp_0)