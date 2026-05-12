"""
================================================================================
        SAVITRIBAI PHULE PUNE UNIVERSITY
        Third Year Computer Engineering - Artificial Intelligence Lab
        Assignment No: 3
================================================================================

TITLE:
    Implement Greedy Search Algorithm for Selection Sort.

--------------------------------------------------------------------------------
PART 1 - THEORY
--------------------------------------------------------------------------------

1. WHAT IS A GREEDY ALGORITHM?
--------------------------------
A Greedy Algorithm is a problem-solving strategy that makes the LOCALLY OPTIMAL
choice at each step, hoping to find the GLOBAL OPTIMAL solution.

Key Idea:
    "At every step, pick the BEST available option right now,
     without worrying about future consequences."

Properties of Greedy Algorithms:
    - Greedy Choice Property : A global solution can be built by making
                               locally optimal (greedy) choices.
    - Optimal Substructure   : Optimal solution to a problem contains
                               optimal solutions to its subproblems.

When to use Greedy?
    - When the problem has optimal substructure.
    - When a locally optimal choice leads to a globally optimal solution.
    - Examples: Sorting, Scheduling, Spanning Trees, Shortest Paths.


2. WHAT IS SELECTION SORT?
----------------------------
Definition:
    Selection Sort is a simple comparison-based sorting algorithm that uses
    the Greedy approach. It repeatedly selects the MINIMUM element from the
    unsorted portion and places it at the correct position.

Greedy Strategy in Selection Sort:
    "At each step, GREEDILY pick the smallest element from the remaining
     unsorted part and place it at the beginning of that part."

    This is greedy because at every pass, we make the locally best decision
    (pick the minimum) without reconsidering previous choices.

Working of Selection Sort:
    - Divide the array into two parts:
          * Sorted part   : Left side (initially empty)
          * Unsorted part : Right side (initially whole array)
    - Find the MINIMUM element in the unsorted part.
    - SWAP it with the first element of the unsorted part.
    - Expand the sorted part by one position.
    - Repeat until the entire array is sorted.


3. STEP-BY-STEP EXAMPLE
--------------------------
Input Array: [64, 25, 12, 22, 11]

Pass 1:
    Unsorted: [64, 25, 12, 22, 11]
    Minimum = 11 (at index 4)
    Swap 64 and 11
    Result:   [11, 25, 12, 22, 64]
    Sorted:   [11] | Unsorted: [25, 12, 22, 64]

Pass 2:
    Unsorted: [25, 12, 22, 64]
    Minimum = 12 (at index 2)
    Swap 25 and 12
    Result:   [11, 12, 25, 22, 64]
    Sorted:   [11, 12] | Unsorted: [25, 22, 64]

Pass 3:
    Unsorted: [25, 22, 64]
    Minimum = 22 (at index 3)
    Swap 25 and 22
    Result:   [11, 12, 22, 25, 64]
    Sorted:   [11, 12, 22] | Unsorted: [25, 64]

Pass 4:
    Unsorted: [25, 64]
    Minimum = 25 (already in place, no swap)
    Result:   [11, 12, 22, 25, 64]
    Sorted:   [11, 12, 22, 25] | Unsorted: [64]

Pass 5:
    Only one element left -> already sorted.
    Final:    [11, 12, 22, 25, 64]


4. ALGORITHM
--------------
SelectionSort(arr):
    n = length of arr
    For i from 0 to n-2:
        min_index = i                        // Assume first unsorted is minimum
        For j from i+1 to n-1:
            If arr[j] < arr[min_index]:
                min_index = j                // Found a smaller element
        If min_index != i:
            Swap arr[i] and arr[min_index]   // Place minimum at correct position


5. COMPLEXITY ANALYSIS
------------------------
    Case              Comparisons        Swaps
    --------------    ---------------    ----------
    Best Case         O(n^2)             O(1)
    Worst Case        O(n^2)             O(n)
    Average Case      O(n^2)             O(n)

    Time Complexity  : O(n^2)  -- two nested loops
    Space Complexity : O(1)    -- in-place sorting, no extra space needed

Note:
    - Selection Sort makes at most O(n) swaps, making it useful when
      WRITE operations are costly (e.g., flash memory).
    - It is NOT stable (equal elements may change relative order).


6. DIFFERENCE - GREEDY vs OTHER SORTING
------------------------------------------

    Feature              Selection Sort       Bubble Sort        Insertion Sort
    -----------------    -----------------    ---------------    ---------------
    Strategy             Greedy (pick min)    Compare adjacent   Build sorted part
    Time Complexity      O(n^2)               O(n^2)             O(n^2)
    Swaps                O(n) max             O(n^2) max         O(n^2) max
    Stable               No                   Yes                Yes
    Space                O(1)                 O(1)               O(1)
    Best for             Min writes needed    Nearly sorted      Nearly sorted


7. APPLICATIONS OF GREEDY SORTING
------------------------------------
    - Used when memory writes are expensive (minimizes swaps).
    - Small datasets where simplicity is more important than speed.
    - As a subroutine in more complex algorithms.
    - Teaching and understanding greedy strategy fundamentals.


8. CONCLUSION
--------------
    - Selection Sort uses Greedy approach: always pick the minimum element.
    - It is simple to understand and implement.
    - Time complexity is O(n^2) in all cases, making it slow for large data.
    - It has an advantage of minimum number of swaps (at most n-1 swaps).
    - Greedy does NOT always give the globally optimal solution for all
      problems, but for sorting, the greedy choice (pick minimum) always
      leads to the correct final sorted array.

================================================================================
PART 2 - PROGRAM
================================================================================
"""


