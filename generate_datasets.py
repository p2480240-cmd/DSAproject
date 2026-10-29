"""
generate_datasets.py
--------------------
Generates 3 datasets containing N integers and saves them into text files:
1. Sorted sequence: 1, 2, 3, ..., N
2. Unsorted with duplicates: pseudo-random numbers with repetition allowed
3. Unsorted unique: full pseudo-random permutation where every number is unique

CONSTRAINT SATISFIED:
Every generator operates in O(1) auxiliary space (streaming generators).
NO one-billion-element list or set is ever constructed in memory.

Writing is buffered in chunks (e.g., 100,000 lines) for maximum disk I/O speed.
"""

import os
import sys
import time
import argparse


def stream_sorted(n):
    """
    Generator yielding sorted numbers from 1 to n.
    Memory: O(1).
    """
    for i in range(1, n + 1):
        yield i


def stream_unsorted_duplicates(n, max_val=None):
    """
    Generator yielding n unsorted numbers with duplicates allowed.
    Uses a fast linear congruential PRNG for high throughput.
    Memory: O(1).
    """
    if max_val is None:
        max_val = max(100, n // 10)
    seed = 123456789
    for _ in range(n):
        seed = (1103515245 * seed + 12345) & 0x7FFFFFFF
        yield (seed % max_val) + 1


def stream_unsorted_unique(n):
    """
    Generator yielding a permutation of numbers 1..n in pseudo-random order.
    Every single number is UNIQUE.
    
    Uses Hull-Dobell Theorem on a power-of-two LCG:
    m is smallest power of 2 >= n.
    For power of 2:
      - c is odd: gcd(c, m) = 1
      - a = 4k + 1: (a - 1) is divisible by 4
    Guarantees full cycle over [0, m-1]. We reject values >= n.
    
    Memory: O(1). Never builds a list or set.
    """
    m = 1
    while m < n:
        m <<= 1
    mask = m - 1
    a = 1664525 * 4 + 1
    c = 1013904223
    x = 42
    count = 0
    while count < n:
        x = (a * x + c) & mask
        if x < n:
            yield x + 1
            count += 1


def write_dataset_to_file(filename, generator, total_count, chunk_size=100000):
    """
    Writes elements from generator into filename in buffered chunks.
    Keeps memory footprint constant (O(chunk_size) << O(N)).
    """
    print(f"\nWriting '{filename}' ({total_count:,} integers)...")
    t0 = time.time()
    
    written = 0
    buffer = []
    
    with open(filename, 'w', buffering=4 * 1024 * 1024) as f:
        for val in generator:
            buffer.append(f"{val}\n")
            written += 1
            
            if len(buffer) >= chunk_size:
                f.writelines(buffer)
                buffer.clear()
                
                # Report progress every 1,000,000 numbers or 10%
                if written % 1000000 == 0 or written == total_count:
                    percent = (written / total_count) * 100
                    elapsed = time.time() - t0
                    rate = written / elapsed if elapsed > 0 else 0
                    print(f"  Progress: {written:,} / {total_count:,} ({percent:5.1f}%) | "
                          f"Rate: {rate:,.0f} ints/sec", end='\r', flush=True)
        
        if buffer:
            f.writelines(buffer)
            buffer.clear()
            
    elapsed = time.time() - t0
    file_size_mb = os.path.getsize(filename) / (1024 * 1024)
    print(f"\n  Done! Time: {elapsed:.2f}s | Size: {file_size_mb:.2f} MB ({file_size_mb / 1024:.2f} GB)")


def main():
    parser = argparse.ArgumentParser(description="Dataset Generator (O(1) memory)")
    parser.add_argument(
        "--size", "-n",
        type=int,
        default=1000000,
        help="Number of integers to generate per file (default: 1,000,000 for quick testing; pass 1000000000 for 1 billion)"
    )
    args = parser.parse_args()
    n = args.size

    print("=" * 65)
    print("DATASET GENERATION (Memory-Safe Streaming)")
    print("=" * 65)
    print(f"Target count per dataset: {n:,}")
    if n >= 1000000000:
        print("Note: 1,000,000,000 integers in text format takes ~10-11 GB per file.")
        print("Ensure you have at least 35 GB free disk space.")
    print("Memory constraint: Generators run in O(1) RAM. No N-element list created.")
    print("-" * 65)

    # 1. Sorted
    write_dataset_to_file("dataset_sorted.txt", stream_sorted(n), n)

    # 2. Unsorted with duplicates
    write_dataset_to_file("dataset_unsorted_duplicates.txt", stream_unsorted_duplicates(n), n)

    # 3. Unsorted unique
    write_dataset_to_file("dataset_unsorted_unique.txt", stream_unsorted_unique(n), n)

    print("\nAll 3 datasets successfully generated!")


if __name__ == "__main__":
    main()
