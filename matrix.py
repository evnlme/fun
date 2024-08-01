from itertools import product
from typing import List
from permutation import (
    Perm,
    permute
)

Vec = List[float]
Mat = List[Vec]

def matToString(mat: Mat) -> str:
    s = ''
    for row in mat:
        s += '[' + ','.join(map(lambda x: f'{x: .10f}', row)) + '],\n'
    return s

def dot(v1: Vec, v2: Vec) -> float:
    return sum(i1 * i2 for i1, i2 in zip(v1, v2))

def multMat(m1: Mat, m2: Mat) -> Mat:
    m = len(m1)
    n = len(m2[0])
    p = len(m1[0]) # == len(m2)
    return [[
        sum(m1[i][k]*m2[k][j] for k in range(p))
        for j in range(n)]
        for i in range(m)]

def isMatIdentity(mat: Mat) -> bool:
    m = len(mat)
    n = len(mat[0])
    if m != n:
        return False
    for i, j in product(range(m), range(n)):
        v = 1.0 if i == j else 0.0
        if abs(mat[i][j]-v) > 1e-9:
            return False
    return True

def isMatEqual(m1: Mat, m2: Mat) -> bool:
    m = len(m1)
    n = len(m1[0])
    if m != len(m2) or n != len(m2[0]):
        return False
    for i, j in product(range(m), range(n)):
        if abs(m1[i][j] - m2[i][j]) > 1e-9:
            return False
    return True

def permToMat(p: Perm) -> Mat:
    n = len(p)
    mat = [[0.0]*n for _ in range(n)]
    for i, j in enumerate(p):
        mat[i][j] = 1.0
    return mat

def permuteMatRows(p: Perm, mat: Mat) -> None:
    permute(p, arr=mat)

def permuteMatCols(p: Perm, mat: Mat) -> None:
    n = len(p)
    def read(key):
        return [mat[rowId][key] for rowId in range(n)]
    def write(key, value):
        for rowId in range(n):
            mat[rowId][key] = value[rowId]
    permute(p, read=read, write=write)