"""
search_comparison.py
--------------------
Compares search algorithms and data structures across different scenarios:
1. Binary search on sorted data (Array).
2. Linear search on sorted data (Array).
3. Linear search on unsorted data with repetition (duplicates).
4. Linear search on unsorted data without repetition (unique).
5. Array vs Linked-List search (cache locality and pointer traversal comparison).
"""

import time
from data_structures import SinglyLinkedList


# ==========================================
# SEARCH ALGORITHMS
# ==========================================

def linear_search_array(arr, target):
    """
    Linear search on an array.
    Time Complexity: O(n)
    Returns: (found: bool, index: int, comparisons: int)
    """
    comparisons = 0
    for idx, val in enumerate(arr):
        comparisons += 1
        if val == target:
            return True, idx, comparisons
    return False, -1, comparisons


def binary_search_array(arr, target):
    """
    Binary search on a sorted array.
    Time Complexity: O(log n)
    Returns: (found: bool, index: int, comparisons: int)
    """
    low = 0
    high = len(arr) - 1
    comparisons = 0
    while low <= high:
        comparisons += 1
        mid = (low + high) // 2
        mid_val = arr[mid]
        if mid_val == target:
            return True, mid, comparisons
        elif mid_val < target:
            low = mid + 1
        else:
            high = mid - 1
    return False, -1, comparisons


# ==========================================
# BENCHMARK SUITE
# ==========================================

def load_data_from_file(filename, limit=100000):
    """Reads up to `limit` numbers from a dataset file."""
    data = []
    with open(filename, 'r') as f:
        for line in f:
            data.append(int(line.strip()))
            if len(data) >= limit:
                break
    return data


