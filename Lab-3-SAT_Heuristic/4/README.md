## IMPORTANT INFO REGARDING EXECUTION OF THE PROGRAM 4.py

### NOTATION
* v denotes the logical disjunction operator (OR)
* ^ denotes the logical conjunciton operator (AND)

### SETUP AND EXECUTION
1. Open 4.py in Visual Studio Code.
2. Make sure the required modules/packages are installed.
3. Run the program; there is no user input required.
4. The output includes:
   1. The formula randomly generated (no input file, but a formula can be manually entered at lines 272-276)
   2. The states in path (path length), number of explored states, and the full path (for each search method)

### MODIFIERS (defaults have been set in lines 10 to 15)
* number of clauses can be modified in line 10 (non-zero positive integer)
* length of each clause can be modified in line 11 (range: integer from 1 to 4)
* number of bits perturbed at each flip during moveGen can be modified in line 12 (range: 1 to clause length)
* beam width can be modified in line 13 (non-zero positive integer)
* tabu tenure can be modified in line 14 (duration of non-flipping of bits. range: integer from 1 to 4)
* we can allow in-clause repetition by changing the parameter at line 15
  
NOTE: NOT ALL combinations of the above will work, due to inter-variable constraints in the problem.
