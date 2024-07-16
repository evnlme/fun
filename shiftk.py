"""
Consideration: Finetuning memory access patterns may speed things up by avoiding cache
misses. Though, you probably want to run a perf test first to see if the optimizations
are necessary.
"""
from math import gcd
from typing import List, Any

def swap(arr: List[Any], i: int, j: int) -> None:
    """In-place swap. Swaps[1]."""
    arr[i], arr[j] = arr[j], arr[i]

def shift_cycle(arr: List[Any], k: int) -> None:
    """In-place shift. Swaps[n-gcd(n,k)]."""
    n = len(arr)
    k = (-k % n + n) % n
    if n == 0 or k == 0:
        return
    m = gcd(n, k)
    for j in range(m):
        i = (j + k) % n
        while i != j:
            i_next = (i + k) % n
            swap(arr, i, i_next)
            i = i_next

def shift_simple(arr: List[Any], k: int) -> List[Any]:
    n = len(arr)
    k = (-k % n + n) % n
    return arr[k:] + arr[:k]

def _reverse(arr: List[Any], i: int, j: int) -> None:
    """In-place reverse. Swaps[(j-i)/2]."""
    while i < j:
        swap(arr, i, j)
        i += 1
        j -= 1

def shift_reverse(arr: List[Any], k: int) -> None:
    """In-place shift.

    Swaps[(n-1)/2+(k-1)/2+(n-k-1)/2] <= Swaps[n-1/2].
    """
    n = len(arr)
    k = (k % n + n) % n
    if n == 0 or k == 0:
        return
    _reverse(arr, 0, n-1)
    _reverse(arr, 0, k-1)
    _reverse(arr, k, n-1)

nk = [
    (5, 0),
    (5, 2),
    (5, 6),
    (5, -3),
    (5, -7),
    (12, 4),
    (12, 5),
    (12, 6),
]

def check(n: int, k: int) -> None:
    arr = list(range(n))
    arr_simple = shift_simple(arr, k)
    arr_cycle = list(arr)
    shift_cycle(arr_cycle, k)
    arr_reverse = list(arr)
    shift_reverse(arr_reverse, k)
    if arr_cycle != arr_simple:
        print(f'Cycle {n} {k}:')
        print(arr_cycle)
        print(arr_simple)
    if arr_reverse != arr_simple:
        print(f'Reverse {n} {k}:')
        print(arr_reverse)
        print(arr_simple)

for n, k in nk:
    check(n, k)
