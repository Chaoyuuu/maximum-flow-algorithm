from collections import defaultdict, deque
import time

#parse the input file and generates an adjacency list
def read_file(filename):
    graph = defaultdict(lambda: defaultdict(int)) #the adjacency list stores the graph, default capacity is 0
    source, sink = "s", "t"  #point s and t
    while True:  #loop until input right filename
        try: #open and read file
            with open(filename, 'r') as file:
                for line in file:
                    u, v, capacity = line.split()
                    graph[u][v] += int(capacity)
            break #Successfully read file than break
        except FileNotFoundError: #not found file
            print(f"Error: File '{filename}' not found. Please try again.")
            filename = input("Please enter the file name (e.g., g1.txt): ").strip()
        except ValueError: #wrong file format
            print("Error: Invalid file format. Please try again.")
            filename = input("Please enter the file name (e.g., g1.txt): ").strip()
    return graph, source, sink #Returns the adjacency list, source point, and junction point

#find an augmentation path using BFS
def bfs(residual_graph, source, sink, parent):
    visited = set() #record the accessed nodes
    queue = deque([source]) #initialize queue and add source point
    visited.add(source) #source point is visited
    while queue: #loop until the queue is empty
        u = queue.popleft() #pop up the first node
        for v, capacity in residual_graph[u].items(): #traverse all adjacent nodes of the current node
            if v not in visited and capacity > 0: #if the node is not accessed and capacity > 0
                queue.append(v) #add node to the queue
                visited.add(v) #mark node as accessed
                parent[v] = u #record parent node
                if v == sink:
                    return True #return successfully found the augmentation path
    return False #not found augmentation path

#ford-fulkerson algorithm
def ford_fulkerson(graph, source, sink):
    residual_graph = defaultdict(lambda: defaultdict(int)) #initialize the residual network
    for u in graph: #traverse every node
        for v, capacity in graph[u].items(): #traverse every edge
            residual_graph[u][v] = capacity #initial capacity = capacity of the input graph
    parent = {} #store augmentation path
    max_flow = 0

    #find augmentation path until can not find
    while bfs(residual_graph, source, sink, parent):
        #find the minimum residual capacity of the augmented path
        path_flow = float('Inf') #initial path flow = infinity
        s = sink #retrace the path from the junction
        while s != source: #back to source point
            path_flow = min(path_flow, residual_graph[parent[s]][s]) #update minimum flow
            s = parent[s]

        #renewal residual network
        v = sink
        while v != source: #back to source point
            u = parent[v] #get parent node
            residual_graph[u][v] -= path_flow #reduce the capacity of the forward edge
            residual_graph[v][u] += path_flow #increase the capacity of the reverse edge
            v = parent[v]
        max_flow += path_flow
    return max_flow

#main program: dynamically reads the file name and calculates the maximum flow
if __name__ == "__main__":
    filename = input("Please enter the file name (e.g., g1.txt): ").strip() #user input filename
    
    graph, source, sink = read_file(filename) #read graph and run Ford-Fulkerson algorithm

    #basic information about a statistical graph
    num_nodes = len(graph)
    num_edges = sum(len(edges) for edges in graph.values())
    max_capacity = max(
        capacity for edges in graph.values() for capacity in edges.values()
    )

    start_time = time.time() #start timing
    
    #call ford_fulkerson algorithm
    max_flow = ford_fulkerson(graph, source, sink)
    
    end_time = time.time() #end timing

    #output
    print(f"m={num_nodes}")
    print(f"n={num_edges}")
    print(f"probability=1")
    print(f"capacity={max_capacity}")
    print(f"\nMax flow = {max_flow}")
    print(f"\nTime taken: {end_time - start_time:.4f} seconds") #output run time
