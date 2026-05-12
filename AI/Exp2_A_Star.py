"""
================================================================================
        SAVITRIBAI PHULE PUNE UNIVERSITY
        Third Year Computer Engineering - Artificial Intelligence Lab
        Assignment No: 2
================================================================================

TITLE:
    Implement A* (A-Star) Algorithm for any Game Search Problem.
    Here we solve the problem of finding the shortest path between
    two cities on a map (Romania Map - classic AI textbook example).

--------------------------------------------------------------------------------
PART 1 - THEORY
--------------------------------------------------------------------------------

1. WHAT IS A SEARCH ALGORITHM?
--------------------------------
In Artificial Intelligence, a Search Algorithm is used to find a solution
(path, sequence of actions) from an initial state to a goal state.

Types of Search:
    - Uninformed Search : No extra information used. (e.g., BFS, DFS)
    - Informed Search   : Uses extra knowledge (heuristics) to guide search.
                          (e.g., Greedy Best First Search, A* Search)

A* belongs to INFORMED (Heuristic) Search category.


2. WHAT IS A HEURISTIC?
-------------------------
A Heuristic is an estimated cost from the current node to the goal node.
It is a "guess" that helps the algorithm find the goal faster.

Properties of a Good Heuristic:
    - Admissible  : Never OVERESTIMATES the actual cost to reach the goal.
                    (Guarantees optimal solution)
    - Consistent  : h(n) <= cost(n, n') + h(n') for every neighbor n' of n.

In our example, we use STRAIGHT-LINE DISTANCE (SLD) to Bucharest as the heuristic.
SLD is always <= actual road distance, so it is admissible.


3. WHAT IS A* ALGORITHM?
--------------------------
Definition:
    A* (pronounced "A-Star") is an informed search algorithm that finds the
    SHORTEST PATH from a start node to a goal node using both:
        - g(n) : Actual cost from start node to current node n
        - h(n) : Heuristic (estimated cost from node n to goal)
        - f(n) : Total estimated cost = g(n) + h(n)

    At every step, A* picks the node with the LOWEST f(n) value.

Key Formula:
    f(n) = g(n) + h(n)

    Where:
        g(n) = cost from START to current node n (known, actual)
        h(n) = estimated cost from n to GOAL    (heuristic, approximate)
        f(n) = total estimated path cost        (used for priority)

Working of A*:
    1. Add start node to OPEN LIST with f = h(start)
    2. While OPEN LIST is not empty:
           a. Pick node with lowest f(n) from OPEN LIST  --> current node
           b. If current == GOAL, reconstruct and return path
           c. Move current to CLOSED LIST (already explored)
           d. For each neighbor of current:
                  - Calculate g, h, f values
                  - If neighbor not in CLOSED LIST and not in OPEN LIST:
                        Add to OPEN LIST
                  - If neighbor already in OPEN LIST with higher f:
                        Update with better path
    3. If OPEN LIST is empty and goal not found: No path exists.

Data Structures Used:
    - Open List  (Priority Queue) : Nodes to be explored, sorted by f(n)
    - Closed List (Set)           : Nodes already explored


4. EXAMPLE - ROMANIA MAP PROBLEM
----------------------------------
Problem:
    Find the shortest path from ARAD to BUCHAREST using the Romania road map.
    This is the classic example from the AI textbook by Russell & Norvig.

Map (Selected cities and road distances in km):

    Arad ---140--- Sibiu ---99---- Fagaras ---211--- Bucharest
     |              |                                    |
    118            80                                  101
     |              |                                    |
    Zerind        Rimnicu ---97--- Pitesti ---101--- Bucharest
     |            Vilcea
    75
     |
    Oradea

Heuristic (Straight-Line Distance to Bucharest):
    Arad      : 366 km
    Zerind    : 374 km
    Oradea    : 380 km
    Sibiu     : 253 km
    Fagaras   : 176 km
    Rimnicu   : 193 km
    Pitesti   : 100 km
    Bucharest :   0 km  (goal, distance to itself = 0)

Step-by-Step Trace:
    Step 1: Start = Arad,    g=0,   h=366, f=366
    Step 2: Explore Arad's neighbors:
                Sibiu  : g=140, h=253, f=393
                Zerind : g=75,  h=374, f=449   (via Timisoara)
            Pick lowest f -> Sibiu (f=393)
    Step 3: Explore Sibiu's neighbors:
                Fagaras  : g=239, h=176, f=415
                Rimnicu  : g=220, h=193, f=413
            Pick lowest f -> Rimnicu (f=413)
    Step 4: Explore Rimnicu's neighbors:
                Pitesti  : g=317, h=100, f=417
            Pick lowest f -> Fagaras (f=415)
    Step 5: Explore Fagaras's neighbors:
                Bucharest: g=450, h=0,   f=450
            Pick lowest f -> Pitesti (f=417)
    Step 6: Explore Pitesti's neighbors:
                Bucharest: g=418, h=0,   f=418  <-- BETTER path to Bucharest!
            Pick lowest f -> Bucharest (f=418)  --> GOAL REACHED!

    Final Path : Arad -> Sibiu -> Rimnicu Vilcea -> Pitesti -> Bucharest
    Total Cost : 418 km


5. WHY A* IS BETTER THAN BFS/DFS?
------------------------------------

    Feature              BFS               DFS               A*
    -----------------    --------------    --------------    ------------------
    Strategy             Level by level    Go deep first     Best f(n) first
    Uses Heuristic       No                No                Yes
    Optimal Path         Yes (unweighted)  No                Yes (if admissible h)
    Time Complexity      O(b^d)            O(b^m)            O(b^d) but faster
    Space Complexity     O(b^d)            O(bm)             O(b^d)
    Complete             Yes               No                Yes

    b = branching factor, d = depth of solution, m = max depth


6. PROPERTIES OF A*
---------------------
    - Complete   : Always finds a solution if one exists.
    - Optimal    : Finds the LEAST COST path (if heuristic is admissible).
    - Efficient  : Explores fewer nodes than BFS due to heuristic guidance.


7. APPLICATIONS OF A*
-----------------------
    - GPS Navigation and Route Planning (Google Maps)
    - Game AI: Finding path for characters in games (e.g., chess, pacman)
    - Robotics: Path planning for robots
    - Network Routing Protocols
    - Puzzle Solving (8-puzzle, 15-puzzle)


8. CONCLUSION
--------------
    - A* uses f(n) = g(n) + h(n) to always explore the most promising node.
    - It is complete and optimal when heuristic is admissible.
    - It is widely used in real-world AI applications like navigation and games.
    - The quality of the heuristic directly affects the efficiency of A*.

================================================================================
PART 2 - PROGRAM
================================================================================
"""

