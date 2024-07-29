"""
Automatic function compositions so you don't have to write them yourself.

Algorithm: Unweighted Floyd-Warshall. All pairs shortest path.
Remark: If the base functions have costs like runtime, a weighted version is possible.
"""

from functools import reduce
from itertools import product
from typing import Any, List, Callable, Tuple, Dict

AutoCompInput = List[Tuple[Callable[[Any], Any], str, str]]
AutoCompOutput = Callable[[Any, str, str], Any]

def compose(*funcs: Callable[[Any], Any]) -> Callable[[Any], Any]:
    return reduce(lambda f, g: lambda x: g(f(x)), funcs)

def createComps(funcs: AutoCompInput) -> AutoCompOutput:
    vertIdMap: Dict[str, int] = dict()
    vertList: List[str] = list()
    compMap: Dict[Tuple[str, str], Callable[[Any], Any]] = dict()
    for _, src, dst in funcs:
        if src not in vertIdMap:
            vertIdMap[src] = len(vertIdMap)
            vertList.append(src)
        if dst not in vertIdMap:
            vertIdMap[dst] = len(vertIdMap)
            vertList.append(dst)

    n = len(vertList)
    # Table for tracking costs (e.g., weights, distances)
    table = [[n]*n for _ in range(n)]
    for f, src, dst in funcs:
        i = vertIdMap[src]
        j = vertIdMap[dst]
        table[i][j] = 1
        compMap[(src, dst)] = f
    for i, src in enumerate(vertList):
        table[i][i] = 0
        compMap[(src, src)] = lambda x: x

    for k in range(n):
        for i, j in product(range(n), range(n)):
            cost = table[i][k] + table[k][j]
            if cost < table[i][j]:
                table[i][j] = cost
                src = vertList[i]
                dst = vertList[j]
                vert = vertList[k]
                f = compMap[(src, vert)]
                g = compMap[(vert, dst)]
                compMap[(src, dst)] = compose(f, g)

    def _comp(v: Any, src: str, dst: str) -> Any:
        if (src, dst) in compMap:
            return compMap[(src, dst)](v)
        else:
            raise Exception('Composition does not exist:', (src, dst))
    return _comp

def runTests() -> None:
    funcs1 = [
        (lambda x: x+1, 'zero', 'one'),
        (lambda x: x+9, 'one', 'ten'),
        (lambda x: x-10, 'ten', 'zero'),
    ]
    comps1 = createComps(funcs1)
    samples1 = [
        ((1, 'one', 'zero'), 0),
        ((10, 'ten', 'zero'), 0),
        ((0, 'zero', 'ten'), 10),
    ]
    for x, y in samples1:
        if comps1(*x) != y:
            print('Error:', x, y)

runTests()
