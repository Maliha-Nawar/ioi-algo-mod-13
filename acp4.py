from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class Node:
    key: int
    left: Optional[Node] = None
    right: Optional[Node] = None


class BinarySearchTree:
    """BST maintaining left.key < node.key < right.key for every node."""

    def __init__(self) -> None:
        self.root: Optional[Node] = None

    def insert(self, key: int) -> None:
        def _insert(node: Optional[Node], val: int) -> Node:
            if node is None:
                return Node(val)
            if val < node.key:
                node.left = _insert(node.left, val)
            elif val > node.key:
                node.right = _insert(node.right, val)
            return node

        self.root = _insert(self.root, key)

    def search(self, key: int) -> bool:
        curr = self.root
        while curr is not None:
            if key == curr.key:
                return True
            curr = curr.left if key < curr.key else curr.right
        return False

    def find_min(self, node: Optional[Node] = None) -> Optional[int]:
        curr = node if node is not None else self.root
        if curr is None:
            return None
        while curr.left is not None:
            curr = curr.left
        return curr.key

    def find_max(self, node: Optional[Node] = None) -> Optional[int]:
        curr = node if node is not None else self.root
        if curr is None:
            return None
        while curr.right is not None:
            curr = curr.right
        return curr.key

    def inorder(self) -> list[int]:
        result: list[int] = []

        def _traverse(node: Optional[Node]) -> None:
            if node is None:
                return
            _traverse(node.left)
            result.append(node.key)
            _traverse(node.right)

        _traverse(self.root)
        return result

    def delete(self, key: int) -> None:
        def _min_node(node: Node) -> Node:
            while node.left is not None:
                node = node.left
            return node

        def _delete(node: Optional[Node], val: int) -> Optional[Node]:
            if node is None:
                return None
            if val < node.key:
                node.left = _delete(node.left, val)
            elif val > node.key:
                node.right = _delete(node.right, val)
            else:
                # 0 or 1 child
                if node.left is None:
                    return node.right
                if node.right is None:
                    return node.left
                # 2 children: swap with inorder successor
                successor = _min_node(node.right)
                node.key = successor.key
                node.right = _delete(node.right, successor.key)
            return node

        self.root = _delete(self.root, key)


if __name__ == "__main__":
    bst = BinarySearchTree()
    for value in [40, 20, 60, 10, 30, 50, 70]:
        bst.insert(value)

    print("Inorder:", bst.inorder())
    print("Min / Max:", bst.find_min(), bst.find_max())
    print("Search 30:", bst.search(30))
    print("Search 25:", bst.search(25))

    bst.delete(20)
    print("After deleting 20:", bst.inorder())