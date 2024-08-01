from copy import deepcopy
from random import shuffle
from typing import List, Callable, Any

Perm = List[int]

def invertPerm(p: Perm) -> None:
    n = len(p)
    for i in range(n):
        if p[i] < 0:
            continue
        prev = i
        curr = p[prev]
        next = p[curr]
        while True:
            p[curr] = prev-n
            if curr == i:
                break
            prev, curr, next = curr, next, p[next]
    for i in range(n):
        p[i] += n

def invertPermSimple(p: Perm) -> Perm:
    pInv = [0]*len(p)
    for i, j in enumerate(p):
        pInv[j] = i
    return pInv

def permute(p: Perm, **kwargs) -> None:
    n = len(p)
    i: int = kwargs['start'] if 'start' in kwargs else 0
    j: int = kwargs['stop'] if 'stop' in kwargs else n
    read: Callable[[int], Any]
    write: Callable[[int, Any], None]
    if 'read' in kwargs and 'write' in kwargs:
        read = kwargs['read']
        write = kwargs['write']
    elif 'arr' in kwargs:
        arr: List[Any] = kwargs['arr']
        read = arr.__getitem__
        write = arr.__setitem__
    else:
        raise ValueError('Expected "read" and "write" in kwargs.')

    for k in range(i, j):
        if p[k] < 0:
            continue
        prev = k
        curr = p[prev]
        prevValue = read(prev)
        while p[curr] >= 0:
            temp = read(curr)
            write(curr, prevValue)
            prevValue = temp
            prev, curr = curr, p[curr]
            p[prev] -= n
        write(curr, prevValue)
    for k in range(i, j):
        p[k] += n

def _runTest() -> None:
    for n in range(20):
        p = list(range(n))
        shuffle(p)
        pInv = deepcopy(p)
        invertPerm(pInv)
        arr = list(range(n))
        permute(p, arr=arr)
        permute(pInv, arr=arr)
        if arr != list(range(n)):
            print('P   :', p)
            print('P^-1:', pInv)
            print('arr :', arr)
            return
    print('Nice!')

if __name__ == '__main__':
    _runTest()
