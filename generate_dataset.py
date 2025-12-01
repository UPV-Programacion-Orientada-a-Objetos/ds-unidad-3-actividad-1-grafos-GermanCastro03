import networkx as nx
import os

def generate_snap_dataset(filename, nodes=1000, edges_per_node=5):
    print(f"Generating graph with {nodes} nodes...")
    # Barabasi-Albert graph mimics real social/web networks (scale-free)
    G = nx.barabasi_albert_graph(nodes, edges_per_node)
    
    print(f"Saving to {filename}...")
    with open(filename, 'w') as f:
        f.write(f"# Synthetic SNAP Dataset\n")
        f.write(f"# Nodes: {nodes} Edges: {G.number_of_edges()}\n")
        f.write(f"# FromNodeId\tToNodeId\n")
        for u, v in G.edges():
            f.write(f"{u}\t{v}\n")
            # Make it directed by adding reverse if needed, 
            # but SNAP files are often just edge lists. 
            # Our C++ treats it as directed edges from file.
            # If we want undirected behavior in a directed loader, we usually list both.
            # But for this test, let's keep it simple.
            
    print("Done.")

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    # Generate 1 Million nodes
    generate_snap_dataset("data/large_snap.txt", nodes=1000000, edges_per_node=3)
