# DSA Project: Dataset Generation, Searching & Insertion Benchmarks

This repository contains clean, modular, and simple programs addressing the three core problems:
1. **Dataset Generation (1 Billion Integers)** with strictly $O(1)$ auxiliary memory (no 1B-element list or set).
2. **Searching Comparison**: Binary search vs Linear search on sorted, duplicated, and unique data; Array vs Linked List.
3. **Insertion Comparison**: Performance at Beginning ($0$), End ($N$), and Specified Position ($k$) across Arrays and Linked Lists.

---

## 📁 Repository Structure

```text
├── generate_datasets.py     # Stream-generates sorted, duplicated, and unique datasets in O(1) RAM
├── data_structures.py       # Clean Singly Linked List (SLL) and Doubly Linked List (DLL) implementations
├── search_comparison.py     # Compares Binary Search, Linear Search, duplicates vs unique, and Array vs SLL
├── insertion_comparison.py  # Compares insertion at beginning, middle (k), and end
├── main.py                  # Single-command runner & interactive menu
└── README.md                # Comprehensive documentation and analysis
```

---

## 1. Dataset Generation

### Requirements & Solutions
Generates 3 text files of $N$ integers (supports $N = 1,000,000,000$):
1. **Sorted sequence**: Sequential integers ($1, 2, 3, \dots, N$).
2. **Unsorted sequence with duplicates**: Generated using a fast PRNG mapped over a modulo range.
3. **Unsorted sequence with unique values**: Generates a complete pseudo-random permutation of $1 \dots N$ with **zero duplicates**.

### Satisfying the 1-Billion Constraint ($O(1)$ Space)
> **Constraint**: *Each generator must avoid building a one-billion-element Python list.*

- A 1-billion integer list in Python would require over **36 GB of RAM**, causing an immediate out-of-memory crash.
- **Solution**: We use **Python generator streams (`yield`)**:
  - For unique unsorted integers, we use the **Hull-Dobell Theorem** on a power-of-two Linear Congruential Generator ($x_{n+1} = (a \cdot x_n + c) \pmod m$). Because $m = 2^{30} \ge 10^9$, $c$ is odd, and $a \equiv 1 \pmod 4$, every number from $0$ to $m-1$ is visited exactly once before any repeat.
  - Generates numbers on the fly in **$O(1)$ memory** (storing only a single state variable).
  - To maximize disk speed, numbers are written in buffered chunks (e.g., 100,000 lines per disk flush).

### Running Dataset Generation
```powershell
# For quick testing (default: 1,000,000 integers per file)
python generate_datasets.py --size 1000000

# For the full 1 billion integers (requires ~35 GB free disk space)
python generate_datasets.py --size 1000000000
```

---

## 2. Searching Comparison

Compares search performance across 4 scenarios:

| Scenario / Comparison | Algorithm | Data Structure | Time Complexity | Comparisons | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Sorted Data** | **Binary Search** | Array | $O(\log n)$ | $\le 17$ steps | Halves search space each step |
| **Sorted Data** | **Linear Search** | Array | $O(n)$ | $\sim 75,000$ steps | Scans sequentially |
| **Unsorted (Duplicates)** | **Linear Search** | Array | $O(n)$ | Variable (earlier) | High-frequency targets match much sooner |
| **Unsorted (Unique)** | **Linear Search** | Array | $O(n)$ | $\sim n/2$ average | Uniform random position |
| **Array vs Linked List** | **Linear Search** | Array vs SLL | $O(n)$ vs $O(n)$ | Identical count | **Array is faster**: Contiguous memory (CPU cache hits) vs pointer dereferencing |

> [!NOTE]
> **Can we Binary Search a Linked List?**  
> No. Binary search requires $O(1)$ random access (`arr[mid]`). On a linked list, reaching the middle node requires $O(k)$ pointer traversal, resulting in $O(n)$ overall runtime and negating the benefit of binary search.

### Running Search Comparison
```powershell
python search_comparison.py
```

---

## 3. Insertion Comparison

Compares insertion at the **Beginning** ($0$), **Middle** ($k$), and **End** ($N$):

| Position | Data Structure | Time Complexity | Real Time ($\mu\text{s}$) | Why? (Underlying Mechanism) |
| :--- | :--- | :--- | :--- | :--- |
| **Beginning** ($0$) | **Array (list)** | $O(n)$ | **623.3 µs** | Every element in memory shifts right by 1 |
| **Beginning** ($0$) | **Linked List (SLL)** | $O(1)$ | **11.3 µs** | Updates head pointer (`new_node.next = head`) |
| **Beginning** ($0$) | **Doubly Linked List**| $O(1)$ | **3.7 µs** | Rewires head and prev/next links |
| **Specified $k$** | **Array (list)** | $O(n - k)$ | **45.5 µs** | Shifting elements in optimized C memory blocks |
| **Specified $k$** | **Linked List (SLL)** | $O(k)$ | **1,454.1 µs** | Traverses $k$ nodes from head before splicing |
| **Specified $k$** | **Doubly Linked List**| $O(k)$ | **1,379.3 µs** | Traverses to node $k$ before splicing |
| **End** ($N$) | **Array (list)** | $O(1)$ amortized | **0.5 µs** | Writes to pre-allocated buffer capacity |
| **End** ($N$) | **Linked List (SLL)** | $O(1)$ | **4.8 µs** | Direct tail pointer update (`tail.next = node`) |
| **End** ($N$) | **Doubly Linked List**| $O(1)$ | **0.9 µs** | Direct tail pointer update |

### Running Insertion Comparison
```powershell
python insertion_comparison.py
```

---

## 4. One-Click Runner

To run the entire suite automatically in sequence:
```powershell
python main.py --all
```
Or run `python main.py` for the interactive menu.
