"""
================================================================================
        SAVITRIBAI PHULE PUNE UNIVERSITY
        Third Year Computer Engineering - Artificial Intelligence Lab
        Assignment No: 4
================================================================================

TITLE:
    Implement a solution for a Constraint Satisfaction Problem (CSP) using
    Branch and Bound and Backtracking for the N-Queens Problem.

--------------------------------------------------------------------------------
PART 1 - THEORY
--------------------------------------------------------------------------------

1. WHAT IS A CONSTRAINT SATISFACTION PROBLEM (CSP)?
-----------------------------------------------------
A Constraint Satisfaction Problem is a problem where we must find values for
a set of variables such that all given constraints are satisfied.

Components of a CSP:
    - Variables   : Things we need to assign values to.
    - Domain      : Set of possible values each variable can take.
    - Constraints : Rules that the assignment must satisfy.

Examples of CSP:
    - N-Queens Problem
    - Graph Coloring
    - Sudoku
    - Map Coloring
    - Scheduling Problems

Two key techniques to solve CSP:
    a) Backtracking
    b) Branch and Bound


2. WHAT IS BACKTRACKING?
--------------------------
Definition:
    Backtracking is a general algorithm for solving CSPs by trying to build
    a solution incrementally. If at any point a partial solution VIOLATES
    a constraint, we ABANDON it and go back (backtrack) to try a different option.

Key Idea:
    "Try a choice. If it leads to a dead end, UNDO it and try the next choice."

Working:
    1. Start with an empty solution.
    2. Try placing a value for the next variable.
    3. Check if the placement satisfies all constraints.
    4. If YES  -> move to the next variable (go deeper).
    5. If NO   -> try the next value (backtrack).
    6. If all values exhausted -> backtrack to previous variable.
    7. Repeat until solution found or all possibilities exhausted.

Analogy:
    Like solving a maze - if a path is blocked, go back and try another path.


3. WHAT IS BRANCH AND BOUND?
------------------------------
Definition:
    Branch and Bound is an optimization technique that:
    - BRANCHES  : Divides the problem into smaller subproblems (like a tree).
    - BOUNDS    : At each step, calculates a bound (limit) to check if a
                  subproblem can possibly lead to a valid/optimal solution.
                  If NOT possible (bound exceeded), PRUNE that branch entirely.

Difference from Backtracking:
    - Backtracking : Checks constraints only after placing a value.
    - Branch & Bound: Uses bounding functions to PRUNE branches BEFORE
                      exploring them, making it more efficient.

In N-Queens:
    - Branch   : Place a queen in a column and explore that branch.
    - Bound    : Check if the current placement can possibly lead to a
                 valid solution (no conflicts in row, column, diagonal).
                 If not, prune the entire subtree.


4. THE N-QUEENS PROBLEM
-------------------------
Definition:
    Place N queens on an N x N chessboard such that NO two queens
    attack each other.

Rules (Constraints):
    - No two queens in the SAME ROW.
    - No two queens in the SAME COLUMN.
    - No two queens on the SAME DIAGONAL (both left and right diagonals).

For our program, N = 8 (classic 8-Queens problem).

Example - 4 Queens Solution:
    Board (4x4):
        . Q . .
        . . . Q
        Q . . .
        . . Q .

    Queens placed at columns: [1, 3, 0, 2]  (0-indexed)
    Row 0 -> Column 1
    Row 1 -> Column 3
    Row 2 -> Column 0
    Row 3 -> Column 2

Constraint Check between two queens (r1,c1) and (r2,c2):
    - Same Column    : c1 == c2                  -> CONFLICT
    - Same Diagonal  : |r1-r2| == |c1-c2|        -> CONFLICT
    (Same row is impossible since we place one queen per row)


5. ALGORITHM - BACKTRACKING FOR N-QUEENS
------------------------------------------
solve(board, row):
    If row == N:
        All queens placed successfully -> print solution
        Return True

    For each column col from 0 to N-1:
        If placing queen at (row, col) is SAFE:
            Place queen at (row, col)      // Branch
            Recursively solve(board, row+1)
            If recursive call returns True:
                Return True
            Remove queen from (row, col)   // Backtrack (undo placement)

    Return False   // No valid column found in this row -> backtrack

isSafe(board, row, col):
    Check all previously placed queens:
        If any queen is in same column OR same diagonal -> return False
    Return True


6. STEP-BY-STEP TRACE (4-Queens Example)
------------------------------------------
Row 0: Try col 0 -> Place Q at (0,0)
Row 1: Try col 0 -> Conflict (same col). Try col 1 -> Conflict (diagonal).
       Try col 2 -> Place Q at (1,2)
Row 2: Try col 0 -> Conflict (diagonal). Try col 1 -> Conflict. ...
       No valid column -> BACKTRACK to Row 1
Row 1: Try col 3 -> Place Q at (1,3)
Row 2: Try col 1 -> Place Q at (2,1)
Row 3: Try col 3 -> Conflict. No valid column -> BACKTRACK to Row 2
...
Eventually finds: [1, 3, 0, 2] -> Valid solution!


7. COMPLEXITY ANALYSIS
------------------------
    Time Complexity  : O(N!)   -- N choices for row 0, N-1 for row 1, etc.
                                   Backtracking prunes many branches so
                                   actual time is much less than N!
    Space Complexity : O(N)    -- for the board array and recursion stack

    For 8-Queens: 92 distinct solutions exist out of 8! = 40320 possibilities.
    Backtracking explores far fewer than 40320 due to early pruning.


8. DIFFERENCE - BACKTRACKING vs BRANCH AND BOUND
--------------------------------------------------

    Feature              Backtracking              Branch and Bound
    -----------------    ----------------------    ----------------------
    Strategy             Try & undo on failure     Try & prune using bound
    Pruning              After constraint fail     Before exploring branch
    Used for             Feasibility problems      Optimization problems
    Efficiency           Moderate                  Better (more pruning)
    Example              N-Queens, Sudoku          Travelling Salesman


9. APPLICATIONS
----------------
    - Puzzle solving (Sudoku, Crossword)
    - Circuit board layout
    - VLSI chip design
    - Scheduling and timetabling
    - Any problem requiring placement with constraints


10. CONCLUSION
---------------
    - N-Queens is a classic CSP solved using Backtracking.
    - We place one queen per row and check column and diagonal constraints.
    - If a placement is invalid, we backtrack and try the next column.
    - Branch and Bound improves this by pruning invalid branches early.
    - For N=8, there are 92 valid solutions.
    - Backtracking is complete: it always finds a solution if one exists.

================================================================================
PART 2 - PROGRAM
================================================================================
"""


