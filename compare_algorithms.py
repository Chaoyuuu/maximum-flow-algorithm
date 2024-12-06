import os
import time
import tracemalloc
from preflow_push_maximum_flow import read_graph_from_file
from ford_fulkerson import ford_fulkerson, read_file
from scaling_ford_fulkerson import max_flow_func

DIR_BASE_PATH = 'GraphGenerator/'

def get_all_file_names(folder_path):
    all_files = os.listdir(folder_path)

    # Filter to include only files (exclude directories)
    file_names = [f for f in os.listdir(folder_path)  # List all files and folders
                  if os.path.isfile(os.path.join(folder_path, f)) and f.endswith('.txt')]
    return file_names

def measure_memory_and_time(algorithm, file_path):
    tracemalloc.start()
    start_time = time.time()
    
    max_flow = algorithm(file_path)
    
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    return max_flow, end_time - start_time, peak

def ford_fulkerson_alg(file_path):
    #read graph
    graph, source, sink = read_file(file_path) 
    
    #basic information about a statistical graph
    num_nodes = len(graph)
    num_edges = sum(len(edges) for edges in graph.values())
    max_capacity = max(
        capacity for edges in graph.values() for capacity in edges.values()
    )
    
    #call ford_fulkerson algorithm
    max_flow = ford_fulkerson(graph, source, sink)
    return max_flow

def scaling_ford_fulkerson_alg(file_path):
    max_flow = max_flow_func(file_path)
    return max_flow

def preflow_push_alg(file_path):
    graph = read_graph_from_file(file_path)

    source = 0
    sink = 1
    max_flow = graph.preflow_push(source, sink)
    return max_flow

# Function to compare three different algorithms
def compare_algorithms():
    
    bipartite_graph = get_all_file_names("./GraphGenerator/Bipartite")
    fixed_degree_graph = get_all_file_names("./GraphGenerator/FixedDegree")
    mesh_graph = get_all_file_names("./GraphGenerator/Mesh")
    random_graph = get_all_file_names("./GraphGenerator/Random")
    
    graph_types = [
        ("Bipartite", bipartite_graph),
        ("FixedDegree", fixed_degree_graph),
        ("Mesh", mesh_graph),
        ("Random", random_graph)
    ]
    
    algorithms = [
        ("Ford-Fulkerson", ford_fulkerson_alg),
        ("Scaling Ford-Fulkerson", scaling_ford_fulkerson_alg),
        ("Preflow-Push", preflow_push_alg),
    ]

    
    for graph_type, generate_graph in graph_types:
        print(f" =====================================")
        print(f" =====> Testing {graph_type} Graph:")
        print(f" =====================================")
        
        for filename in generate_graph:
            print(f"File name: {filename}")
            for algo_name, algorithm in algorithms:
                file_path = DIR_BASE_PATH + graph_type + '/' + filename
                
                max_flow, elapsed_time, peak_mem = measure_memory_and_time(algorithm, file_path)
            
                print(f"  •{algo_name} - Max Flow: {max_flow}")
                print(f"    ◦ Time: {elapsed_time:.4f} seconds")
                print(f"    ◦ Peak Memory: {peak_mem / 1024:.2f} KB")
            print('- - - - - - - - - - - - - - - - - - - - - - -')


if __name__ == "__main__":
    compare_algorithms()
