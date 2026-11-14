from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class BSTNode:
    key: int
    left: Optional[BSTNode] = None
    right: Optional[BSTNode] = None


class BinarySearchTree:
    """Maintains left.key < node.key < right.key for every node."""

    def __init__(self) -> None:
        self.root: Optional[BSTNode] = None

    def insert(self, key: int) -> None:
        def _insert(node: Optional[BSTNode], val: int) -> BSTNode:
            if node is None:
                return BSTNode(val)
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

    def find_min(self) -> Optional[int]:
        if self.root is None:
            return None
        curr = self.root
        while curr.left is not None:
            curr = curr.left
        return curr.key

    def find_max(self) -> Optional[int]:
        if self.root is None:
            return None
        curr = self.root
        while curr.right is not None:
            curr = curr.right
        return curr.key

    def inorder(self) -> list[int]:
        result: list[int] = []

        def _dfs(node: Optional[BSTNode]) -> None:
            if node is None:
                return
            _dfs(node.left)
            result.append(node.key)
            _dfs(node.right)

        _dfs(self.root)
        return result

    def delete(self, key: int) -> None:
        def _min_node(node: BSTNode) -> BSTNode:
            while node.left is not None:
                node = node.left
            return node

        def _delete(node: Optional[BSTNode], val: int) -> Optional[BSTNode]:
            if node is None:
                return None
            if val < node.key:
                node.left = _delete(node.left, val)
            elif val > node.key:
                node.right = _delete(node.right, val)
            else:
                if node.left is None:
                    return node.right
                if node.right is None:
                    return node.left
                successor = _min_node(node.right)
                node.key = successor.key
                node.right = _delete(node.right, successor.key)
            return node

        self.root = _delete(self.root, key)


if __name__ == "__main__":
    tree = BinarySearchTree()
    for val in [25, 15, 50, 10, 22, 35, 70]:
        tree.insert(val)

    print("Inorder:", tree.inorder())
    print("Min / Max:", tree.find_min(), tree.find_max())
    print("Search 22:", tree.search(22))
    print("Search 99:", tree.search(99))

    tree.delete(15)
    print("After delete(15):", tree.inorder())