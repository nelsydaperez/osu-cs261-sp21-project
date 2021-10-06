# Course: CS261 - Data Structures
# Author: Nelsyda Perez
# Assignment: 6 - Graph Implementation
# Description: Implementation of a directed graph ADT

import heapq
from collections import deque


class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        Add new vertex to the graph. Returns the number of vertices in the graph.
        """
        self.v_count += 1
        self.adj_matrix.append([0] * self.v_count)
        for i in range(0, self.v_count - 1):
            self.adj_matrix[i].append(0)
        return self.v_count

    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        Add one-way edge to the graph ( src --> dst ).
        """
        if src < 0 or src >= self.v_count:
            return

        if dst < 0 or dst >= self.v_count:
            return

        if src == dst:
            return

        self.adj_matrix[src][dst] = weight

    def remove_edge(self, src: int, dst: int) -> None:
        """
        Remove one-way edge from the graph ( src --> dst ).
        """
        if src < 0 or src >= self.v_count:
            return

        if dst < 0 or dst >= self.v_count:
            return

        if src == dst:
            return

        if self.adj_matrix[src][dst] != 0:
            self.adj_matrix[src][dst] = 0

    def get_vertices(self) -> []:
        """
        Return list of vertices in the graph (any order).
        """
        return list(range(0, self.v_count))

    def get_edges(self) -> []:
        """
        Return list of edges in the graph (any order).
        """
        list_of_edges = []
        for i in range(0, self.v_count):
            for j in range(0, self.v_count):
                if self.adj_matrix[i][j] != 0:
                    list_of_edges.append((i, j, self.adj_matrix[i][j]))
        return list_of_edges

    def is_valid_path(self, path: []) -> bool:
        """
        Return True if provided path is valid, False otherwise.
        """
        # Checks for empty list as path
        if not path:
            return True

        # Iterates through path and checks for edges. Returns False if current edge checked is invalid.
        index = 0
        while index + 1 != len(path):
            if self.adj_matrix[path[index]][path[index + 1]] == 0:
                return False
            index += 1
        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during DFS search.
        Vertices are picked in ascending order.
        """
        if v_start < 0 or v_start >= self.v_count:
            return []
        if v_end is not None and (v_end < 0 or v_end >= self.v_count):
            v_end = None
        stack = deque()
        stack.append(v_start)
        visited = []
        while stack:
            i = stack.pop()
            if i not in visited:
                visited.append(i)
                if i is v_end:
                    return visited
                for j in range(self.v_count - 1, -1, -1):
                    if self.adj_matrix[i][j] != 0:
                        stack.append(j)
        return visited

    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search.
        Vertices are picked in ascending order.
        """
        if v_start < 0 or v_start >= self.v_count:
            return []
        if v_end is not None and (v_end < 0 or v_end >= self.v_count):
            v_end = None
        stack = deque()
        stack.append(v_start)
        visited = []
        while stack:
            i = stack.popleft()
            if i not in visited:
                visited.append(i)
                if i is v_end:
                    return visited
                for j in range(0, self.v_count):
                    if j not in visited and self.adj_matrix[i][j] != 0:
                        stack.append(j)
        return visited

    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
        """

        # Cycles can only possible if there are 2 or more vertices
        if self.v_count < 2:
            return False

        visited = []
        path = []

        # Checks every DPS path by setting all vertices as the starting vertices for each possible DPS.
        for vertex in range(0, self.v_count):

            # Checks if the vertex has been fully analyzed prior to the recursive call
            if vertex not in visited:
                if self._has_cycle_rec(vertex, visited, path):
                    return True

        return False  # All possible DPS paths have been analyzed and no cycle has been found

    def _has_cycle_rec(self, vertex, visited, path):
        """
        Recursive helper function for has_cycle.
        """
        visited.append(vertex)    # keeps track of all vertices that have been fully explored (all edges analyzed)
        path.append(vertex)  # keeps track of vertices in a single DPS path

        # Recursive call for all adjacent vertices made
        for i in range(0, self.v_count):

            # Checks if vertex is adjacent to current vertex being checked prior to entering
            if self.adj_matrix[vertex][i] != 0:
                if i not in visited:
                    if self._has_cycle_rec(i, visited, path):  # Recursion occurs if adj. vertex is not visited
                        return True
                elif i in path:
                    return True       # A cycle is found when the vertex i is both visited and on the current path

        # Remove vertex from stack after all adjacent nodes have been analyzed
        path.remove(vertex)
        return False

    def dijkstra(self, src: int) -> []:
        """
        Returns a list whose elements are the length of the shortest path between the src and the vertices corresponding
        to the indices of the list.
        """
        # Checks if src vertex exists
        if src < 0 or src >= self.v_count:
            return

        distance = [float('inf')] * self.v_count  # Initialize all to infinity
        distance[src] = 0  # Initialize the source distance as 0
        priority = []  # represented as a min heap
        visited = []
        heapq.heappush(priority, [distance[src], src])  # add source vertex to priority queue

        while priority:
            vertex = heapq.heappop(priority)[1]  # gets vertex with smallest distance
            if vertex not in visited:
                visited.append(vertex)
                for i in range(0, self.v_count):
                    if self.adj_matrix[vertex][i] != 0:
                        # Update adj. vertex's current minimum distance value and add adj. vertex to the priority queue
                        distance[i] = min(distance[i], distance[vertex] + self.adj_matrix[vertex][i])
                        heapq.heappush(priority, [distance[i], i])
        return distance


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = DirectedGraph()
    print(g)
    for _ in range(5):
        g.add_vertex()
    print(g)

    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    for src, dst, weight in edges:
        g.add_edge(src, dst, weight)
    print(g)


    print("\nPDF - method get_edges() example 1")
    print("----------------------------------")
    g = DirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    for path in test_cases:
        print(path, g.is_valid_path(path))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for start in range(5):
        print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)

    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
        g.remove_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')

    edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    for src, dst in edges_to_add:
        g.add_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    print('\n', g)


    print("\nPDF - dijkstra() example 1")
    print("--------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
