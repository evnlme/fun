import random
from copy import deepcopy
from typing import Tuple
from permutation import (
    Perm,
    invertPerm,
    permute,
)
from matrix import (
    Mat,
    multMat,
    matToString,
    isMatIdentity,
    isMatEqual,
    permuteMatCols,
    permuteMatRows,
)

def _findPivot(mat: Mat, k: int, n: int) -> int:
    value = abs(mat[k][k])
    valueId = k
    for rowId in range(k, n):
        row = mat[rowId]
        if abs(row[k]) > value:
            value = abs(row[k])
            valueId = rowId
    return valueId

def _elim(l: Mat, u: Mat, k: int, n: int) -> None:
    for rowId in range(k+1, n):
        c = u[rowId][k] / u[k][k]
        l[rowId][k] = c
        u[rowId][k] = 0
        for colId in range(k+1, n):
            u[rowId][colId] -= c*u[k][colId]

def _permute(p: Perm, l: Mat, k: int, n: int) -> None:
    def read(key):
        return l[key][k]
    def write(key, value):
        l[key][k] = value
    permute(p, i=k+1, j=n, read=read, write=write)

def _plu(p: Perm, l: Mat, u: Mat, k: int, n: int) -> None:
    if k == n:
        return
    pivotRowId = _findPivot(u, k, n)
    u[k], u[pivotRowId] = u[pivotRowId], u[k]
    _elim(l, u, k, n)
    _plu(p, l, u, k+1, n)
    _permute(p, l, k, n)
    p[k], p[pivotRowId] = p[pivotRowId], p[k]

def plu(mat: Mat) -> Tuple[Perm, Mat, Mat]:
    n = len(mat)
    p = list(range(n))
    l = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    u = deepcopy(mat)
    _plu(p, l, u, 0, n)
    invertPerm(p)
    return p, l, u

def invertUpper(u: Mat) -> Mat:
    n = len(u)
    mat = [[0.0]*n for _ in range(n)]
    for k in range(n):
        mat[k][k] = 1 / u[k][k]
        i = k - 1
        while i >= 0:
            mat[i][k] = -sum(u[i][j]*mat[j][k] for j in range(k, i, -1)) / u[i][i]
            i -= 1
    return mat

def invertLower(l: Mat) -> Mat:
    n = len(l)
    mat = [[0.0]*n for _ in range(n)]
    for k in range(n):
        mat[k][k] = 1 / l[k][k]
        i = k + 1
        while i < n:
            mat[i][k] = -sum(l[i][j]*mat[j][k] for j in range(0, i)) / l[i][i]
            i += 1
    return mat

def invertMat(mat: Mat) -> Mat:
    p, l, u = plu(mat)
    lInv = invertLower(l)
    uInv = invertUpper(u)
    matInv = multMat(uInv, lInv)
    permuteMatCols(p, matInv)
    return matInv

def _debug(mat: Mat, matInv: Mat, iden: Mat) -> None:
    print('Size:', len(mat))
    p, l, u = plu(mat)
    lu = multMat(l, u)
    permuteMatRows(p, lu)
    if isMatEqual(mat, lu):
        print('PLU ok.')
    else:
        print('Mat:')
        print(matToString(mat))
        print('PLU:')
        print(matToString(lu))
        print('P:', p)
        print('LU:')
        print(matToString(multMat(l, u)))

    lInv = invertLower(l)
    if isMatIdentity(multMat(lInv, l)):
        print('L: ok.')
    else:
        print('L:')
        print(matToString(l))
        print('L^-1:')
        print(matToString(lInv))

    uInv = invertUpper(u)
    if isMatIdentity(multMat(uInv, u)):
        print('U: ok.')
    else:
        print('U:')
        print(matToString(u))
        print('U^-1:')
        print(matToString(uInv))

    print('Iden:')
    print(matToString(iden))

def _runTest() -> None:
    for n in range(1, 20):
        # Low probability of being singular.
        mat = [[random.random()*2.0 - 1.0 for j in range(n)] for i in range(n)]
        matInv = invertMat(mat)
        # Right inverse makes permutation issues easier to debug.
        iden = multMat(mat, matInv)
        if not isMatIdentity(iden):
            _debug(mat, matInv, iden)
            return
    print('Nice!')

if __name__ == '__main__':
    _runTest()