def run_search_comparison(sample_size=100000):
    print("=" * 78)
    print(f"SEARCH BENCHMARK & COMPARISON (Sample size: {sample_size:,})")
    print("=" * 78)

    # 1. Load Datasets
    print("Loading test datasets...")
    sorted_arr = load_data_from_file("dataset_sorted.txt", sample_size)
    unsorted_dup_arr = load_data_from_file("dataset_unsorted_duplicates.txt", sample_size)
    unsorted_uniq_arr = load_data_from_file("dataset_unsorted_unique.txt", sample_size)

    # Build Linked List for Array vs Linked List comparison
    print("Building Singly Linked List from unique dataset...")
    sll = SinglyLinkedList()
    for num in unsorted_uniq_arr:
        sll.insert_last(num)
    print("Data loaded successfully.\n")

    # Select representative search targets:
    # Target near the 75% mark for realistic search
    target_sorted = sorted_arr[int(sample_size * 0.75)]
    target_dup = unsorted_dup_arr[int(sample_size * 0.75)]
    target_uniq = unsorted_uniq_arr[int(sample_size * 0.75)]

    results = []

    # -------------------------------------------------------------
    # 1. Binary Search on Sorted Data (Array)
    # -------------------------------------------------------------
    t0 = time.perf_counter()
    found, idx, comps = binary_search_array(sorted_arr, target_sorted)
    elapsed_us = (time.perf_counter() - t0) * 1e6
    results.append({
        "Scenario": "1. Sorted Data (Target ~75%)",
        "Algorithm": "Binary Search",
        "Structure": "Array",
        "Found": found,
        "Comparisons": comps,
        "Time (µs)": f"{elapsed_us:,.2f}",
        "Big-O": "O(log n)"
    })

    # Linear Search on Sorted Data (for direct comparison)
    t0 = time.perf_counter()
    found, idx, comps = linear_search_array(sorted_arr, target_sorted)
    elapsed_us = (time.perf_counter() - t0) * 1e6
    results.append({
        "Scenario": "1. Sorted Data (Target ~75%)",
        "Algorithm": "Linear Search",
        "Structure": "Array",
        "Found": found,
        "Comparisons": comps,
        "Time (µs)": f"{elapsed_us:,.2f}",
        "Big-O": "O(n)"
    })

    # -------------------------------------------------------------
    # 2. Linear Search on Unsorted Data with Repetition (Duplicates)
    # -------------------------------------------------------------
    t0 = time.perf_counter()
    found, idx, comps = linear_search_array(unsorted_dup_arr, target_dup)
    elapsed_us = (time.perf_counter() - t0) * 1e6
    results.append({
        "Scenario": "2. Unsorted (With Duplicates)",
        "Algorithm": "Linear Search",
        "Structure": "Array",
        "Found": found,
        "Comparisons": comps,
        "Time (µs)": f"{elapsed_us:,.2f}",
        "Big-O": "O(n) [earlier hit]"
    })

    # -------------------------------------------------------------
    # 3. Linear Search on Unsorted Data without Repetition (Unique)
    # -------------------------------------------------------------
    t0 = time.perf_counter()
    found, idx, comps = linear_search_array(unsorted_uniq_arr, target_uniq)
    elapsed_us = (time.perf_counter() - t0) * 1e6
    results.append({
        "Scenario": "3. Unsorted (Unique Values)",
        "Algorithm": "Linear Search",
        "Structure": "Array",
        "Found": found,
        "Comparisons": comps,
        "Time (µs)": f"{elapsed_us:,.2f}",
        "Big-O": "O(n) [avg n/2]"
    })

    # -------------------------------------------------------------
    # 4. Array vs Linked List Search (Same target on identical data)
    # -------------------------------------------------------------
    # Array search
    t0 = time.perf_counter()
    found, idx, comps = linear_search_array(unsorted_uniq_arr, target_uniq)
    elapsed_us_arr = (time.perf_counter() - t0) * 1e6
    results.append({
        "Scenario": "4. Representation Comparison",
        "Algorithm": "Linear Search",
        "Structure": "Array (list)",
        "Found": found,
        "Comparisons": comps,
        "Time (µs)": f"{elapsed_us_arr:,.2f}",
        "Big-O": "O(n) [Cache friendly]"
    })

    # Linked List search
    t0 = time.perf_counter()
    found, idx, comps = sll.search(target_uniq)
    elapsed_us_ll = (time.perf_counter() - t0) * 1e6
    results.append({
        "Scenario": "4. Representation Comparison",
        "Algorithm": "Linear Search",
        "Structure": "Linked List (SLL)",
        "Found": found,
        "Comparisons": comps,
        "Time (µs)": f"{elapsed_us_ll:,.2f}",
        "Big-O": "O(n) [Pointer chase]"
    })

    # Print Table
    header = f"{'Scenario':<32} | {'Algorithm':<14} | {'Structure':<18} | {'Comps':<7} | {'Time (µs)':<11} | {'Big-O'}"
    print(header)
    print("-" * len(header))
    for r in results:
        print(f"{r['Scenario']:<32} | {r['Algorithm']:<14} | {r['Structure']:<18} | {r['Comparisons']:<7} | {r['Time (µs)']:<11} | {r['Big-O']}")

    print("\n" + "=" * 78)
    print("KEY INSIGHTS:")
    print("1. Binary Search vs Linear Search:")
    print("   Binary search took ~log2(N) comparisons (e.g., ~17 steps for 100k items),")
    print("   making it thousands of times faster than O(n) linear search.")
    print("\n2. Duplicates vs Unique Linear Search:")
    print("   In datasets with duplicates, a frequently occurring target is found much")
    print("   earlier on average because multiple matching candidates exist.")
    print("\n3. Array vs Linked List Search:")
    print("   Although both perform O(n) comparisons, Array linear search is much faster")
    print("   in practice because array elements are stored contiguously in memory,")
    print("   maximizing CPU L1/L2 cache hits. Linked List requires pointer dereferencing")
    print("   at each node, incurring cache misses.")
    print("   Note on Binary Search: Cannot be efficiently applied to Linked Lists because")
    print("   finding the middle node takes O(k) sequential steps rather than O(1) random access.")
    print("=" * 78)


if __name__ == "__main__":
    run_search_comparison()