import heapq   # heapq gives us a min-heap (priority queue) - picks lowest f(n) first


# ============================================================
#  GRAPH - Romania Road Map
#  Format: { 'City': [('Neighbor', distance), ...] }
#  This is a WEIGHTED UNDIRECTED graph (roads go both ways)
# ============================================================
graph = {
    'Arad'           : [('Zerind', 75),  ('Timisoara', 118), ('Sibiu', 140)],
    'Zerind'         : [('Arad', 75),    ('Oradea', 71)],
    'Oradea'         : [('Zerind', 71),  ('Sibiu', 151)],
    'Timisoara'      : [('Arad', 118),   ('Lugoj', 111)],
    'Lugoj'          : [('Timisoara', 111), ('Mehadia', 70)],
    'Mehadia'        : [('Lugoj', 70),   ('Drobeta', 75)],
    'Drobeta'        : [('Mehadia', 75), ('Craiova', 120)],
    'Sibiu'          : [('Arad', 140),   ('Oradea', 151), ('Fagaras', 99), ('Rimnicu Vilcea', 80)],
    'Rimnicu Vilcea' : [('Sibiu', 80),   ('Pitesti', 97),  ('Craiova', 146)],
    'Fagaras'        : [('Sibiu', 99),   ('Bucharest', 211)],
    'Pitesti'        : [('Rimnicu Vilcea', 97), ('Craiova', 138), ('Bucharest', 101)],
    'Craiova'        : [('Drobeta', 120), ('Rimnicu Vilcea', 146), ('Pitesti', 138)],
    'Bucharest'      : [('Fagaras', 211), ('Pitesti', 101), ('Giurgiu', 90), ('Urziceni', 85)],
    'Giurgiu'        : [('Bucharest', 90)],
    'Urziceni'       : [('Bucharest', 85)]
}


