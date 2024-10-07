"""Red-Black Tree implementation.

Be careful with variable reuse after rotation.
"""
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

class RBSide(Enum):
  LEFT: bool = False
  RIGHT: bool = True

  @staticmethod
  def flip(side: 'RBSide') -> 'RBSide':
    return RBSide.LEFT if side.value else RBSide.RIGHT

class RBColor(Enum):
  BLACK: bool = False
  RED: bool = True

  @staticmethod
  def flip(color: 'RBColor') -> 'RBColor':
    return RBColor.BLACK if color.value else RBColor.RED

@dataclass
class RBNode[KT, VT]:
  key: KT
  value: VT
  left: Optional['RBNode[KT, VT]'] = None
  right: Optional['RBNode[KT, VT]'] = None
  parent: Optional['RBParent[KT, VT]'] = None

  def __str__(self) -> str:
    node = self
    side = ''
    depth = 0
    stack = []
    lines = []
    while node or stack:
      if node is None:
        node, depth = stack.pop()
        side = 'R'
      else:
        color = '+' if getColor(node) == RBColor.RED else ''
        line = f'{side}({node.key}, {node.value}){color}'
        lines.append(' '*(2*depth) + line)
        if node.right:
          stack.append((node.right, depth+1))
        node = node.left
        side = 'L'
        depth += 1
    return '\n'.join(lines)

  @property
  def side(self) -> Optional[RBSide]:
    return self.parent.side if self.parent else None

  @side.setter
  def side(self, value: RBSide) -> None:
    if self.parent:
      self.parent.side = value

  def setChild(self, side: RBSide, child: Optional['RBNode']) -> None:
    if side == RBSide.LEFT:
      self.left = child
    else: # side == RBSide.RIGHT
      self.right = child

  def getChild(self, side: RBSide) -> Optional['RBNode']:
    if side == RBSide.LEFT:
      return self.left
    else: # side == RBSide.RIGHT
      return self.right

  def clear(self) -> None:
    self.left = None
    self.right = None
    self.parent = None

  def successor(self) -> 'RBNode':
    prevNode = self
    node = self.right
    while node is not None:
      prevNode = node
      node = node.left
    return prevNode

  def isAdjacent(self, node: 'RBNode') -> Optional['RBNode']:
    if self.parent and self.parent.node == node:
      return self
    if node.parent and node.parent.node == self:
      return node
    return None

@dataclass
class RBParent[KT, VT]:
  node: RBNode[KT, VT]
  side: RBSide
  color: RBColor = RBColor.BLACK

  def reparent(self, child: Optional[RBNode]) -> None:
    self.node.setChild(self.side, child)
    if child is not None:
      child.parent = self

def getColor(node: Optional[RBNode]) -> RBColor:
  if node is None or node.parent is None:
    return RBColor.BLACK
  return node.parent.color

def setColor(node: Optional[RBNode], value: RBColor) -> None:
  if node is None or node.parent is None:
    return
  node.parent.color = value

