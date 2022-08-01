import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

# for one specific run
c_val = 10.0
k_val = "linear"

# to change the degree of polynomial kernel
polydeg = 2

data = pd.read_csv("spambase.data", header = None) # get data

x = data.iloc[:,:-1]         # get all columns except last
y = data.iloc[:,-1]          # get last column

# feature scaling to standardize/normalize all feature values
scalar = StandardScaler()
x = scalar.fit_transform(x)

# split given dataset into training set (70%) and testing set (30%)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3)

def want_spec():
    # Model declaration and training:
    model = SVC(C = c_val, degree = polydeg, kernel = k_val)
    model.fit(x_train, y_train)
    # get prediction score on test dataset
    sc = model.score(x_test, y_test)
    st = model.score(x_train, y_train)
    print("C: " + str(c_val))
    print("Kernel: " + str(k_val))
    print("Training Accuracy: " + str(st))
    print("Testing Accuracy: " + str(sc))

def go_thru_all():
    c_array = [0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0]
    k_array = ["linear", "poly", "rbf", "sigmoid"]
    print()
    print("Format of the below output lines:")
    print("[kernel_name, c-value, training accuracy, testing accuracy]")
    print("__________________________________________________________________________________")
    for k in k_array:
        best_c = 0.001
        best_acc = 0.0
        best_st = 0.0
        for c_v in c_array:
            line = []
            line.append(k)
            line.append(c_v)
            # Model declaration and training:
            model = SVC(C = c_v, degree = polydeg, kernel = k)
            model.fit(x_train, y_train)
            sc = model.score(x_test, y_test)
            st = model.score(x_train, y_train)
            if sc > best_acc:
                best_acc = sc
                best_c = c_v
                best_st = st
            line.append(st)
            line.append(sc)
            print(line)
        print("For the " + str(k) + " kernel,")
        print("Best value of c is: " + str(best_c))
        print("Training Accuracy: " + str(best_st))
        print("Testing Accuracy: " + str(best_acc))
        print("________________________________________________")


import time 
start = time.time()

#want_spec()
go_thru_all()

end = time.time()
print("\nTime taken: " + str(end-start))