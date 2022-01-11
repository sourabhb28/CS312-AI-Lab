import random
from itertools import combinations
import copy
import operator # for helping to sort objects by attribute

formula = []
num_literals = 4            # this can't be readjusted due to the nature of this program

# zone to modify stuff, all greater than zero.
num_clauses = 5
clause_length = 3
perturb_num = 1             # number of bits flipped at each perturbation
bw_def = 2                  # default beam width
tt_def = 3                  # default tabu tenure value
allow_repetition_within = 0 # this allows terms like (A v A V ~B) to be accepted. (1 for yes/ 0 for no)


class state:
    def __init__(self, bitStr):
        self.bitStr = bitStr
        self.heuristic = None
        self.parent = None
        self.ttAtState = None
    
    def __eq__(self, obj2):
        if not isinstance(obj2, state):
            return NotImplemented
        return (self.bitStr == obj2.bitStr)

def litDict(clause):
    ldict = {}
    ldict['A'] = clause[0]
    ldict['B'] = clause[1]
    ldict['C'] = clause[2]
    ldict['D'] = clause[3]
    ldict['~A'] = flipBit(clause[0])
    ldict['~B'] = flipBit(clause[1])
    ldict['~C'] = flipBit(clause[2])
    ldict['~D'] = flipBit(clause[3])
    return ldict

def isVisited(curr_state, closed, open): # checks if curr_state has been visited already or not
    for state in closed:
        if state.bitStr == curr_state.bitStr:
            return True
    for state in open:
        if state.bitStr == curr_state.bitStr:
            return True
    return False

def isExplored(curr_state, closed): # checks if curr_state has been explored already or not
    for state in closed:
        if state.bitStr == curr_state.bitStr:
            return True
    return False

def h_value(state):
    lDict = litDict(state.bitStr)
    clause_value = 0
    # this calculates number of clauses satisfied by the current state's bitString values
    for clause in formula:
        c_sum = 0
        for i in range(clause_length):
            c_sum = c_sum or lDict[clause[i]]
        clause_value = clause_value + c_sum
    return clause_value

def goalTest(state):
    if state.heuristic == num_clauses: # goal state is when all clauses are satisfied
        return True
    else:
        return False

def moveGen(curr_state, perturb_num, tt = None):
    neighbours = []
    all_indices = [0, 1, 2, 3]
    if tt:
        all_combos = list(combinations(all_indices, perturb_num))
        for combo in all_combos:
            state_copy = copy.deepcopy(curr_state)
            for bitIndex in combo:
                if state_copy.ttAtState[bitIndex] == 0:
                    state_copy.bitStr[bitIndex] = flipBit(state_copy.bitStr[bitIndex])
                    state_copy.ttAtState[bitIndex] = tt # once flipped, reset tabu tenure to max tt
                    otherIndices = []                   # to decrement non-zero tt of other indices
                    for index in all_indices:
                        if index not in [bitIndex]:
                            otherIndices.append(index)
                    for index in otherIndices:
                        if state_copy.ttAtState[index] == 0:
                            continue
                        else:
                            state_copy.ttAtState[index] -= 1
                    neighbours.append(state_copy)
        return neighbours
    else:
        all_combos = list(combinations(all_indices, perturb_num)) # choose r number from the index list for perturbation
        for combo in all_combos:
            state_copy = copy.deepcopy(curr_state) # create a copy
            for bitIndex in combo:
                state_copy.bitStr[bitIndex] = flipBit(state_copy.bitStr[bitIndex]) # invert that choosen bit
            neighbours.append(state_copy)
        return neighbours

def backTrack(path, curr_state): # to baktrack during output
    path.append(curr_state.bitStr)
    if curr_state.parent == None:
        return
    else:
        backTrack(path, curr_state.parent)

def flipBit(num): # to flip a bit
    return 1 - num

def neg(literal): # negates a literal
    if literal[0] == '~':
        return literal[1]
    else:
        return '~' + literal

def isTautology(full_clause): # checks if a clause is a tautology
    for l in full_clause:
        if neg(l) in full_clause:
            return True
    return False

def isDuplicate(new_clause): # checks if a clause has already been used in the formula
    for clause in formula:
        if clause == new_clause:
            return True
    return False

def VND(initial_state):
    initial_state.heuristic = h_value(initial_state)
    next_state = [initial_state]
    l = 1
    while True:
        last_state = next_state[-1]

        if goalTest(last_state):
            full_path = []
            backTrack(full_path, last_state)
            print("No. of states in path : " + str(len(full_path)))
            print("No. of states explored : " + str(len(next_state)))
            for ele in list(reversed(full_path)):
                print(ele)
            return True
        
        maxima = last_state
        for neighbour in moveGen(last_state, l): # get neighbours, update heuristic and parent
            neighbour.parent = last_state
            neighbour.heuristic = h_value(neighbour)
            if neighbour.heuristic > maxima.heuristic:
                maxima = neighbour
        
        if not isExplored(maxima, next_state):
            next_state.append(maxima)          # set maximum heuristic valued state
        
        if maxima == last_state:
            l = min(4, l + 1)                  # set wider neighbourhood
        

