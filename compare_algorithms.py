import os
import time
from preflow_push_maximum_flow import read_graph_from_file
from ford_fulkerson import ford_fulkerson, read_file
from scaling_ford_fulkerson import read_graph, build_capacity_matrix, get_source_and_sink, scaling_ford_fulkerson

DIR_BASE_PATH = 'GraphGenerator/'

def get_all_file_names(folder_path):
    all_files = os.listdir(folder_path)

    # Filter to include only files (exclude directories)
    file_names = [f for f in os.listdir(folder_path)  # List all files and folders
                  if os.path.isfile(os.path.join(folder_path, f)) and f.endswith('.txt')]
    return file_names

def execute_algorithm_and_measure_time(algorithm, file_path):
    max_flow, elapsed_time = algorithm(file_path)
    return max_flow, elapsed_time

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
    start_time = time.time()
    max_flow = ford_fulkerson(graph, source, sink)
    end_time = time.time()
    
    return max_flow, end_time - start_time

def scaling_ford_fulkerson_alg(file_path):
    
    nodes, edges, node_to_index = read_graph(file_path)
    capacity, _ = build_capacity_matrix(nodes, edges)
    source, sink = get_source_and_sink(node_to_index)
    
    start_time = time.time()
    max_flow = scaling_ford_fulkerson(capacity, source, sink)
    end_time = time.time()
    
    return max_flow, end_time - start_time

def preflow_push_alg(file_path):
    graph = read_graph_from_file(file_path)

    source = 0
    sink = 1
    start_time = time.time()
    max_flow = graph.preflow_push(source, sink)
    end_time = time.time()
    return max_flow, end_time - start_time

# Function to compare three different algorithms
def compare_algorithms():
    
    bipartite_graph = get_all_file_names("./GraphGenerator/Bipartite")
    fixed_degree_graph = get_all_file_names("./GraphGenerator/FixedDegree")
    mesh_graph = get_all_file_names("./GraphGenerator/Mesh")
    random_graph = get_all_file_names("./GraphGenerator/Random")
    
    graph_types = [
        # ("Bipartite", bipartite_graph),
        # ("FixedDegree", fixed_degree_graph),
        ("Mesh", mesh_graph),
        # ("Random", random_graph)
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
                
                max_flow, elapsed_time = execute_algorithm_and_measure_time(algorithm, file_path)
            
                print(f"  •{algo_name} - Max Flow: {max_flow}")
                print(f"    ◦ Time: {elapsed_time:.4f} seconds")
            print('- - - - - - - - - - - - - - - - - - - - - - -')


if __name__ == "__main__":
    compare_algorithms()
