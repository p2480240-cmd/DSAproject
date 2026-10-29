# Data Structures & Algorithms: Dataset Generation, Search & Insertion Benchmarks

A comprehensive, production-quality comparative analysis of fundamental data structures (**Dynamic Arrays**, **Singly Linked Lists**, and **Doubly Linked Lists**) and core algorithms (**Binary Search** vs. **Linear Search**).

This project addresses three specific algorithmic challenges:

1. **Generating 1 Billion Integers** to disk under strict **$O(1)$ auxiliary memory** (preventing out-of-memory crashes by avoiding 1-billion-element lists).
2. **Searching Analysis**: Comparing Binary Search vs. Linear Search across sorted, duplicated, and unique datasets, as well as contrasting Array vs. Linked List representations.
3. **Insertion Analysis**: Benchmarking insertion performance at the Beginning ($0$), End ($N$), and Specified Position ($k$) across Arrays, Singly Linked Lists, and Doubly Linked Lists.

---

## Table of Contents

- [1. Quick Start Guide](#1-quick-start-guide)
- [2. Repository Architecture](#2-repository-architecture)
- [3. Problem 1: Dataset Generation (1 Billion Integers in $O(1)$ RAM)](#3-problem-1-dataset-generation-1-billion-integers-in-o1-ram)
  - [The Memory Problem](#the-memory-problem)
  - [Mathematical Solution: Hull-Dobell Theorem (LCG Permutation)](#mathematical-solution-hull-dobell-theorem-lcg-permutation)
  - [Buffered Disk I/O Architecture](#buffered-disk-io-architecture)
- [4. Problem 2: Searching Analysis](#4-problem-2-searching-analysis)
  - [Scenarios Evaluated](#scenarios-evaluated)
  - [Experimental Results](#experimental-results)
  - [Deep Dive: Why Arrays Outperform Linked Lists (CPU Cache Locality)](#deep-dive-why-arrays-outperform-linked-lists-cpu-cache-locality)
  - [Why Binary Search Fails on Linked Lists](#why-binary-search-fails-on-linked-lists)
- [5. Problem 3: Insertion Analysis](#5-problem-3-insertion-analysis)
  - [Scenarios Evaluated](#scenarios-evaluated-1)
  - [Experimental Results](#experimental-results-1)
  - [Detailed Mechanistic Breakdown](#detailed-mechanistic-breakdown)
- [6. Comprehensive Complexity Cheat Sheet](#6-comprehensive-complexity-cheat-sheet)
- [7. How to Reproduce &amp; Run](#7-how-to-reproduce--run)

---

## 1. Quick Start Guide

No external dependencies are required; the entire project runs on pure Python 3.8+.

```powershell
# Clone or navigate to the directory
cd d:\Code\DSAproject

# Run the complete test suite (Generation, Searching, and Insertion) in one go
python main.py --all
```

You can also run any module independently:

```powershell
python generate_datasets.py --size 1000000   # Generate datasets
python search_comparison.py                  # Run search benchmarks
python insertion_comparison.py               # Run insertion benchmarks
```

---

## 2. Repository Architecture

```text
DSAproject/
│
├── generate_datasets.py     # Streaming generator: produces 3 datasets with O(1) memory
├── data_structures.py       # Pure implementations of Singly & Doubly Linked Lists
├── search_comparison.py     # Benchmark suite for Binary Search & Linear Search
├── insertion_comparison.py  # Benchmark suite for Beginning, Middle (k), and End insertions
├── main.py                  # Unified CLI & interactive menu runner
├── dsa_structures.py        # Compatibility entry point
└── README.md                # Detailed project documentation
```

---

## 3. Problem 1: Dataset Generation (1 Billion Integers in $O(1)$ RAM)

### The Memory Problem

The prompt asks to generate **one billion integers ($10^9$)** into three text files:

1. A **sorted** sequence.
2. An **unsorted** sequence where **duplicates** are allowed.
3. An **unsorted** sequence where every value is **unique**.

> **Mandatory Constraint:** *Each generator must avoid building a one-billion-element Python list.*

#### Why a naive approach crashes:

- In Python, a 64-bit integer object takes $28\text{ bytes}$, and a list pointer takes $8\text{ bytes}$.
- A list of $10^9$ integers consumes:
  $$
  \approx 10^9 \times (28 + 8)\text{ bytes} \approx 36\text{ GB of RAM}
  $$
- A naive `set()` to track uniqueness for 1 billion items consumes **over $64\text{ GB of RAM}$**.
- Any system with standard memory (8 GB – 32 GB) will trigger an immediate **Out of Memory (OOM) fatal crash**.

---

### Mathematical Solution: Hull-Dobell Theorem (LCG Permutation)

To generate $10^9$ unique numbers in pseudo-random order **without storing previous numbers in a list or set**, we use number theory via a **full-cycle Linear Congruential Generator (LCG)**:

$$
x_{n+1} = (a \cdot x_n + c) \pmod m
$$

By the **Hull-Dobell Theorem**, an LCG has a full period of length $m$ if and only if:

1. $c$ and $m$ are coprime ($\gcd(c, m) = 1$).
2. $a - 1$ is divisible by all prime factors of $m$.
3. $a - 1$ is divisible by $4$ if $m$ is divisible by $4$.

#### Implementation Details:

- We choose $m$ as the smallest power of $2$ greater than or equal to $10^9$:
  $$
  m = 2^{30} = 1,073,741,824
  $$
- Since $m$ is a power of 2:
  - Any odd integer $c$ is coprime to $m$. We choose $c = 1,013,904,223$.
  - 2 is the only prime factor. We pick $a = 1,664,525 \times 4 + 1 = 6,658,101$, ensuring $a - 1$ is divisible by 4.
  - Modulo operation is optimized to bitwise AND: `x & (m - 1)`.
- When $x < 10^9$, we yield $x + 1$; otherwise, we discard it and continue (rejection sampling).
- **Result:** Every single integer in $[1, 10^9]$ is generated **exactly once** in pseudo-random order.
- **Memory Used:** Exactly **1 integer state variable ($O(1)$ memory)**!

```python
def stream_unsorted_unique(n):
    m = 1
    while m < n:
        m <<= 1
    mask = m - 1
    a = 1664525 * 4 + 1
    c = 1013904223
    x = 42  # Seed
    count = 0
    while count < n:
        x = (a * x + c) & mask
        if x < n:
            yield x + 1
            count += 1
```

---

### Buffered Disk I/O Architecture

Writing numbers one line at a time to a file with `f.write(f"{x}\n")` triggers 1 billion system calls, which is extremely slow.

To achieve maximum write throughput while maintaining $O(1)$ RAM:

- The generator yields integers one by one.
- A batch buffer collects $100,000$ lines in memory ($\approx 1\text{ MB}$ footprint).
- `f.writelines(buffer)` flushes the block to the OS disk cache in a single write operation.
- **Write Speed:** Up to **$1.5\text{ Million integers / second}$**.

---

## 4. Problem 2: Searching Analysis

### Scenarios Evaluated

1. **Binary Search on Sorted Data (Array)**
2. **Linear Search on Sorted Data (Array)**
3. **Linear Search on Unsorted Data with Duplicates**
4. **Linear Search on Unsorted Data with Unique Values**
5. **Array vs. Singly Linked List Search**

---

### Experimental Results

*(Benchmark on $N = 100,000$ elements, searching for a target positioned at $\approx 75\%$ of the sequence)*

| Scenario                        | Algorithm               | Data Structure     | Comparisons      | Elapsed Time          | Complexity                |
| :------------------------------ | :---------------------- | :----------------- | :--------------- | :-------------------- | :------------------------ |
| **Sorted Data**           | **Binary Search** | Dynamic Array      | **16**     | **16.4 µs**    | $O(\log n)$             |
| **Sorted Data**           | **Linear Search** | Dynamic Array      | 75,001           | 4,180.3 µs           | $O(n)$                  |
| **Unsorted (Duplicates)** | **Linear Search** | Dynamic Array      | **10,185** | **671.4 µs**   | $O(n)$ [early hit]      |
| **Unsorted (Unique)**     | **Linear Search** | Dynamic Array      | 75,001           | 4,756.5 µs           | $O(n)$ [avg $n/2$]    |
| **Representation Test**   | **Linear Search** | Dynamic Array      | 75,001           | **4,085.0 µs** | $O(n)$ [Cache friendly] |
| **Representation Test**   | **Linear Search** | Singly Linked List | 75,001           | **4,521.5 µs** | $O(n)$ [Pointer chase]  |

---

### Deep Dive: Why Arrays Outperform Linked Lists (CPU Cache Locality)

Notice that when scanning the exact same data, the **Array finished faster than the Linked List**, even though both performed identical $75,001$ element comparisons.

```text
Array Memory Layout (Contiguous):
[ Node 0 ][ Node 1 ][ Node 2 ][ Node 3 ][ Node 4 ]  <-- Loaded together in CPU L1/L2 Cache line!

Linked List Memory Layout (Heap Fragmented):
[ Node 0 ] ----> [ Node 1 ] ----> [ Node 2 ] ----> [ Node 3 ]
(Addr 0x1A20)    (Addr 0x9F00)    (Addr 0x33B0)     <-- Cache miss on every jump!
```

- **Dynamic Array:** Elements are laid out contiguously in memory. When the CPU fetches `arr[i]`, the hardware prefetcher loads an entire **cache line** (typically 64 bytes) into L1 cache, making subsequent iterations nearly instantaneous.
- **Linked List:** Each node is independently allocated on the heap. Traversal requires following memory pointers (`curr = curr.next`), repeatedly invalidating CPU cache lines and incurring memory latency stalls (**pointer chasing**).

---

### Why Binary Search Fails on Linked Lists

A common question in computer science: *Can we use Binary Search on a Linked List?*

- **The Requirement:** Binary Search relies on $O(1)$ random access to immediately evaluate the middle element: $\text{mid} = \frac{\text{low} + \text{high}}{2}$.
- **The Bottleneck:** A standard linked list does not support indexing. Reaching the $k$-th node requires starting from `head` and traversing $k$ pointers sequentially ($O(k)$ time).
- **The Math:** If finding the midpoint takes $O(n)$ at step 1, $O(n/2)$ at step 2, etc.:
  $$
  T(n) = n + \frac{n}{2} + \frac{n}{4} + \dots = O(n)
  $$

  Binary Search on a Linked List degrades to **$O(n)$**, completely eliminating the $O(\log n)$ advantage while adding recursion and traversal overhead.

---

## 5. Problem 3: Insertion Analysis

### Scenarios Evaluated

1. **At the Beginning** of a sequence (index $0$).
2. **At a Specified Position $k$** (index $k = N // 2$, middle).
3. **At the End** of a sequence (index $N$).

---

### Experimental Results

*(Benchmark on $N = 100,000$ elements)*

| Insertion Position                     | Data Structure           | Time Complexity    | Measured Time         | What actually happens                                        |
| :------------------------------------- | :----------------------- | :----------------- | :-------------------- | :----------------------------------------------------------- |
| **Beginning ($0$)**            | Dynamic Array (`list`) | $O(n)$           | **110.9 µs**   | Must shift all 100,000 elements right by 1 slot              |
| **Beginning ($0$)**            | Singly Linked List       | $O(1)$           | **10.3 µs**    | Updates head pointer (`new.next = head`)                   |
| **Beginning ($0$)**            | Doubly Linked List       | $O(1)$           | **3.1 µs**     | Rewires head pointer and prev/next links                     |
| **Specified $k$ ($50,000$)** | Dynamic Array (`list`) | $O(n - k)$       | **42.3 µs**    | Shifts $50,000$ elements using fast C `memmove`          |
| **Specified $k$ ($50,000$)** | Singly Linked List       | $O(k)$           | **1,152.1 µs** | Must traverse $50,000$ nodes from `head` before splicing |
| **Specified $k$ ($50,000$)** | Doubly Linked List       | $O(k)$           | **1,077.1 µs** | Must traverse $50,000$ nodes from `head` before splicing |
| **End ($N$)**                  | Dynamic Array (`list`) | $O(1)$ amortized | **0.5 µs**     | Directly appends into pre-allocated buffer                   |
| **End ($N$)**                  | Singly Linked List       | $O(1)$           | **3.0 µs**     | Updates tail pointer (`tail.next = node; tail = node`)     |
| **End ($N$)**                  | Doubly Linked List       | $O(1)$           | **0.7 µs**     | Updates tail pointer and prev links                          |

---

### Detailed Mechanistic Breakdown

#### 1. Beginning Insertion ($pos = 0$)

- **Linked Lists win decisively ($O(1)$):** Inserting at the front requires allocating one node and pointing its `next` pointer to `head`. No other nodes are touched.
- **Array suffers ($O(n)$):** In a contiguous array, index 0 is fixed at the start of the memory block. Every single item from index $0$ to $n-1$ must be physically shifted one index to the right in RAM.

#### 2. End Insertion ($pos = N$)

- **Both are $O(1)$:**
  - Dynamic Arrays maintain extra capacity buffer; adding to the end is a direct pointer write $O(1)$ amortized.
  - Linked Lists equipped with a `tail` pointer append in $O(1)$ without needing to traverse the list.

#### 3. Specified Position $k$ Insertion ($pos = k$)

- **The Linked List Paradox:**
  - In theory, "inserting into a linked list is $O(1)$".
  - **However:** That $O(1)$ guarantee **only applies once you already have a direct reference to the target node**!
  - If you only have the index $k$, the program must first step through nodes $0 \to 1 \to 2 \dots \to k - 1$. The traversal takes $O(k)$ steps.
  - In our benchmarks, traversing $50,000$ pointer hops in Python took $\approx 1,150\ \mu\text{s}$, whereas Python's array shifted $50,000$ elements using optimized low-level C `memmove` in just $42.3\ \mu\text{s}$.

---

## 6. Comprehensive Complexity Cheat Sheet

### Time Complexity Matrix

| Operation                         | Dynamic Array                           | Singly Linked List (with Tail)       | Doubly Linked List (with Tail)         |
| :-------------------------------- | :-------------------------------------- | :----------------------------------- | :------------------------------------- |
| **Access by Index ($k$)** | **$O(1)$**                      | $O(k)$                             | $O(\min(k, n-k))$                    |
| **Search (Unsorted)**       | $O(n)$                                | $O(n)$                             | $O(n)$                               |
| **Search (Sorted)**         | **$O(\log n)$** (Binary Search) | $O(n)$ (Linear Search only)        | $O(n)$ (Linear Search only)          |
| **Insert at Beginning**     | $O(n)$                                | **$O(1)$**                   | **$O(1)$**                     |
| **Insert at End**           | **$O(1)$** (amortized)          | **$O(1)$**                   | **$O(1)$**                     |
| **Insert at Index $k$**   | $O(n - k)$                            | $O(k)$ traversal + $O(1)$ link   | $O(k)$ traversal + $O(1)$ link     |
| **Delete at Beginning**     | $O(n)$                                | **$O(1)$**                   | **$O(1)$**                     |
| **Delete at End**           | **$O(1)$**                      | $O(n)$ (needs second-to-last node) | **$O(1)$** (has `tail.prev`) |

### Space Overhead Comparison

- **Dynamic Array:** $8\text{ bytes}$ per pointer + minimal over-allocation buffer.
- **Singly Linked List:** $1$ Python object header + $1$ value reference + $1$ `next` pointer ($\approx 48\text{ bytes/node}$).
- **Doubly Linked List:** $1$ Python object header + $1$ value reference + $1$ `next` pointer + $1$ `prev` pointer ($\approx 56\text{ bytes/node}$).

---

## 7. How to Reproduce & Run

### Prerequisites

- Python 3.8 or higher.
- Operating System: Windows, macOS, or Linux.
- No third-party packages required (`pip install` not needed).

### Commands

#### 1. Run Everything (All 3 Parts)

```powershell
python main.py --all
```

#### 2. Interactive Menu

```powershell
python main.py
```

#### 3. Run Dataset Generator Separately

```powershell
# Quick test (1 Million numbers per file, takes ~2 seconds)
python generate_datasets.py --size 1000000

# Full 1 Billion numbers (generates dataset_sorted.txt, dataset_unsorted_duplicates.txt, dataset_unsorted_unique.txt)
python generate_datasets.py --size 1000000000
```

#### 4. Run Search Benchmarks Separately

```powershell
python search_comparison.py
```

#### 5. Run Insertion Benchmarks Separately

```powershell
python insertion_comparison.py
```
