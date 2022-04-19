################### IMPORTANT ###################

1. After extracting these files, ensure that the following is true:
    - spambase.data is in the same directory/folder as 4.py.
    - sklearn and pandas are installed on your system. If not installed, use ``` pip install <package-name> ``` .
    - Then, the code can be run in different settings, as explained below.

2. To use one specific pair of kernel and c-value: (using function want_spec())
    - Line 74 should be uncommented, line 75 should be commented out.
    - Set the required (kernel, c) values at lines 8 and 7. Then, run the code.

3. To show all kernels with various c-values: (using function go_thru_all())
    - Line 74 should be commented out, line 75 should be uncommented. Then, run the code.
    - Please wait for the (Linear, 100) and (Linear, 1000) cases to load, as they might take some time.
    - The entire process occurs in about 210 seconds. (Including the above cases that are the time-taking ones).

#### Other Info
* To change degree of polynomial kernel, change polydeg at line 11.
* Possible kernels include: linear , poly , rbf , sigmoid .
* c-values usually used during tweaking of code include: 0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000.