# ============================================================
#  SELECTION SORT FUNCTION (Greedy Approach)
#  Parameter:
#    arr - the list of numbers to be sorted
#  Returns:
#    sorted list (in-place, original list is modified)
# ============================================================
def selection_sort(arr):

    # n = total number of elements in the array
    n = len(arr)

    # Outer loop: represents the boundary of sorted | unsorted parts
    # After each pass, i-th position gets the correct (minimum) element
    for i in range(n - 1):

        # GREEDY CHOICE: Assume the first element of unsorted part is minimum
        min_index = i

        # Inner loop: scan the entire unsorted part to find the true minimum
        for j in range(i + 1, n):

            # If we find an element smaller than current minimum, update index
            if arr[j] < arr[min_index]:
                min_index = j       # Greedy update: new minimum found

        # Only swap if we found a smaller element (min is not already in place)
        if min_index != i:
            arr[i], arr[min_index] = arr[min_index], arr[i]   # Swap

        # Show state of array after each pass (for understanding)
        sorted_part   = arr[:i+1]
        unsorted_part = arr[i+1:]
        print(f"  Pass {i+1}: {sorted_part} | {unsorted_part}  "
              f"(min={arr[i]}, swapped with index {min_index})" if min_index != i
              else f"  Pass {i+1}: {sorted_part} | {unsorted_part}  "
              f"(min={arr[i]}, already in place)")

    return arr


# ============================================================
#  MAIN - Entry point of the program
# ============================================================
if __name__ == "__main__":

    # Input array to be sorted
    arr = [64, 25, 12, 22, 11]

    print("=" * 60)
    print("     GREEDY ALGORITHM - SELECTION SORT")
    print("=" * 60)

    # Display original array before sorting
    print(f"\n  Original Array : {arr}")
    print(f"  Total Elements : {len(arr)}")
    print("\n  Sorted | Unsorted parts shown after each pass:")
    print("-" * 60)

    # Call selection sort - array is sorted in-place
    selection_sort(arr)

    print("-" * 60)

    # Display final sorted array
    print(f"\n  Sorted Array   : {arr}")
    print("=" * 60)