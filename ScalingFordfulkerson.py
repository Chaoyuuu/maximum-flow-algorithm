import sys
from collections import deque, defaultdict

INF = float('inf')

def scaling_ford_fulkerson(capacity, source, sink):
    n = len(capacity)
    residual_capacity = [row[:] for row in capacity]
    max_flow = 0

    max_capacity = max(max(row) for row in capacity)
    delta = 1
    while delta <= max_capacity:
        delta <<= 1
    delta >>= 1

    parent = [-1] * n
    while delta > 0:
        while bfs(residual_capacity, source, sink, parent, delta):
            path_flow = INF
            v = sink
            while v != source:
                u = parent[v]
                path_flow = min(path_flow, residual_capacity[u][v])
                v = u

            v = sink
            while v != source:
                u = parent[v]
                residual_capacity[u][v] -= path_flow
                residual_capacity[v][u] += path_flow
                v = u

            max_flow += path_flow
        delta >>= 1

    return max_flow

def bfs(residual_capacity, source, sink, parent, delta):
    n = len(residual_capacity)
    visited = [False] * n
    queue = deque([source])
    visited[source] = True
    parent[source] = -1

    while queue:
        u = queue.popleft()
        for v in range(n):
            if not visited[v] and residual_capacity[u][v] >= delta:
                queue.append(v)
                visited[v] = True
                parent[v] = u
                if v == sink:
                    return True
    return False

def main():
    print("Algorithm: Scaling Ford-Fulkerson")
    input_file = input("Enter the input file name: ")

    print("Select mode:")
    print("1 - Mesh")
    print("2 - FixedDegree")
    print("3 - Bipartite")
    print("4 - Random")
    mode = int(input("Enter mode (1-4): "))
    if mode < 1 or mode > 4:
        print("Invalid mode selected. Please enter a number between 1 and 4.")
        return

    node_to_index = {}
    nodes = []
    edges = []
    max_capacity = 0
    min_capacity = INF

    with open(input_file, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) != 3:
                raise ValueError(f"Invalid line format: {line}")

            source, target, capacity = parts[0], parts[1], int(parts[2])
            if source not in node_to_index:
                node_to_index[source] = len(nodes)
                nodes.append(source)
            if target not in node_to_index:
                node_to_index[target] = len(nodes)
                nodes.append(target)

            u, v = node_to_index[source], node_to_index[target]
            edges.append((u, v, capacity))
            max_capacity = max(max_capacity, capacity)
            min_capacity = min(min_capacity, capacity)

    n = len(nodes)
    capacity = [[0] * n for _ in range(n)]
    out_degree = [0] * n
    for u, v, cap in edges:
        capacity[u][v] = cap
        out_degree[u] += 1

    if 's' not in node_to_index or 't' not in node_to_index:
        raise ValueError("Graph must contain source ('s') and sink ('t') nodes.")

    source, sink = node_to_index['s'], node_to_index['t']
    max_flow = scaling_ford_fulkerson(capacity, source, sink)

    if mode == 1:  # Basic max-flow calculation
        print("Max flow:", max_flow)
    elif mode == 2:  # Extended graph info
        avg_out_degree = sum(out_degree) // n
        print("Graph Info:")
        print(f"{n}v-{avg_out_degree}out-{min_capacity}min-{max_capacity}max")
        print(f"\t{n} vertices")
        print(f"\t{avg_out_degree} edges out of each node")
        print(f"\tCapacities range from {min_capacity} to {max_capacity}")
        print(f"\tMax flow: {max_flow}")
    elif mode == 3:  # Bipartite graph info
        print("The graph is a bipartite graph with:")
        print("m =", len(edges))
        print("n =", len(nodes))
        print("Max flow =", max_flow)
    elif mode == 4:  # Random graph density
        density = len(edges) / (n * (n - 1)) * 100
        print("Random graph")
        print(input_file)
        print(f"{(density // 10) * 10}% dense")
        print("Max flow:", max_flow)
    else:
        print("Invalid mode selected.")

if __name__ == "__main__":
    main()
