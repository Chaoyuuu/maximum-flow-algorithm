import time
from preflow_push_maximum_flow import read_graph_from_file
from ford_fulkerson import ford_fulkerson, read_file
from scaling_ford_fulkerson import max_flow_func

DIR_BASE_PATH = 'GraphGenerator/'

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
    
    bipartite_graph = ['3x4_minC10_maxC_20_prob1.txt', '10x20_minC1_maxC50_prob1.txt']
    fixed_degree_graph = ['10v-3out-4minC-100maxC.txt', '150v-10out-1minC-20maxC.txt']
    mesh_graph = ['3row-5col-1cap-const.txt', '10row-20col-50cap-nonConst.txt']
    random_graph = ['10v-10d-5minC-10maxC.txt', '100v-100d-1minC-50maxC.txt']
    
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
                
                start_time = time.time()
                max_flow = algorithm(file_path)
                end_time = time.time()
                
                print(f"  •{algo_name} - Max Flow: {max_flow}")
                print(f"    ◦ Time: {end_time - start_time:.4f} seconds")
            print('- - - - - - - - - - - - - - - - - - - - - - -')


if __name__ == "__main__":
    compare_algorithms()
