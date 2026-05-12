"""
================================================================================
        SAVITRIBAI PHULE PUNE UNIVERSITY
        Third Year Computer Engineering - Artificial Intelligence Lab
        Assignment No: 1
================================================================================

TITLE:
    Implement Depth First Search (DFS) and Breadth First Search (BFS) Algorithm.
    Use an undirected graph and develop a recursive algorithm for searching all
    the vertices of a graph or tree data structure.

--------------------------------------------------------------------------------
PART 1 - THEORY
--------------------------------------------------------------------------------

1. WHAT IS A GRAPH?
-------------------
A Graph is a non-linear data structure consisting of:
    - Vertices (Nodes): The entities in the graph (e.g., cities, web pages)
    - Edges           : The connections between vertices

Types of Graphs:
    - Undirected Graph : Edges have NO direction. If A connects to B, B connects to A.
    - Directed Graph   : Edges have direction. A->B does NOT mean B->A.

Representation:
    - Adjacency List  : Each node stores a list of its neighbors. (Used here)
    - Adjacency Matrix: 2D matrix where matrix[i][j] = 1 if edge exists.

Example Graph used in this program:
         A
        / \
       B   C
      / \   \
     D   E - F

    Adjacency List:
        A : [B, C]
        B : [A, D, E]
        C : [A, F]
        D : [B]
        E : [B, F]
        F : [C, E]


2. WHAT IS GRAPH TRAVERSAL?
----------------------------
Graph Traversal means visiting every vertex of a graph exactly once in a
systematic manner. Two standard algorithms are:
    a) Depth First Search (DFS)
    b) Breadth First Search (BFS)


3. DEPTH FIRST SEARCH (DFS)
----------------------------
Definition:
    DFS is a graph traversal algorithm that starts at a source node and
    explores as FAR as possible along each branch BEFORE backtracking.

Working:
    - Visit the starting node and mark it as visited.
    - Recursively visit each unvisited neighbor.
    - Backtrack when no unvisited neighbors remain.

Data Structure Used:
    - Stack (Recursion uses the implicit call stack)

Algorithm (Recursive):
    DFS(vertex, visited):
        1. Mark vertex as visited
        2. Print vertex
        3. For each neighbor of vertex:
               If neighbor not visited:
                   Call DFS(neighbor, visited)

Example Trace (Starting from A):
    Visit A -> go to B -> go to D (dead end, backtrack)
            -> go to E -> go to F -> go to C (dead end, backtrack)
    Output: A B D E F C

Time Complexity  : O(V + E)  where V = Vertices, E = Edges
Space Complexity : O(V)      for the visited set and recursion stack

Applications of DFS:
    - Topological Sorting
    - Detecting cycles in a graph
    - Solving maze problems
    - Finding connected components


4. BREADTH FIRST SEARCH (BFS)
------------------------------
Definition:
    BFS is a graph traversal algorithm that starts at a source node and
    explores all NEIGHBORING nodes first, before moving to the next level.

Working:
    - Visit the starting node, mark it visited, add it to a queue.
    - Dequeue a node, visit all its unvisited neighbors.
    - Enqueue each unvisited neighbor.
    - Repeat until queue is empty.

Data Structure Used:
    - Queue (FIFO - First In First Out)

Algorithm (Iterative):
    BFS(start):
        1. Create an empty queue and visited set
        2. Add start to queue and mark as visited
        3. While queue is not empty:
               vertex = dequeue from queue
               Print vertex
               For each neighbor of vertex:
                   If neighbor not visited:
                       Mark as visited
                       Enqueue neighbor

Example Trace (Starting from A):
    Level 0: A
    Level 1: B, C         (neighbors of A)
    Level 2: D, E, F      (neighbors of B and C)
    Output: A B C D E F

Time Complexity  : O(V + E)  where V = Vertices, E = Edges
Space Complexity : O(V)      for the visited set and queue

Applications of BFS:
    - Shortest path in an unweighted graph
    - Level order traversal of a tree
    - Web crawlers
    - Social network friend suggestions (degree of connection)


5. DIFFERENCE BETWEEN DFS AND BFS
------------------------------------

    Feature              DFS                          BFS
    -----------------    -------------------------    -------------------------
    Full Form            Depth First Search           Breadth First Search
    Data Structure       Stack (Recursion)            Queue
    Approach             Go deep first, backtrack     Visit level by level
    Memory Usage         Less (one path at a time)    More (stores all neighbors)
    Shortest Path        Not guaranteed               Guaranteed (unweighted graph)
    Implementation       Recursive / Iterative        Iterative
    Output (example)     A B D E F C                  A B C D E F


6. CONCLUSION
--------------
    - DFS is useful when we want to explore all possible paths (e.g., maze solving).
    - BFS is useful when we want the shortest path (e.g., GPS navigation).
    - Both algorithms have the same time complexity O(V + E) but differ in strategy.
    - The visited set is crucial in undirected graphs to avoid infinite loops.

================================================================================
PART 2 - PROGRAM
================================================================================
"""

