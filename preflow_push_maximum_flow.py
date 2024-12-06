import sys
from collections import defaultdict, deque
import time


class Graph:
    """
    Represents a directed graph using an adjacency list.

    Attributes:
        vertices (set): A set of unique vertices in the graph.
        graph (defaultdict): A nested dictionary representing edges and their capacities.
    """

    def __init__(self):
        """
            Initializes an empty graph with no vertices or edges.
        """
        self.vertices = set()  # Stores all vertices in the graph
        self.graph = defaultdict(lambda: defaultdict(int))  # Adjacency list for storing capacities

    def add_edge(self, u, v, capacity):
        """
        Adds an edge to the graph with a specified capacity.

        Args:
            u (int): The starting vertex of the edge.
            v (int): The ending vertex of the edge.
            capacity (int): The capacity of the edge.
        """
        self.graph[u][v] += capacity  # Update the forward edge capacity
        self.graph[v][u] += 0  # Initialize reverse edge with 0 capacity
        self.vertices.add(u)
        self.vertices.add(v)

    def preflow_push(self, source, sink):
        """
        Implements the Preflow-Push algorithm to compute the maximum flow in the graph.

        Args:
            source (int): The source vertex.
            sink (int): The sink vertex.

        Returns:
            int: The maximum flow from source to sink.
        """

        # Initialize structures for the algorithm
        vertex_count = max(self.vertices) + 1
        excess = [0] * vertex_count  # Excess flow for each vertex
        height = [0] * vertex_count  # Height of each vertex
        flow = defaultdict(lambda: defaultdict(int))  # Tracks flow along each edge
        height[source] = vertex_count  # Set height of the source to the number of vertices

        # Preflow: Push initial flow from the source to its neighbors
        for v in self.graph[source]:
            flow[source][v] = self.graph[source][v]
            flow[v][source] = -flow[source][v]
            excess[v] = self.graph[source][v]
            excess[source] -= self.graph[source][v]

        # Active nodes (those with excess > 0)
        active = deque([v for v in range(vertex_count) if v != source and v != sink and excess[v] > 0])

        # Push operation: Push flow from node u to node v
        def push(u, v):
            """
            Push flow from vertex u to vertex v.

            Args:
                u (int): The source vertex of the flow.
                v (int): The destination vertex of the flow.
            """
            delta = min(excess[u], self.graph[u][v] - flow[u][v])
            flow[u][v] += delta
            flow[v][u] -= delta
            excess[u] -= delta
            excess[v] += delta

        # Relabel operation: Increase the height of a vertex
        def relabel(u):
            """
            Relabel the height of a vertex to enable flow push.

            Args:
                u (int): The vertex to relabel.
            """
            min_height = float('inf')
            for v in self.graph[u]:
                if self.graph[u][v] - flow[u][v] > 0:  # Check for residual capacity
                    min_height = min(min_height, height[v])
            height[u] = min_height + 1

        # Process active nodes
        while active:
            u = active.popleft()
            while excess[u] > 0:
                for v in self.graph[u]:
                    if self.graph[u][v] - flow[u][v] > 0 and height[u] == height[v] + 1:
                        push(u, v)
                        if v != source and v != sink and excess[v] > 0 and v not in active:
                            active.append(v)  # Add v to active queue if newly active
                        break
                else:
                    relabel(u)  # Relabel if no push occurred
                    break
            if excess[u] > 0 and u not in active:
                active.append(u)  # Re-add u to active queue if still active

        # Calculate maximum flow as the sum of flows leaving the source
        return sum(flow[source][v] for v in self.graph[source])


def node_converter(node):
    """
    Converts node identifiers to integer indices.

    Args:
        node (str): The node identifier (e.g., 's', 't', or 'v1').

    Returns:
        int: The corresponding integer index for the node.
    """
    if node == 's':
        return 0  # Source node
    elif node == 't':
        return 1  # Sink node
    else:
        return int(node[1:]) + 1  # Convert numeric part of node label to index


def read_graph_from_file(filename):
    """
    Reads a graph from a file and constructs a Graph object.

    Args:
        filename (str): The name of the file containing the graph data.

    Returns:
        Graph: The constructed Graph object.
    """
    g = Graph()
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) != 3:
                print(f"Skipping invalid line: {line}")
                continue

            node1, node2, cap = parts
            g.add_edge(node_converter(node1), node_converter(node2), int(cap))
    return g


if __name__ == "__main__":
    filename = sys.argv[1]  # e.g. 'GraphGenerator/FixedDegree/100v-5out-25min-200max.txt'
    graph = read_graph_from_file(filename)

    source = 0
    sink = 1
    start_time = time.time()
    max_flow = graph.preflow_push(source, sink)
    end_time = time.time()
    print(f"The maximum possible flow is {max_flow}.")
    print(f"The execution time is {end_time - start_time: .2f} seconds.")
