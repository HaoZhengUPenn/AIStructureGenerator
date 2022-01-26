import numpy as np
import scipy.linalg
import sympy
from numpy import dot, zeros
from numpy.linalg import matrix_rank, norm
import os
import sys

def import_matrix_from_txt(path):
    result = []
    file = open(path,"r")
    lines = file.readlines()
    #print("There are {} rows in the matrix.".format(len(lines)))
    for line in lines:
        lst = line.split(",")
        new_list = []
        for i in lst:
            new_list.append(float(i.strip()))
        result.append(new_list)
    file.close()
    return result

def import_vector_from_text(path):
    result = []
    file = open(path,"r")
    lines = file.readlines()
    for line in lines:
        result.append(float(line.strip()))
    file.close()
    return result

def export_list_to_text(lst, file_path):
    file = open(file_path, "w")
    for item in lst:
        file.write(str(item)+"\n")
    file.close()

path = os.path.dirname(os.path.abspath(__file__))+"\\"

file_path = path+"equilibrium_matrix.txt"
matrix_as_list = import_matrix_from_txt(file_path)

matrix = np.array(matrix_as_list)
j_3,b = matrix.shape
r = np.linalg.matrix_rank(matrix)

print(j_3)
print("The statical indeterminacy is {}.".format(b-r))
print("The kinematical indeterminacy is {}.".format(j_3-r))

file_path_force = path+"pellegrino_applied_load.txt"
applied_load = import_vector_from_text(file_path_force)
force_vec = np.array(applied_load, ndmin=2)
force_vec = force_vec.reshape(-1,1)
# print(force_vec)
tension_vec, residual, rank, s= np.linalg.lstsq(matrix,force_vec)
tension_vec = tension_vec.T
print(tension_vec)
tension_vec = tension_vec[0]
tension_vec[np.abs(tension_vec)>1e15] = 0
export_list_to_text(tension_vec, path+"pellegrino_modified_tension.txt")

# input()