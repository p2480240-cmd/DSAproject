import time
import random
import os

# ==========================================
# 1. DATASET GENERATION (TEXT FILES)
# ==========================================
def generate_datasets(n=100000):
    files = {
        "dataset_sorted.txt": "Sorted",
        "dataset_unsorted_duplicates.txt": "Unsorted with Duplicates",
        "dataset_unsorted_unique.txt": "Unsorted Unique"
    }
    
    print(f"Generating 3 datasets ({n:,} numbers each)...")
    for filename, desc in files.items():
        t0 = time.time()
        with open(filename, 'w') as f:
            if filename == "dataset_sorted.txt":
                for i in range(1, n + 1):
                    f.write(f"{i}\n")
            elif filename == "dataset_unsorted_duplicates.txt":
                for _ in range(n):
                    f.write(f"{random.randint(1, n // 10)}\n")
            elif filename == "dataset_unsorted_unique.txt":
                # Hull-Dobell LCG full-cycle permutation (least space O(1))
                m = 1
                while m < n:
                    m <<= 1
                a, c, x = 1664525 * 4 + 1, 1013904223, 42
                count = 0
                while count < n:
                    x = (a * x + c) & (m - 1)
                    if x < n:
                        f.write(f"{x + 1}\n")
                        count += 1
                        
        elapsed = time.time() - t0
        size_mb = os.path.getsize(filename) / (1024 * 1024)
        print(f"[{desc}] Saved to '{filename}' | Time taken: {elapsed:.4f}s | Size: {size_mb:.2f} MB")
    print()


# ==========================================
# 2. STACK IMPLEMENTATION
# ==========================================
class Stack:
    def __init__(self):
        self.items = []

    def insert_first(self, val):
        self.items.insert(0, val)

    def insert_at(self, pos, val):
        if 0 <= pos <= len(self.items):
            self.items.insert(pos, val)

    def insert_last(self, val):
        self.items.append(val)

    def delete_first(self):
        return self.items.pop(0) if self.items else None

    def delete_at(self, pos):
        if 0 <= pos < len(self.items):
            return self.items.pop(pos)
        return None

    def delete_last(self):
        return self.items.pop() if self.items else None

    def search(self, val):
        for i, item in enumerate(self.items):
            if item == val:
                return True, i
        return False, -1

    def __len__(self):
        return len(self.items)


# ==========================================
# 3. SINGLY LINKED LIST (SLL)
# ==========================================
class SLLNode:
    __slots__ = ('val', 'next')
    def __init__(self, val):
        self.val = val
        self.next = None

class SLL:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def insert_first(self, val):
        node = SLLNode(val)
        node.next = self.head
        self.head = node
        if self.tail is None:
            self.tail = node
        self.size += 1

    def insert_at(self, pos, val):
        if pos < 0 or pos > self.size:
            return
        if pos == 0:
            self.insert_first(val)
            return
        if pos == self.size:
            self.insert_last(val)
            return
        curr = self.head
        for _ in range(pos - 1):
            curr = curr.next
        node = SLLNode(val)
        node.next = curr.next
        curr.next = node
        self.size += 1

    def insert_last(self, val):
        node = SLLNode(val)
        if self.head is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.size += 1

    def delete_first(self):
        if self.head is None:
            return None
        val = self.head.val
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self.size -= 1
        return val

    def delete_at(self, pos):
        if pos < 0 or pos >= self.size:
            return None
        if pos == 0:
            return self.delete_first()
        if pos == self.size - 1:
            return self.delete_last()
        curr = self.head
        for _ in range(pos - 1):
            curr = curr.next
        val = curr.next.val
        curr.next = curr.next.next
        self.size -= 1
        return val

    def delete_last(self):
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

    def search(self, val):
        curr = self.head
        idx = 0
        while curr:
            if curr.val == val:
                return True, idx
            curr = curr.next
            idx += 1
        return False, -1

    def __len__(self):
        return self.size