# ============================================================
#  GLOBAL VARIABLE
#  N = size of the chessboard (N x N) and number of queens
# ============================================================
N = 8   # Change this to solve for different board sizes


# ============================================================
#  IS_SAFE FUNCTION (Bounding Function - Branch and Bound)
#  Checks if placing a queen at (row, col) is safe.
#  Parameters:
#    board - list where board[i] = column of queen in row i
#    row   - current row where we want to place the queen
#    col   - column we want to place the queen in
#  Returns:
#    True if safe, False if conflict exists
# ============================================================
def is_safe(board, row, col):

    # Check all previously placed queens (rows 0 to row-1)
    for prev_row in range(row):

        prev_col = board[prev_row]   # Column of queen in prev_row

        # Conflict 1: Same column
        if prev_col == col:
            return False

        # Conflict 2: Same diagonal
        # Two queens are on same diagonal if |row difference| == |col difference|
        if abs(prev_row - row) == abs(prev_col - col):
            return False

    # No conflict found -> placement is safe
    return True


# ============================================================
#  SOLVE FUNCTION (Backtracking)
#  Recursively places queens row by row.
#  Parameters:
#    board     - list to store column positions of queens
#    row       - current row being processed
#    solutions - list to collect all valid solutions
# ============================================================
def solve(board, row, solutions):

    # BASE CASE: All N queens placed successfully
    if row == N:
        solutions.append(board[:])   # Save a copy of the current solution
        return

    # Try placing queen in each column of current row
    for col in range(N):

        # BOUND CHECK: Is placing queen at (row, col) safe?
        if is_safe(board, row, col):

            # BRANCH: Place the queen at (row, col)
            board[row] = col

            # Recurse to place queen in the next row
            solve(board, row + 1, solutions)

            # BACKTRACK: Remove queen (reset position) and try next column
            board[row] = -1


# ============================================================
#  PRINT_BOARD FUNCTION
#  Displays the chessboard with Q for queen and . for empty
#  Parameter:
#    board - list where board[i] = column of queen in row i
# ============================================================
def print_board(board):

    for row in range(N):
        # Build each row: 'Q' at queen's column, '.' elsewhere
        line = ""
        for col in range(N):
            if board[row] == col:
                line += " Q "   # Queen
            else:
                line += " . "   # Empty cell
        print("  " + line)
    print()


# ============================================================
#  MAIN - Entry point of the program
# ============================================================
if __name__ == "__main__":

    # Initialize board with -1 (no queen placed yet)
    board = [-1] * N

    # List to store all valid solutions
    solutions = []

    print("=" * 60)
    print(f"      N-QUEENS PROBLEM (N = {N})")
    print("      Using Backtracking and Branch & Bound")
    print("=" * 60)

    # Run the solver starting from row 0
    solve(board, 0, solutions)

    # Display total number of solutions found
    print(f"\n  Total Solutions Found : {len(solutions)}")
    print("=" * 60)

    # Display first 3 solutions (to keep output readable)
    display_count = min(3, len(solutions))
    for i in range(display_count):
        print(f"\n  Solution {i + 1}:")
        print(f"  Queen positions (col per row): {solutions[i]}")
        print()
        print_board(solutions[i])
        print("-" * 60)

    # Display the very first solution clearly
    if solutions:
        print(f"\n  First Solution Column Positions : {solutions[0]}")
        print("  (board[row] = column where queen is placed in that row)")
    print("=" * 60)