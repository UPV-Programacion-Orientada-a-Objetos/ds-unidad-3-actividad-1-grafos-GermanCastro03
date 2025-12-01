import sys
import os
import time

# Ensure we can import the extension
sys.path.append(os.getcwd())

# Add MinGW bin to PATH for DLLs
mingw_bin = r"C:\msys64\ucrt64\bin"
if os.path.exists(mingw_bin):
    os.environ['PATH'] = mingw_bin + os.pathsep + os.environ['PATH']


try:
    import neuronet
except ImportError as e:
    print(f"Error importing neuronet: {e}")
    sys.exit(1)

def test_neuronet():
    print("Initializing NeuroNet...")
    g = neuronet.PyGrafo()
    
    data_file = os.path.abspath("data/test_graph.txt")
    print(f"Loading data from {data_file}...")
    g.cargar_datos(data_file)
    
    n = g.get_num_nodos()
    m = g.get_num_aristas()
    print(f"Nodes: {n}, Edges: {m}")
    
    if n != 10:
        print("FAIL: Expected 10 nodes")
    else:
        print("PASS: Node count correct")
        
    # Test BFS
    print("Testing BFS 0 -> 9")
    path = g.bfs(0, 9)
    print(f"Path: {path}")
    
    if len(path) > 0 and path[0] == 0 and path[-1] == 9:
        print("PASS: BFS found path")
    else:
        print("FAIL: BFS failed")

    # Test Degree
    deg0 = g.obtener_grado(0)
    print(f"Degree of 0: {deg0}")
    if deg0 == 2:
        print("PASS: Degree correct")
    else:
        print("FAIL: Degree incorrect")

    # Test Neighbors
    vecinos = g.get_vecinos(0)
    print(f"Neighbors of 0: {vecinos}")
    if sorted(vecinos) == [1, 2]:
        print("PASS: Neighbors correct")
    else:
        print("FAIL: Neighbors incorrect")

if __name__ == "__main__":
    test_neuronet()
