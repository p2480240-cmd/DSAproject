"""
main.py
-------
Single entry-point runner for the DSA Project.
Runs dataset generation, search comparison, and insertion comparison.
"""

import sys
import os

from generate_datasets import write_dataset_to_file, stream_sorted, stream_unsorted_duplicates, stream_unsorted_unique
from search_comparison import run_search_comparison
from insertion_comparison import benchmark_insertion


def run_all(sample_size=100000):
    print("=" * 80)
    print("  DSA BENCHMARK SUITE: DATASETS, SEARCHING & INSERTION")
    print("=" * 80)

    # 1. Dataset Generation
    print("\n[PART 1: DATASET GENERATION]")
    print(f"Generating datasets with N = {sample_size:,} (Memory constraint: O(1) space)...")
    write_dataset_to_file("dataset_sorted.txt", stream_sorted(sample_size), sample_size)
    write_dataset_to_file("dataset_unsorted_duplicates.txt", stream_unsorted_duplicates(sample_size), sample_size)
    write_dataset_to_file("dataset_unsorted_unique.txt", stream_unsorted_unique(sample_size), sample_size)

    # 2. Searching
    print("\n[PART 2: SEARCHING COMPARISON]")
    run_search_comparison(sample_size)

    # 3. Insertion
    print("\n[PART 3: INSERTION COMPARISON]")
    benchmark_insertion(sample_size)

    print("\n" + "=" * 80)
    print("ALL BENCHMARKS COMPLETED SUCCESSFULLY!")
    print("=" * 80)


def show_menu():
    print("\n" + "=" * 50)
    print("       DSA PROJECT - RUNNER MENU")
    print("=" * 50)
    print("1. Run All Benchmarks (Dataset Gen, Search, Insertion)")
    print("2. Run Dataset Generation only (generate_datasets.py)")
    print("3. Run Searching Comparison only (search_comparison.py)")
    print("4. Run Insertion Comparison only (insertion_comparison.py)")
    print("5. Exit")
    print("=" * 50)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        run_all(100000)
        return

    show_menu()
    choice = input("Enter choice (1-5) [default 1]: ").strip()
    if choice in ("", "1"):
        run_all(100000)
    elif choice == "2":
        size_input = input("Enter count N [default 1,000,000]: ").strip()
        n = int(size_input) if size_input.isdigit() else 1000000
        write_dataset_to_file("dataset_sorted.txt", stream_sorted(n), n)
        write_dataset_to_file("dataset_unsorted_duplicates.txt", stream_unsorted_duplicates(n), n)
        write_dataset_to_file("dataset_unsorted_unique.txt", stream_unsorted_unique(n), n)
    elif choice == "3":
        run_search_comparison()
    elif choice == "4":
        benchmark_insertion()
    elif choice == "5":
        print("Exiting.")
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()
