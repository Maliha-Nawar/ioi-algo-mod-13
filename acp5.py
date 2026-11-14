from __future__ import annotations
from collections import deque
from dataclasses import dataclass
from typing import Optional


@dataclass
class Node:
    key: int
    left: Optional[Node] = None
    right: Optional[Node] = None


class BinarySearchTree:
    """Binary Search Tree maintaining the invariant: left.key < node.key < right.key."""

    def __init__(self) -> None:
        self.root: Optional[Node] = None

    # --- Core Operations (Review / Reinforcement) ---

    def insert(self, key: int) -> None:
        def _insert(node: Optional[Node], val: int) -> Node:
            if node is None:
                return Node(val)
            if val < node.key:
                node.left = _insert(node.left, val)
            elif val > node.key:
                node.right = _insert(node.right, val)
            # Duplicate keys ignored to keep BST property unambiguous
            return node

        self.root = _insert(self.root, key)

    def search(self, key: int) -> bool:
        curr = self.root
        while curr is not None:
            if key == curr.key:
                return True
            curr = curr.left if key < curr.key else curr.right
        return False

    def inorder(self) -> list[int]:
        """Visits left -> root -> right; yields keys in sorted order."""
        result: list[int] = []

        def _dfs(node: Optional[Node]) -> None:
            if node is None:
                return
            _dfs(node.left)
            result.append(node.key)
            _dfs(node.right)

        _dfs(self.root)
        return result

    # --- Next-Step Operations & Structural Checks ---

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

    def height(self) -> int:
        """Returns number of edges on longest root-to-leaf path (-1 for empty tree)."""
        def _height(node: Optional[Node]) -> int:
            if node is None:
                return -1
            return 1 + max(_height(node.left), _height(node.right))

        return _height(self.root)

    def level_order(self) -> list[list[int]]:
        """Returns keys grouped by depth to inspect tree shape."""
        if self.root is None:
            return []

        levels: list[list[int]] = []
        queue: deque[Node] = deque([self.root])

        while queue:
            level_size = len(queue)
            current_level: list[int] = []
            for _ in range(level_size):
                node = queue.popleft()
                current_level.append(node.key)
                if node.left is not None:
                    queue.append(node.left)
                if node.right is not None:
                    queue.append(node.right)
            levels.append(current_level)

        return levels

    def delete(self, key: int) -> None:
        """Handles leaf (0 children), single-child (1 child), and 2-child cases."""
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
                # Case 1 & Case 2: 0 or 1 child
                if node.left is None:
                    return node.right
                if node.right is None:
                    return node.left

                # Case 3: 2 children -> replace with inorder successor (min of right subtree)
                successor = _min_node(node.right)
                node.key = successor.key
                node.right = _delete(node.right, successor.key)

            return node

        self.root = _delete(self.root, key)


# ==========================================
# Classroom Walkthrough
# ==========================================
if __name__ == "__main__":
    bst = BinarySearchTree()
    keys = [50, 30, 70, 20, 40, 60, 80]

    for k in keys:
        bst.insert(k)

    print("Initial levels:  ", bst.level_order())
    print("Inorder (sorted):", bst.inorder())
    print("Min / Max:       ", bst.find_min(), "/", bst.find_max())
    print("Height:          ", bst.height())
    print("Search 60 / 25:  ", bst.search(60), "/", bst.search(25))

    # Trace deletion cases:
    bst.delete(20)  # Leaf node
    print("After delete(20):", bst.level_order(), "-> inorder:", bst.inorder())

    bst.delete(30)  # Single-child node (only right child 40)
    print("After delete(30):", bst.level_order(), "-> inorder:", bst.inorder())

    bst.delete(50)  # Root with two children (replaced by successor 60)
    print("After delete(50):", bst.level_order(), "-> inorder:", bst.inorder())