from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


# ==========================================
# 1. Baseline: Basic BST Operations
# ==========================================
@dataclass
class BSTNode:
    key: int
    left: Optional[BSTNode] = None
    right: Optional[BSTNode] = None


class BinarySearchTree:
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

    def inorder(self) -> list[int]:
        result: list[int] = []

        def _traverse(node: Optional[BSTNode]) -> None:
            if node is None:
                return
            _traverse(node.left)
            result.append(node.key)
            _traverse(node.right)

        _traverse(self.root)
        return result


# ==========================================
# 2. B-Tree Implementation (Minimum Degree t)
# ==========================================
# Invariant for minimum degree t >= 2:
# - Non-root nodes hold between (t - 1) and (2t - 1) keys.
# - Internal nodes have len(keys) + 1 child pointers.
# - All leaf nodes sit at the same depth.
@dataclass
class BTreeNode:
    leaf: bool = True
    keys: list[int] = field(default_factory=list)
    children: list[BTreeNode] = field(default_factory=list)


class BTree:
    def __init__(self, t: int = 2) -> None:
        if t < 2:
            raise ValueError("Minimum degree t must be at least 2")
        self.t = t
        self.root = BTreeNode(leaf=True)

    def search(self, key: int, node: Optional[BTreeNode] = None) -> bool:
        if node is None:
            node = self.root

        idx = 0
        while idx < len(node.keys) and key > node.keys[idx]:
            idx += 1

        if idx < len(node.keys) and key == node.keys[idx]:
            return True
        if node.leaf:
            return False
        return self.search(key, node.children[idx])

    def insert(self, key: int) -> None:
        if self.search(key):
            return  # Keep keys unique for clean classroom comparison

        root = self.root
        max_keys = 2 * self.t - 1

        # Root is full: allocate a new root and split old root
        if len(root.keys) == max_keys:
            new_root = BTreeNode(leaf=False, children=[root])
            self.root = new_root
            self._split_child(new_root, 0)
            self._insert_non_full(new_root, key)
        else:
            self._insert_non_full(root, key)

    def _split_child(self, parent: BTreeNode, child_idx: int) -> None:
        t = self.t
        full_child = parent.children[child_idx]
        new_child = BTreeNode(leaf=full_child.leaf)

        median_key = full_child.keys[t - 1]

        # Right half moves to new_child; left half stays in full_child
        new_child.keys = full_child.keys[t:]
        full_child.keys = full_child.keys[: t - 1]

        if not full_child.leaf:
            new_child.children = full_child.children[t:]
            full_child.children = full_child.children[:t]

        parent.children.insert(child_idx + 1, new_child)
        parent.keys.insert(child_idx, median_key)

    def _insert_non_full(self, node: BTreeNode, key: int) -> None:
        idx = len(node.keys) - 1

        if node.leaf:
            node.keys.append(0)  # Placeholder slot
            while idx >= 0 and key < node.keys[idx]:
                node.keys[idx + 1] = node.keys[idx]
                idx -= 1
            node.keys[idx + 1] = key
            return

        while idx >= 0 and key < node.keys[idx]:
            idx -= 1
        idx += 1

        # Proactive split on descent ensures no bottom-up backtracking
        if len(node.children[idx].keys) == 2 * self.t - 1:
            self._split_child(node, idx)
            if key > node.keys[idx]:
                idx += 1

        self._insert_non_full(node.children[idx], key)

    def inorder(self, node: Optional[BTreeNode] = None) -> list[int]:
        if node is None:
            node = self.root
        if node.leaf:
            return list(node.keys)

        result: list[int] = []
        for i, key in enumerate(node.keys):
            result.extend(self.inorder(node.children[i]))
            result.append(key)
        result.extend(self.inorder(node.children[len(node.keys)]))
        return result

    def display_levels(self) -> list[list[list[int]]]:
        """Returns levels as lists of node key-lists to inspect height & balance."""
        levels: list[list[list[int]]] = []
        current_level = [self.root]

        while current_level:
            levels.append([n.keys for n in current_level])
            next_level: list[BTreeNode] = []
            for n in current_level:
                if not n.leaf:
                    next_level.extend(n.children)
            current_level = next_level

        return levels


# ==========================================
# 3. Classroom Walkthrough Demo
# ==========================================
if __name__ == "__main__":
    sample_keys = [10, 20, 5, 6, 12, 30, 7, 17]

    bst = BinarySearchTree()
    btree = BTree(t=2)  # Max 3 keys per node, min 1 key per non-root node

    for k in sample_keys:
        bst.insert(k)
        btree.insert(k)

    print("BST inorder:   ", bst.inorder())
    print("BTree inorder: ", btree.inorder())
    print("BTree levels:  ", btree.display_levels())
    print("Search 12 in BTree:", btree.search(12))
    print("Search 99 in BTree:", btree.search(99))