"""
insertion_comparison.py
-----------------------
Compares insertion performance across data structures:
1. At the beginning of a sequence (pos = 0)
2. At the end of a sequence (pos = N)
3. At a specified position k (pos = k, e.g. middle)

Data Structures compared:
- Dynamic Array (Python list)
- Singly Linked List (SLL)
- Doubly Linked List (DLL)
"""

import time
import copy
from data_structures import SinglyLinkedList, DoublyLinkedList


def benchmark_insertion(n=100000):
    print("=" * 82)
    print(f"INSERTION BENCHMARK & COMPARISON (Sequence Size: {n:,})")
    print("=" * 82)

    k_pos = n // 2
    test_val = 999999

    # Setup baseline data
    raw_data = list(range(1, n + 1))

    # Build initial structures
    print("Initializing test structures...")
    arr = list(raw_data)

    sll = SinglyLinkedList()
    for x in raw_data:
        sll.insert_last(x)

    dll = DoublyLinkedList()
    for x in raw_data:
        dll.insert_last(x)

    results = []

    # =============================================================
    # 1. INSERTION AT THE BEGINNING (index 0)
    # =============================================================
    # Dynamic Array: requires shifting all N elements right by 1
    t0 = time.perf_counter()
    arr.insert(0, test_val)
    arr_beg_time = (time.perf_counter() - t0) * 1e6
    results.append({
        "Position": "Beginning (pos = 0)",
        "Structure": "Array (list)",
        "Time (µs)": f"{arr_beg_time:,.2f}",
        "Big-O": "O(n)",
        "Mechanism": "Shifts all N elements right in memory"
    })

    # Singly Linked List: O(1) pointer rewire
    t0 = time.perf_counter()
    sll.insert_first(test_val)
    sll_beg_time = (time.perf_counter() - t0) * 1e6
    results.append({
        "Position": "Beginning (pos = 0)",
        "Structure": "Singly Linked List",
        "Time (µs)": f"{sll_beg_time:,.2f}",
        "Big-O": "O(1)",
        "Mechanism": "new_node.next = head; head = new_node"
    })

    # Doubly Linked List: O(1) pointer rewire
    t0 = time.perf_counter()
    dll.insert_first(test_val)
    dll_beg_time = (time.perf_counter() - t0) * 1e6
    results.append({
        "Position": "Beginning (pos = 0)",
        "Structure": "Doubly Linked List",
        "Time (µs)": f"{dll_beg_time:,.2f}",
        "Big-O": "O(1)",
        "Mechanism": "Rewires head and prev/next pointers"
    })

    # =============================================================
    # 2. INSERTION AT SPECIFIED POSITION k (middle: k = n // 2)
    # =============================================================
    # Dynamic Array: shifts elements from k to end right by 1
    t0 = time.perf_counter()
    arr.insert(k_pos, test_val)
    arr_mid_time = (time.perf_counter() - t0) * 1e6
    results.append({
        "Position": f"Specified k (pos = {k_pos:,})",
        "Structure": "Array (list)",
        "Time (µs)": f"{arr_mid_time:,.2f}",
        "Big-O": "O(n - k)",
        "Mechanism": "Shifts (n - k) elements in memory"
    })

    # Singly Linked List: traverses k nodes from head
    t0 = time.perf_counter()
    sll.insert_at(k_pos, test_val)
    sll_mid_time = (time.perf_counter() - t0) * 1e6
    results.append({
        "Position": f"Specified k (pos = {k_pos:,})",
        "Structure": "Singly Linked List",
        "Time (µs)": f"{sll_mid_time:,.2f}",
        "Big-O": "O(k)",
        "Mechanism": "Traverses k nodes from head, then splices"
    })

    # Doubly Linked List: traverses to node k
    t0 = time.perf_counter()
    dll.insert_at(k_pos, test_val)
    dll_mid_time = (time.perf_counter() - t0) * 1e6
    results.append({
        "Position": f"Specified k (pos = {k_pos:,})",
        "Structure": "Doubly Linked List",
        "Time (µs)": f"{dll_mid_time:,.2f}",
        "Big-O": "O(k)",
        "Mechanism": "Traverses to node k, then splices pointers"
    })

    # =============================================================
    # 3. INSERTION AT THE END (pos = N)
    # =============================================================
    # Dynamic Array: append to tail buffer
    t0 = time.perf_counter()
    arr.append(test_val)
    arr_end_time = (time.perf_counter() - t0) * 1e6
    results.append({
        "Position": "End (pos = N)",
        "Structure": "Array (list)",
        "Time (µs)": f"{arr_end_time:,.2f}",
        "Big-O": "O(1) amortized",
        "Mechanism": "Writes to allocated buffer capacity"
    })

    # Singly Linked List: O(1) via tail pointer
    t0 = time.perf_counter()
    sll.insert_last(test_val)
    sll_end_time = (time.perf_counter() - t0) * 1e6
    results.append({
        "Position": "End (pos = N)",
        "Structure": "Singly Linked List",
        "Time (µs)": f"{sll_end_time:,.2f}",
        "Big-O": "O(1)",
        "Mechanism": "tail.next = new_node; tail = new_node"
    })

    # Doubly Linked List: O(1) via tail pointer
    t0 = time.perf_counter()
    dll.insert_last(test_val)
    dll_end_time = (time.perf_counter() - t0) * 1e6
    results.append({
        "Position": "End (pos = N)",
        "Structure": "Doubly Linked List",
        "Time (µs)": f"{dll_end_time:,.2f}",
        "Big-O": "O(1)",
        "Mechanism": "tail.next = new_node; node.prev = tail"
    })

    # =============================================================
    # DISPLAY TABLE
    # =============================================================
    print()
    header = f"{'Insertion Position':<26} | {'Structure':<20} | {'Time (µs)':<11} | {'Big-O':<16} | {'Mechanism'}"
    print(header)
    print("-" * len(header))
    for r in results:
        print(f"{r['Position']:<26} | {r['Structure']:<20} | {r['Time (µs)']:<11} | {r['Big-O']:<16} | {r['Mechanism']}")

    print("\n" + "=" * 82)
    print("KEY INSIGHTS:")
    print("1. Insertion at Beginning:")
    print("   Linked Lists excel here (O(1)), updating only the head pointer.")
    print("   Arrays take O(n) because all n elements must be shifted in memory.")
    print("\n2. Insertion at End:")
    print("   Both Array append (O(1) amortized) and Linked List with tail pointer (O(1))")
    print("   are extremely fast.")
    print("\n3. Insertion at Specified Position k:")
    print("   - Array takes O(n - k) memory shifts (implemented efficiently in C).")
    print("   - Linked List takes O(k) traversal steps to reach the kth node before")
    print("     splicing in O(1). If a pointer to node k is already known, insertion")
    print("     is O(1); otherwise traversal dominates the runtime.")
    print("=" * 82)


if __name__ == "__main__":
    benchmark_insertion(100000)