# ============================================================
#  HEURISTIC TABLE
#  Straight-Line Distance (SLD) from each city to Bucharest.
#  This is our h(n) - estimated cost to goal.
#  SLD is admissible because actual road distance >= SLD always.
# ============================================================
heuristic = {
    'Arad'           : 366,
    'Zerind'         : 374,
    'Oradea'         : 380,
    'Timisoara'      : 329,
    'Lugoj'          : 244,
    'Mehadia'        : 241,
    'Drobeta'        : 242,
    'Sibiu'          : 253,
    'Rimnicu Vilcea' : 193,
    'Fagaras'        : 176,
    'Pitesti'        : 100,
    'Craiova'        : 160,
    'Bucharest'      :   0,   # Goal node - distance to itself is 0
    'Giurgiu'        :  77,
    'Urziceni'       :  80
}


# ============================================================
#  A* ALGORITHM FUNCTION
#  Parameters:
#    graph     - weighted adjacency list
#    heuristic - h(n) values for each node
#    start     - starting city
#    goal      - destination city
# ============================================================
def astar(graph, heuristic, start, goal):

    # ---- OPEN LIST (Priority Queue) ----
    # Each entry: (f(n), g(n), current_node, path_so_far)
    # heapq always pops the SMALLEST f(n) first
    open_list = []
    heapq.heappush(open_list, (heuristic[start], 0, start, [start]))
    #                           f(start)=h(start), g=0, node, path

    # ---- CLOSED LIST (Set) ----
    # Stores nodes we have already fully explored
    closed_list = set()

    print("\nA* Search Steps:")
    print("-" * 60)

    # Keep exploring until open list is empty
    while open_list:

        # Pop node with LOWEST f(n) from priority queue
        f, g, current, path = heapq.heappop(open_list)

        # Show current step for understanding
        print(f"  Exploring: {current:20s} | g={g:4d} | h={heuristic[current]:4d} | f={f:4d}")

        # GOAL CHECK: If current node is the goal, we are done!
        if current == goal:
            print("-" * 60)
            return path, g   # Return the path and total cost

        # Skip this node if already explored (in closed list)
        if current in closed_list:
            continue

        # Mark current node as explored
        closed_list.add(current)

        # Explore all neighbors of current node
        for neighbor, cost in graph[current]:

            # Skip neighbor if already fully explored
            if neighbor in closed_list:
                continue

            # Calculate g(neighbor) = g(current) + edge cost
            g_new = g + cost

            # Calculate h(neighbor) = heuristic value of neighbor
            h_new = heuristic[neighbor]

            # Calculate f(neighbor) = g + h
            f_new = g_new + h_new

            # Add neighbor to open list with updated path
            heapq.heappush(open_list, (f_new, g_new, neighbor, path + [neighbor]))

    # If we reach here, no path was found
    return None, float('inf')


# ============================================================
#  MAIN - Entry point of the program
# ============================================================
if __name__ == "__main__":

    # Define start and goal cities
    start_city = 'Arad'
    goal_city  = 'Bucharest'

    print("=" * 60)
    print("        A* ALGORITHM - ROMANIA MAP PROBLEM")
    print("=" * 60)
    print(f"  Start : {start_city}")
    print(f"  Goal  : {goal_city}")
    print("=" * 60)

    # Run A* algorithm
    path, total_cost = astar(graph, heuristic, start_city, goal_city)

    # Display the result
    if path:
        print(f"\n  Optimal Path Found!")
        print(f"  Path : {' -> '.join(path)}")
        print(f"  Total Distance : {total_cost} km")
    else:
        print("\n  No path found between the given cities.")

    print("=" * 60)