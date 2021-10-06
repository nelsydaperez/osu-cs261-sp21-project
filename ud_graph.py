# Course: CS261 - Data Structures
# Author: Nelsyda Perez
# Assignment: 6 - Graph Implementation
# Description: Implementation of an undirected graph ADT

import heapq
from collections import deque


class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        Add new vertex to the graph
        """
        if v in self.adj_list:
            return
        else:
            self.adj_list[v] = []
        
    def add_edge(self, u: str, v: str) -> None:
        """
        Add edge to the graph
        """
        # Does nothing if vertices are equal
        if u == v:
            return

        # Adds vertex u if it does not not exist
        if u not in self.adj_list:
            self.adj_list[u] = [v]

        # Adds v to adjacent vertices list for vertex u if it does not exist already
        elif v not in self.adj_list[u]:
            self.adj_list[u].append(v)

        # Adds vertex v if it does not not exist
        if v not in self.adj_list:
            self.adj_list[v] = [u]

        # Adds u to adjacent vertices list for vertex v if it does not exist already
        elif u not in self.adj_list[v]:
            self.adj_list[v].append(u)

    def remove_edge(self, v: str, u: str) -> None:
        """
        Remove edge from the graph
        """
        # Does nothing if the vertices do not exist
        if v not in self.adj_list or u not in self.adj_list:
            return

        # Removes edge (adjacent vertices from their respective lists) if the edge exists
        if u in self.adj_list[v] and v in self.adj_list[u]:
            self.adj_list[v].remove(u)
            self.adj_list[u].remove(v)

    def remove_vertex(self, v: str) -> None:
        """
        Remove vertex and all connected edges
        """
        if v not in self.adj_list:
            return
        del self.adj_list[v]
        for vertex in self.adj_list:
            if v in self.adj_list[vertex]:
                self.adj_list[vertex].remove(v)

    def get_vertices(self) -> []:
        """
        Return list of vertices in the graph (any order)
        """
        list_of_vertices = []
        for vertex in self.adj_list:
            list_of_vertices.append(vertex)
        return list_of_vertices

    def get_edges(self) -> []:
        """
        Return list of edges in the graph (any order)
        """
        list_of_edges = []
        previous = []
        for vertex in self.adj_list:
            for adjacent in self.adj_list[vertex]:
                if adjacent not in previous:
                    list_of_edges.append((vertex, adjacent))
            previous.append(vertex)
        return list_of_edges

    def is_valid_path(self, path: []) -> bool:
        """
        Return True if provided path is valid, False otherwise
        """
        # Checks for empty list as path
        if not path:
            return True

        # Checks if first vertex of path exists
        if path[0] not in self.adj_list:
            return False

        # Iterates through path and checks for edges. Returns False if current edge checked is invalid.
        index = 0
        while index + 1 != len(path):
            if path[index + 1] not in self.adj_list[path[index]]:
                return False
            index += 1
        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during DFS search
        Vertices are picked in alphabetical order
        """
        if v_start not in self.adj_list:
            return []
        if v_end is not None and v_end not in self.adj_list:
            v_end = None
        stack = deque()
        stack.append(v_start)
        visited = []
        successors = []
        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                visited.append(vertex)
                if vertex is v_end:
                    return visited
                temp = self.adj_list[vertex].copy()
                heapq.heapify(temp)
                while temp:
                    successors.append(heapq.heappop(temp))
                while successors:
                    stack.append(successors.pop())
        return visited

    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search
        Vertices are picked in alphabetical order
        """
        if v_start not in self.adj_list:
            return []
        if v_end is not None and v_end not in self.adj_list:
            v_end = None
        stack = deque()
        stack.append(v_start)
        visited = []
        while stack:
            vertex = stack.popleft()
            if vertex not in visited:
                visited.append(vertex)
                if vertex is v_end:
                    return visited
                successors = self.adj_list[vertex].copy()
                heapq.heapify(successors)
                while successors:
                    if successors[0] not in visited:
                        stack.append(heapq.heappop(successors))
                    else:
                        heapq.heappop(successors)
        return visited

    def count_connected_components(self):
        """
        Return number of connected components in the graph
        """
        list_of_vertices = self.get_vertices()
        count = 0
        while list_of_vertices:
            count += 1
            path = self.dfs(list_of_vertices[0])
            for vertex in path:
                list_of_vertices.remove(vertex)
        return count

    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
        """
        visited = []

        # Checks every DPS path by setting all vertices as the starting vertices for each possible DPS.
        for vertex in self.adj_list:
            # Checks if the vertex has been fully analyzed prior to the recursive call
            if vertex not in visited:
                if self._has_cycle_rec(vertex, visited):
                    return True
                
        return False  # All possible DPS paths have been analyzed and no cycle has been found

    def _has_cycle_rec(self, vertex, visited, previous=None):
        """
        Recursive helper function for has_cycle.
        """
        visited.append(vertex)  # keeps track of all vertices that have been fully explored (all edges analyzed)

        # Recursive call for all adjacent nodes made
        for adjacent in self.adj_list[vertex]:
            if adjacent not in visited:
                if self._has_cycle_rec(adjacent, visited, vertex):  # Recursion occurs if adj. vertex is not visited
                    return True

            # Checks if the visited vertex is connected to the current vertex. Note that for a cycle to occur, backwards
            # movement along the same edge is not allowed.
            elif previous != adjacent:
                return True
        return False


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = UndirectedGraph()
    print(g)

    for v in 'ABCDE':
        g.add_vertex(v)
    print(g)

    g.add_vertex('A')
    print(g)

    for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
        g.add_edge(u, v)
    print(g)

    print("\nPDF - method remove_edge() / remove_vertex example 1")
    print("----------------------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    g.remove_vertex('DOES NOT EXIST')
    g.remove_edge('A', 'B')
    g.remove_edge('X', 'B')
    print(g)
    g.remove_vertex('D')
    print(g)

    print("\nPDF - method get_vertices() / get_edges() example 1")
    print("---------------------------------------------------")
    g = UndirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    print(g.get_edges(), g.get_vertices(), sep='\n')

    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    for path in test_cases:
        print(list(path), g.is_valid_path(list(path)))

    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = 'ABCDEGH'
    for case in test_cases:
        print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    print('-----')
    for i in range(1, len(test_cases)):
        v1, v2 = test_cases[i], test_cases[-1 - i]
        print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')

    print("\nPDF - method count_connected_components() example 1")
    print("---------------------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print(g.count_connected_components(), end=' ')
    print()

    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
        'add FG', 'remove GE')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print('{:<10}'.format(case), g.has_cycle())
