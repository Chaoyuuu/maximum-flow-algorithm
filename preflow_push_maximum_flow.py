import sys
from collections import defaultdict, deque


class Graph:
    def __init__(self, vertices):
        self.vertices = vertices
        self.graph = defaultdict(lambda: defaultdict(int))

    def add_edge(self, u, v, capacity):
        self.graph[u][v] += capacity  # Add capacity to the edge
        self.graph[v][u] += 0  # Reverse edge initially has 0 capacity

    def preflow_push(self, source, sink):
        # Initialize structures
        excess = [0] * self.vertices
        height = [0] * self.vertices
        flow = defaultdict(lambda: defaultdict(int))
        height[source] = self.vertices  # Height of source is the number of vertices

        # Preflow initialization
        for v in self.graph[source]:
            flow[source][v] = self.graph[source][v]
            flow[v][source] = -flow[source][v]
            excess[v] = self.graph[source][v]
            excess[source] -= self.graph[source][v]

        # Active nodes (those with excess > 0)
        active = deque([v for v in range(self.vertices) if v != source and v != sink and excess[v] > 0])

        # Push and Relabel operations
        def push(u, v):
            delta = min(excess[u], self.graph[u][v] - flow[u][v])
            flow[u][v] += delta
            flow[v][u] -= delta
            excess[u] -= delta
            excess[v] += delta

        def relabel(u):
            min_height = float('inf')
            for v in self.graph[u]:
                if self.graph[u][v] - flow[u][v] > 0:
                    min_height = min(min_height, height[v])
            height[u] = min_height + 1

        while active:
            u = active.popleft()
            while excess[u] > 0:
                for v in self.graph[u]:
                    if self.graph[u][v] - flow[u][v] > 0 and height[u] == height[v] + 1:
                        push(u, v)
                        if v != source and v != sink and excess[v] > 0 and v not in active:
                            active.append(v)
                        break
                else:
                    relabel(u)
                    break
            if excess[u] > 0 and u not in active:
                active.append(u)

        # Calculate maximum flow
        return sum(flow[source][v] for v in self.graph[source])


def node_converter(node):
    if node == 's':
        return 0
    elif node == 't':
        return 1
    else:
        return int(node[1:]) + 1


def read_graph_from_file(filename):
    g = Graph(0)
    line_cnt = 0
    with open(filename, 'r') as file:
        for line in file:
            line_cnt += 1
            parts = line.strip().split()
            if len(parts) != 3:
                print(f"Skipping invalid line: {line}")
                continue

            node1, node2, cap = parts
            g.add_edge(node_converter(node1), node_converter(node2), int(cap))

    g.vertices = line_cnt
    return g

if __name__ == "__main__":
    filename = sys.argv[1] # e.g. 'FixedDegree/100v-5out-25min-200max.txt'
    graph = read_graph_from_file(filename)
    print("Graph Representation:")

    source = 0
    sink = 1
    print(f"The maximum possible flow is {graph.preflow_push(source, sink)}")