def beamSearch(initial_state, bw):
    initial_state.heuristic = h_value(initial_state)
    OPEN = [initial_state]
    CLOSED = []
    while OPEN:
        alt_open = []
        for state in OPEN:
            CLOSED.append(state)
            if goalTest(state):
                full_path = []
                backTrack(full_path, state)
                print("No. of states in path : " + str(len(full_path)))
                print("No. of states explored : " + str(len(CLOSED)))
                for ele in list(reversed(full_path)):
                    print(ele)
                return True
            
            for neighbour in moveGen(state, perturb_num):
                if not isVisited(neighbour, CLOSED, OPEN):
                    neighbour.heuristic = h_value(neighbour)
                    neighbour.parent = state
                    alt_open.append(neighbour)
        
        parent_state = OPEN[0]
        OPEN.clear()
        OPEN += alt_open
        # for ele in OPEN:
        #     print(ele.bitStr)
        OPEN.sort(key = operator.attrgetter("heuristic"))
        OPEN = list(reversed(OPEN))
        OPEN = OPEN[:bw]
        if not len(OPEN):
            print("width is zero....")
            return False
        
        if parent_state.heuristic >= OPEN[0].heuristic:
            full_path = []
            backTrack(full_path, state)
            print("No. of states in path : " + str(len(full_path)))
            print("No. of states explored : " + str(len(CLOSED)))
            for ele in list(reversed(full_path)):
                print(ele)
            print("Stuck in local Maxima .... ")
            return False
    return False

def tabuSearch(initial_state, tt=tt_def):
    initial_state.ttAtState = [0, 0, 0, 0]
    initial_state.heuristic = h_value(initial_state)
    curr_state = initial_state
    CLOSED = []
    while True:
        CLOSED.append(curr_state)
        if goalTest(curr_state):
            full_path = []
            backTrack(full_path, curr_state)
            print("No. of states in path : " + str(len(full_path)))
            print("No. of states explored : " + str(len(CLOSED)))
            for ele in list(reversed(full_path)):
                print(ele)
            return True
        alt_curr = curr_state
        max_h = 0
        neighbour_list = moveGen(curr_state, perturb_num, tt)
        for neighbour in neighbour_list: # get neighbours, update heuristic and parent
            neighbour.parent = alt_curr
            neighbour.heuristic = h_value(neighbour)
            if neighbour.heuristic > max_h:
                max_h = neighbour.heuristic
                curr_state = neighbour
        
        if not neighbour_list:
            full_path = []
            backTrack(full_path, curr_state)
            print("No. of states in path : " + str(len(full_path)))
            print("No. of states explored : " + str(len(CLOSED)))
            for ele in list(reversed(full_path)):
                print(ele)
            print("try reducing tt, unable to reach any valid neighbours .... ")
            return False


literals_list = ['A', 'B', 'C', 'D', '~A', '~B', '~C', '~D']

for clause in range(num_clauses):
    flag = 1
    while flag:
        new_clause = []
        # each clause is formed by three of the eight possible literals (formed by 4 variables and their negations)
        for i in range(clause_length):
            # generate a list of 3 random elements of literals_list
            new_clause.append(random.choice(literals_list))
        # but it may be a tautology! need to restart in that case
        if(not allow_repetition_within):
            if (isTautology(new_clause)) or (len(set(new_clause)) != len(new_clause)) or (isDuplicate(new_clause)):
                continue
            else:
                flag = 0
        else:
            if (isTautology(new_clause)) or (isDuplicate(new_clause)):
                continue
            else:
                flag = 0
    formula.append(new_clause)

# manual formula entering zone, with some samples
# formula = [['A', 'B', 'C'], ['A', 'B', 'D'], ['A', 'D', 'C'], ['D', 'B', 'C'], ['A', 'B', 'C']]
# formula = [['A', 'A', 'A'], ['B', 'B', 'B'], ['B', 'B', 'C'], ['C', 'C', 'C'], ['D', 'D', 'D']]
formula = [
['~D', 'B', 'A'],
['D', 'B', '~A'],
['B', 'D', 'C'],
['~D', '~C', 'B'],
['A', 'C', 'D']
]

print("\nThe formula generated is: ", end="")
line = "("
ctr = 0
fp = open("input.txt","w")

for clause in formula:
    ctr += 1
    each_clause = " v ".join(clause)
    line += (each_clause)
    if ctr == num_clauses:
        line += (")")
        break
    line += (") ^ (")
print(line + "\n")

ctr = 0
for clause in formula:
    ctr += 1
    ctr2 = 0
    fp.write("[")
    for lit in clause:
        ctr2 += 1
        fp.write("\'" + str(lit) + "\'")
        if ctr2 == clause_length:
            break
        else:
            fp.write(", ")
    if ctr == num_clauses:
        fp.write("]\n")
        break
    else:
        fp.write("],\n")
    
# print("Pick a search algorithm from the choices:")
# print("0: Variable Neighbourhood Descent")
# print("1: Beam Search")
# print("2: Tabu Search")
# print("Enter your choice: ", end="")
# choice = int(input())
initial_state = state([0, 0, 0, 0])

# neigh = moveGen(initial_state, 1, 2)
# for member in neigh:
#     print(member.bitStr)

# if choice == 0:
#     VND(initial_state)
# elif choice == 1:
#     beamSearch(initial_state, bw_def)
# elif choice == 2:
#     tabuSearch(initial_state, tt_def)
# else:
#     print("Invalid choice!\n")

print("Using Variable Neighbourhood Descent,")
VND(initial_state)
print("\nUsing Beam Search, (beam width = " + str(bw_def) + ")")
beamSearch(initial_state, bw_def)
print("\nUsing Tabu Search, (tabu tenure = " + str(tt_def) + ")")
tabuSearch(initial_state, tt_def)
print("")
            

