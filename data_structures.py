"""
data_structures.py
------------------
Clean, simple implementations of fundamental data structures:
- Singly Linked List (SLL)
- Doubly Linked List (DLL)

Both structures maintain head and tail pointers for O(1) operations at ends.
"""

class SLLNode:
    """Node for a Singly Linked List."""
    __slots__ = ('val', 'next')
    
    def __init__(self, val):
        self.val = val
        self.next = None


class SinglyLinkedList:
    """Singly Linked List with head, tail, and size tracking."""
    
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def insert_first(self, val):
        """Insert a value at the beginning: O(1)."""
        node = SLLNode(val)
        node.next = self.head
        self.head = node
        if self.tail is None:
            self.tail = node
        self.size += 1

    def insert_last(self, val):
        """Insert a value at the end: O(1) using tail pointer."""
        node = SLLNode(val)
        if self.head is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.size += 1

    def insert_at(self, pos, val):
        """Insert a value at 0-based index pos: O(k) traversal."""
        if pos <= 0:
            self.insert_first(val)
            return
        if pos >= self.size:
            self.insert_last(val)
            return
        
        curr = self.head
        for _ in range(pos - 1):
            curr = curr.next
        
        node = SLLNode(val)
        node.next = curr.next
        curr.next = node
        self.size += 1

    def delete_first(self):
        """Remove and return the first element: O(1)."""
        if self.head is None:
            return None
        val = self.head.val
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self.size -= 1
        return val

    def delete_last(self):
        """Remove and return the last element: O(n) in SLL."""
        if self.head is None:
            return None
        if self.head == self.tail:
            val = self.head.val
            self.head = self.tail = None
            self.size = 0
            return val
        
        curr = self.head
        while curr.next != self.tail:
            curr = curr.next
        val = self.tail.val
        curr.next = None
        self.tail = curr
        self.size -= 1
        return val

    def search(self, target):
        """
        Linear search: O(n).
        Returns (found: bool, index: int, comparisons: int).
        """
        curr = self.head
        idx = 0
        comparisons = 0
        while curr:
            comparisons += 1
            if curr.val == target:
                return True, idx, comparisons
            curr = curr.next
            idx += 1
        return False, -1, comparisons

    def __len__(self):
        return self.size

    def __iter__(self):
        curr = self.head
        while curr:
            yield curr.val
            curr = curr.next


class DLLNode:
    """Node for a Doubly Linked List."""
    __slots__ = ('val', 'prev', 'next')
    
    def __init__(self, val):
        self.val = val
        self.prev = None
        self.next = None


class DoublyLinkedList:
    """Doubly Linked List with head, tail, and size tracking."""
    
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def insert_first(self, val):
        """Insert at beginning: O(1)."""
        node = DLLNode(val)
        if self.head is None:
            self.head = self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node
        self.size += 1

    def insert_last(self, val):
        """Insert at end: O(1)."""
        node = DLLNode(val)
        if self.head is None:
            self.head = self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        self.size += 1

    def insert_at(self, pos, val):
        """Insert at 0-based index pos: O(k) traversal."""
        if pos <= 0:
            self.insert_first(val)
            return
        if pos >= self.size:
            self.insert_last(val)
            return
        
        curr = self.head
        for _ in range(pos):
            curr = curr.next
        
        node = DLLNode(val)
        node.prev = curr.prev
        node.next = curr
        curr.prev.next = node
        curr.prev = node
        self.size += 1

    def search(self, target):
        """
        Linear search: O(n).
        Returns (found: bool, index: int, comparisons: int).
        """
        curr = self.head
        idx = 0
        comparisons = 0
        while curr:
            comparisons += 1
            if curr.val == target:
                return True, idx, comparisons
            curr = curr.next
            idx += 1
        return False, -1, comparisons

    def __len__(self):
        return self.size

    def __iter__(self):
        curr = self.head
        while curr:
            yield curr.val
            curr = curr.next
