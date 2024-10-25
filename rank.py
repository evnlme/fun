import operator as op
from math import ceil, floor
from random import randrange
from typing import List, Optional

def getRank[T](arr: List[T], elem: T, *, left: bool = True) -> int:
    rank = 0
    cmp = op.lt if left else op.le
    for x in arr:
        if cmp(x, elem):
            rank += 1
    return rank

def getPercentile[T](arr: List[T], elem: T, *, left: bool = True) -> float:
    rank = getRank(arr, elem, left=left)
    return rank / len(arr)

def _swap[T](arr: List[T], i: int, j: int) -> None:
    arr[i], arr[j] = arr[j], arr[i]

def _partition[T](arr: List[T], left: int, right: int, pivotIndex: int) -> int:
    pivot = arr[pivotIndex]
    _swap(arr, left, pivotIndex)
    i, j = left+1, right
    while i < j:
        if arr[i] < pivot:
            i += 1
        else:
            _swap(arr, i, j-1)
            j -= 1
    _swap(arr, i-1, left)
    # Left:  [left, i-1)
    # Pivot: [i-1]
    # Right: [i, right)
    return i-1

def _getPivot[T](arr: List[T], left: int, right: int, *, mom: bool) -> int:
    if not mom:
        return randrange(left, right)
    # Median of Medians
    if right - left <= 5:
        mid = (left+right) // 2
        return _select(arr, mid, mom=False, left=left, right=right)
    i = left
    for mLeft in range(left, right, 5):
        mRight = min(mLeft + 5, right)
        mid = (mLeft+mRight) // 2
        medianIndex = _select(arr, mid, mom=False, left=mLeft, right=mRight)
        _swap(arr, medianIndex, i)
        i += 1
    return _select(arr, (left+i) // 2, mom=mom, left=left, right=i)

def _select[T](
    arr: List[T],
    rank: int,
    *,
    mom: bool = True,
    left: Optional[int] = None,
    right: Optional[int] = None,
) -> int:
    left = left or 0
    right = right or len(arr)
    pivotIndex = left
    while left < right:
        pivotIndex = _getPivot(arr, left, right, mom=mom)
        pivotIndex = _partition(arr, left, right, pivotIndex)
        if pivotIndex == rank:
            return pivotIndex
        elif pivotIndex < rank:
            left = pivotIndex + 1
        else: # pivotIndex > rank
            right = pivotIndex
    return pivotIndex

def getElemAtRank[T](arr: List[T], rank: int) -> T:
    pivotIndex = _select(arr, rank, mom=True)
    return arr[pivotIndex]

def getElemAtPercentile[T](arr: List[T], percentile: float) -> T:
    rankF = percentile * len(arr)
    # Floor is used here but ceil can also work.
    rank = floor(rankF)
    return getElemAtRank(arr, rank)