# ==========================================
# 4. DOUBLY LINKED LIST (DLL)
# ==========================================
class DLLNode:
    __slots__ = ('val', 'prev', 'next')
    def __init__(self, val):
        self.val = val
        self.prev = None
        self.next = None

class DLL:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def insert_first(self, val):
        node = DLLNode(val)
        if self.head is None:
            self.head = self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node
        self.size += 1

    def insert_at(self, pos, val):
        if pos < 0 or pos > self.size:
            return
        if pos == 0:
            self.insert_first(val)
            return
        if pos == self.size:
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

    def insert_last(self, val):
        node = DLLNode(val)
        if self.head is None:
            self.head = self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        self.size += 1

    def delete_first(self):
        if self.head is None:
            return None
        val = self.head.val
        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None
        self.size -= 1
        return val

    def delete_at(self, pos):
        if pos < 0 or pos >= self.size:
            return None
        if pos == 0:
            return self.delete_first()
        if pos == self.size - 1:
            return self.delete_last()
        curr = self.head
        for _ in range(pos):
            curr = curr.next
        val = curr.val
        curr.prev.next = curr.next
        curr.next.prev = curr.prev
        self.size -= 1
        return val

    def delete_last(self):
        if self.tail is None:
            return None
        val = self.tail.val
        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None
        self.size -= 1
        return val

    def search(self, val):
        curr = self.head
        idx = 0
        while curr:
            if curr.val == val:
                return True, idx
            curr = curr.next
            idx += 1
        return False, -1

    def __len__(self):
        return self.size


# ==========================================
# 5. EXECUTION & SEARCH FROM TEXT FILES
# ==========================================
def test_structure(ds_class, ds_name, filename, search_target):
    print(f"--- Testing {ds_name} on '{filename}' ---")
    ds = ds_class()

    # 1. Load numbers directly from text file
    t0 = time.time()
    with open(filename, 'r') as f:
        for line in f:
            ds.insert_last(int(line.strip()))
    load_time = time.time() - t0
    print(f"Loaded {len(ds):,} items in {load_time:.4f}s")

    # 2. Search
    t0 = time.time()
    found, pos = ds.search(search_target)
    print(f"Search for {search_target}: Found={found} at index {pos} | Time: {(time.time() - t0) * 1e6:.2f} µs")

    # 3. Insertions: First, Middle, Last
    t0 = time.time()
    ds.insert_first(999999)
    print(f"Insert First (999999): Success | Time: {(time.time() - t0) * 1e6:.2f} µs")

    t0 = time.time()
    ds.insert_at(len(ds) // 2, 888888)
    print(f"Insert at Middle (888888): Success | Time: {(time.time() - t0) * 1e6:.2f} µs")

    t0 = time.time()
    ds.insert_last(777777)
    print(f"Insert Last (777777): Success | Time: {(time.time() - t0) * 1e6:.2f} µs")

    # 4. Deletions: First, Middle, Last
    t0 = time.time()
    v1 = ds.delete_first()
    print(f"Delete First: Output={v1} | Time: {(time.time() - t0) * 1e6:.2f} µs")

    t0 = time.time()
    v2 = ds.delete_at(len(ds) // 2)
    print(f"Delete at Middle: Output={v2} | Time: {(time.time() - t0) * 1e6:.2f} µs")

    t0 = time.time()
    v3 = ds.delete_last()
    print(f"Delete Last: Output={v3} | Time: {(time.time() - t0) * 1e6:.2f} µs\n")


if __name__ == "__main__":
    generate_datasets(100000)

    datasets = [
        ("dataset_sorted.txt", 50000),
        ("dataset_unsorted_duplicates.txt", 500),
        ("dataset_unsorted_unique.txt", 259)
    ]

    for filename, target in datasets:
        print("=" * 60)
        print(f"FILE: {filename}")
        print("=" * 60)
        test_structure(Stack, "Stack", filename, target)
        test_structure(SLL, "Singly Linked List (SLL)", filename, target)
        test_structure(DLL, "Doubly Linked List (DLL)", filename, target)
