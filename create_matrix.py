import pandas as pd
import json
import numpy as np
import random
from copy import deepcopy

pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 20)

#file_name = 'constraint_inp1.json'

def create_matrix_constraints(data:list[dict]):
    
    matrix = pd.DataFrame(data)
    matrix_profs = create_matrix_profs(matrix)
    matrix_class_profs = create_matrix_class_profs(matrix)

    # print(matrix_profs)
    # print(matrix_class_profs)

    return matrix_class_profs, matrix_profs

def create_matrix_profs(matrix, max_period = 5):

    profs = list(matrix['Professor'].unique())
    mat_profs = np.zeros((len(profs), 60), dtype = np.int64)
    mat_profs = np.array(list(map(lambda x: func_util(x, np.random.randint(0, max_period + 1)), mat_profs)))

    matrix_profs = pd.DataFrame(pd.Series(mat_profs.tolist(), index=profs), columns=["Period"])
    return matrix_profs

def create_matrix_class_profs(matrix):

    Time_periods = [1,2,3]
    mat = deepcopy(matrix)
    mat['Period'] = mat['Duration']
    
    matrix_typeP = mat[mat['Type'] == 'P']
    matrix_typeP['Period'] = matrix_typeP['Duration'].apply(lambda x: int(x) * np.random.choice(Time_periods)) 

    for idx in matrix_typeP.index:
        mat.loc[idx, 'Period'] = matrix_typeP.loc[idx, 'Period']
    
    profs = list(mat['Professor'].unique())
    size_row, size_col = len(mat), len(profs)
    matrix_class_profs = pd.DataFrame(np.zeros((size_row, size_col), dtype=np.int64).tolist(), columns = profs)

    for idx in range(len(mat)):
        matrix_class_profs.loc[idx, mat.loc[idx, 'Professor']] = mat.loc[idx, 'Period']

    return matrix_class_profs

def func_util(lst: list[int], max_period_busy: int) -> list[int]:
    busy_periods = np.random.randint(0, max_period_busy + 1)
    lst_busy_periods = random.sample(range(len(lst)), busy_periods)

    for idx in lst_busy_periods:
        lst[idx] = 1
    return lst