# ============================================================
#  Graph represented as an Adjacency List using a dictionary.
#  Each key is a node, and its value is a list of neighbors.
#  This is an UNDIRECTED graph (edges go both ways).
# ============================================================
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

# Graph Structure:
#
#      A
#     / \
#    B   C
#   / \   \
#  D   E - F


# ============================================================
#  RECURSIVE DFS FUNCTION
#  Parameters:
#    graph   - the adjacency list
#    vertex  - current node being visited
#    visited - set of already visited nodes
# ============================================================
def dfs(graph, vertex, visited=None):

    # First call: initialize the visited set (empty)
    if visited is None:
        visited = set()

    # Mark current vertex as visited so we don't visit it again
    visited.add(vertex)

    # Print the current vertex (this is where we "process" the node)
    print(vertex, end=" ")

    # Loop through all neighbors of the current vertex
    for neighbor in graph[vertex]:

        # Only visit the neighbor if it hasn't been visited yet
        if neighbor not in visited:

            # Recursive call: go deeper into the graph
            dfs(graph, neighbor, visited)

    # Return visited set (useful if caller wants to inspect it)
    return visited


# ============================================================
#  ITERATIVE BFS FUNCTION
#  Parameters:
#    graph - the adjacency list
#    start - the starting node
# ============================================================
def bfs(graph, start):

    # Set to keep track of visited nodes (avoid revisiting)
    visited = set()

    # Queue for BFS - initialized with the starting node
    # We use a list as a queue: append() to enqueue, pop(0) to dequeue
    queue = [start]

    # Mark the start node as visited right away
    visited.add(start)

    # Keep going until all reachable nodes are visited
    while queue:

        # Dequeue the first element from the queue (FIFO)
        vertex = queue.pop(0)

        # Print the current vertex
        print(vertex, end=" ")

        # Visit all neighbors of the current vertex
        for neighbor in graph[vertex]:

            # If neighbor hasn't been visited, add it to queue
            if neighbor not in visited:
                visited.add(neighbor)       # Mark as visited
                queue.append(neighbor)      # Enqueue for future processing


# ============================================================
#  MAIN - Entry point of the program
# ============================================================
if __name__ == "__main__":

    # Display the graph structure
    print("=" * 50)
    print("         GRAPH - ADJACENCY LIST")
    print("=" * 50)
    for node, neighbors in graph.items():
        print(f"  {node}  -->  {neighbors}")

    print("\n" + "=" * 50)
    print("   DFS Traversal (Recursive) from node 'A'")
    print("=" * 50)
    print("Visited Order: ", end="")
    dfs(graph, 'A')          # Start DFS from node 'A'

    print("\n\n" + "=" * 50)
    print("   BFS Traversal (Iterative) from node 'A'")
    print("=" * 50)
    print("Visited Order: ", end="")
    bfs(graph, 'A')          # Start BFS from node 'A'
    print("\n")