@dataclass
class RBTree[KT, VT]:
  root: Optional[RBNode[KT, VT]] = None

  def __str__(self) -> str:
    return str(self.root)

  def _reparent(self, parent: Optional[RBParent], child: Optional[RBNode]) -> None:
    if parent is None:
      self.root = child
      if child is not None:
        child.parent = None
    else:
      parent.reparent(child)

  def _rotate(self, node: RBNode) -> None:
    """Rotate node with its parent.

    If node is red, black height is invariant under rotation.
    If node is black, black height will change for the following subtrees:
      Left rotation: Left subtree +1, Middle subtree 0, Right subtree -1.
      Right rotation: Left subtree -1, Middle subtree 0, Right subtree +1.
    """
    if node.parent is None:
      return
    parentNode = node.parent.node
    middleNode = node.getChild(RBSide.flip(node.side))
    nodeParent = parentNode.parent
    parentParent = RBParent(node, RBSide.flip(node.side), getColor(node))
    middleParent = RBParent(parentNode, node.side, getColor(middleNode))
    self._reparent(nodeParent, node)
    self._reparent(parentParent, parentNode)
    self._reparent(middleParent, middleNode)

  def _fixRed(self, node: RBNode) -> Optional[RBNode]:
    """Fix possible red-violation at node.

    Assume no black-violation.
    Assume no red-violation above the node.
    """
    if getColor(node) != RBColor.RED:
      return None
    parentNode = node.parent.node
    if getColor(parentNode) != RBColor.RED:
      return None
    gpNode = parentNode.parent.node
    siblingNode = gpNode.getChild(RBSide.flip(parentNode.side))
    if getColor(siblingNode) == RBColor.RED:
      setColor(parentNode, RBColor.BLACK)
      setColor(siblingNode, RBColor.BLACK)
      setColor(gpNode, RBColor.RED)
      return gpNode
    if node.side != parentNode.side:
      self._rotate(node)
      self._rotate(node)
    else:
      self._rotate(parentNode)
    return None

  def insert(self, k: KT, v: VT) -> None:
    if self.root is None:
      self.root = RBNode(k, v)
      return

    parent = self.root
    side = None
    while True:
      side = RBSide.LEFT if k < parent.key else RBSide.RIGHT
      child = parent.getChild(side)
      if child is None:
        break
      parent = child

    node = RBNode(k, v)
    self._reparent(RBParent(parent, side, RBColor.RED), node)
    while node is not None:
      node = self._fixRed(node)

  def _swapParents(self, n1: RBNode, n2: RBNode) -> None:
    n1Parent = n1.parent
    n2Parent = n2.parent
    self._reparent(n2Parent, n1)
    self._reparent(n1Parent, n2)

  def _swapChildren(self, n1: RBNode, n2: RBNode, side: RBSide) -> None:
    n1Child = n1.getChild(side)
    n2Child = n2.getChild(side)
    n1Parent = RBParent(n2, side, getColor(n1Child))
    n2Parent = RBParent(n1, side, getColor(n2Child))
    self._reparent(n1Parent, n1Child)
    self._reparent(n2Parent, n2Child)

  def _swapNodes(self, n1: RBNode, n2: RBNode) -> None:
    childNode = n1.isAdjacent(n2)
    if childNode:
      side = childNode.side
      parentNode = childNode.parent.node
      gcNode = childNode.getChild(side)
      childParent = RBParent(childNode, side, getColor(childNode))
      parentParent = parentNode.parent
      gcParent = RBParent(parentNode, side, getColor(gcNode))
      self._reparent(childParent, parentNode)
      self._reparent(parentParent, childNode)
      self._reparent(gcParent, gcNode)
      self._swapChildren(childNode, parentNode, RBSide.flip(side))
    else:
      self._swapParents(n1, n2)
      self._swapChildren(n1, n2, RBSide.LEFT)
      self._swapChildren(n1, n2, RBSide.RIGHT)

  def _fixBlack(self, parent: Optional[RBParent]) -> Optional[RBParent]:
    if parent is None:
      return None
    parentNode = parent.node
    siblingNode = parentNode.getChild(RBSide.flip(parent.side))
    if getColor(siblingNode) == RBColor.RED:
      self._rotate(siblingNode)
    siblingNode = parentNode.getChild(RBSide.flip(parent.side))
    aNode = siblingNode.getChild(parent.side)
    bNode = siblingNode.getChild(RBSide.flip(parent.side))
    if getColor(bNode) == RBColor.RED:
      self._rotate(siblingNode)
      setColor(bNode, RBColor.BLACK)
      return None
    if getColor(aNode) == RBColor.RED:
      self._rotate(aNode)
      self._rotate(aNode)
      setColor(siblingNode, RBColor.BLACK)
      return None
    if getColor(parentNode) == RBColor.RED:
      setColor(parentNode, RBColor.BLACK)
      setColor(siblingNode, RBColor.RED)
      return None
    setColor(siblingNode, RBColor.RED)
    return parentNode.parent

  def removeNode(self, node: RBNode) -> None:
    if node.left and node.right:
      succNode = node.successor()
      self._swapNodes(node, succNode)
    parent = node.parent
    childNode = node.left or node.right
    self._reparent(parent, childNode)
    node.clear()
    if childNode is not None:
      return
    if parent is not None and parent.color == RBColor.RED:
      return
    while parent is not None:
      parent = self._fixBlack(parent)

  def searchRange(self, k1: KT, k2: KT) -> List[RBNode]:
    nodes = []
    currNode = self.root
    stack = []
    while currNode or stack:
      while currNode:
        stack.append(currNode)
        currNode = None if currNode.key < k1 else currNode.left
      currNode = stack.pop()
      if (not currNode.key < k1) and (not k2 < currNode.key):
        nodes.append(currNode)
      currNode = None if k2 < currNode.key else currNode.right
    return nodes

  def removeRange(self, k1: KT, k2: KT) -> List[RBNode]:
    nodes = self.searchRange(k1, k2)
    for node in nodes:
      self.removeNode(node)
    return nodes

if __name__ == '__main__':
  import random
  t = RBTree()
  xs = list(range(10000))
  random.shuffle(xs)
  for x in xs:
    t.insert(x, None)
  random.shuffle(xs)
  for x in xs:
    nodes = t.searchRange(x, x)
    t.removeNode(nodes[0])
  print(t.root)
