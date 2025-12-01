import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import time
import os
import sys

# Ensure we can import the extension
sys.path.append(os.getcwd())

# Add MinGW bin to PATH for DLLs
mingw_bin = r"C:\msys64\ucrt64\bin"
if os.path.exists(mingw_bin):
    os.environ['PATH'] = mingw_bin + os.pathsep + os.environ['PATH']


try:
    import neuronet
except ImportError as e:
    messagebox.showerror("Error", f"Could not import neuronet extension: {e}")
    sys.exit(1)

class NeuroNetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NeuroNet - Massive Graph Analysis")
        self.root.geometry("1200x800")

        self.graph_system = neuronet.PyGrafo()
        self.loaded = False

        self._setup_ui()

    def _setup_ui(self):
        # Top Control Panel
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(side=tk.TOP, fill=tk.X)

        ttk.Button(control_frame, text="Load Dataset (SNAP)", command=self.load_dataset).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(control_frame, text="Start Node:").pack(side=tk.LEFT, padx=5)
        self.start_node_var = tk.StringVar()
        ttk.Entry(control_frame, textvariable=self.start_node_var, width=10).pack(side=tk.LEFT)

        ttk.Label(control_frame, text="End Node:").pack(side=tk.LEFT, padx=5)
        self.end_node_var = tk.StringVar()
        ttk.Entry(control_frame, textvariable=self.end_node_var, width=10).pack(side=tk.LEFT)

        ttk.Label(control_frame, text="Depth:").pack(side=tk.LEFT, padx=5)
        self.depth_var = tk.StringVar(value="2")
        ttk.Entry(control_frame, textvariable=self.depth_var, width=5).pack(side=tk.LEFT)

        ttk.Button(control_frame, text="Run BFS", command=self.run_bfs).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Run DFS", command=self.run_dfs).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Visualize Neighborhood", command=self.visualize_neighborhood).pack(side=tk.LEFT, padx=5)

        # Metrics Panel
        metrics_frame = ttk.LabelFrame(self.root, text="Metrics", padding="10")
        metrics_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        
        self.lbl_nodes = ttk.Label(metrics_frame, text="Nodes: 0")
        self.lbl_nodes.pack(side=tk.LEFT, padx=10)
        
        self.lbl_edges = ttk.Label(metrics_frame, text="Edges: 0")
        self.lbl_edges.pack(side=tk.LEFT, padx=10)
        
        self.lbl_max_degree = ttk.Label(metrics_frame, text="Max Degree Node: N/A")
        self.lbl_max_degree.pack(side=tk.LEFT, padx=10)
        
        self.lbl_memory = ttk.Label(metrics_frame, text="Est. Memory: 0 MB")
        self.lbl_memory.pack(side=tk.LEFT, padx=10)

        # Main Content Area (Split: Log vs Visualization)
        paned_window = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left: Log/Stats
        self.log_text = tk.Text(paned_window, width=40, height=20)
        paned_window.add(self.log_text)

        # Right: Visualization
        self.viz_frame = ttk.Frame(paned_window)
        paned_window.add(self.viz_frame)
        
        self.figure, self.ax = plt.subplots(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.viz_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def log(self, message):
        self.log_text.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {message}\n")
        self.log_text.see(tk.END)

    def load_dataset(self):
        file_path = filedialog.askopenfilename(title="Select Edge List", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if not file_path:
            return

        self.log(f"Loading dataset: {file_path}...")
        self.root.update()
        
        start_time = time.time()
        try:
            self.graph_system.cargar_datos(file_path)
            elapsed = time.time() - start_time
            
            num_nodes = self.graph_system.get_num_nodos()
            num_edges = self.graph_system.get_num_aristas()
            
            self.log(f"Load Complete in {elapsed:.4f}s")
            self.log(f"Nodes: {num_nodes}, Edges: {num_edges}")
            
            # Update Metrics
            max_crit = self.graph_system.get_nodo_mas_critico()
            max_degree = self.graph_system.obtener_grado(max_crit)
            mem_bytes = self.graph_system.get_memoria_estimada()
            mem_mb = mem_bytes / (1024 * 1024)
            
            self.lbl_nodes.config(text=f"Nodes: {num_nodes}")
            self.lbl_edges.config(text=f"Edges: {num_edges}")
            self.lbl_max_degree.config(text=f"Max Degree Node: {max_crit} (Deg: {max_degree})")
            self.lbl_memory.config(text=f"Est. Memory: {mem_mb:.2f} MB")
            
            self.loaded = True
            
            # Capture C++ stdout stats if possible, or just rely on python getters
            # self.graph_system.imprimir_estadisticas() # Prints to console
            
        except Exception as e:
            self.log(f"Error loading data: {e}")

    def run_bfs(self):
        if not self.loaded:
            messagebox.showwarning("Warning", "Load a dataset first.")
            return
            
        try:
            start = int(self.start_node_var.get())
            end = int(self.end_node_var.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid node IDs")
            return

        self.log(f"Running BFS from {start} to {end}...")
        self.root.update()
        
        t0 = time.time()
        path = self.graph_system.bfs(start, end)
        dt = time.time() - t0
        
        if not path:
            self.log(f"BFS Finished in {dt:.6f}s. No path found.")
        else:
            self.log(f"BFS Finished in {dt:.6f}s. Distance: {len(path)-1}")
            self.log(f"Path: {path[:10]}... (showing first 10)")

    def run_dfs(self):
        if not self.loaded:
            messagebox.showwarning("Warning", "Load a dataset first.")
            return
            
        try:
            start = int(self.start_node_var.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid start node ID")
            return

        self.log(f"Running DFS from {start}...")
        self.root.update()
        
        t0 = time.time()
        traversal = self.graph_system.dfs(start)
        dt = time.time() - t0
        
        if not traversal:
            self.log(f"DFS Finished in {dt:.6f}s. No nodes found.")
        else:
            self.log(f"DFS Finished in {dt:.6f}s. Visited {len(traversal)} nodes.")
            self.log(f"Traversal: {traversal[:20]}... (showing first 20)")

    def visualize_neighborhood(self):
        if not self.loaded:
            return
            
        try:
            center_node = int(self.start_node_var.get())
            depth = int(self.depth_var.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid Start Node or Depth")
            return

        self.log(f"Visualizing neighborhood of {center_node} with depth {depth}...")
        
        # Use BFS with depth to get all nodes within specified depth
        nodes_in_depth = self.graph_system.bfs_with_depth(center_node, depth)
        
        self.log(f"Found {len(nodes_in_depth)} nodes within depth {depth}")
        
        # Limit visualization to avoid crash
        if len(nodes_in_depth) > 150:
            self.log("Neighborhood too large to visualize all. Showing first 100.")
            nodes_in_depth = nodes_in_depth[:100]

        # Build NetworkX graph for visualization only
        G = nx.DiGraph()  # Use directed graph
        G.add_nodes_from(nodes_in_depth)
        
        # Add edges between nodes in the subgraph
        for node in nodes_in_depth:
            neighbors = self.graph_system.get_vecinos(node)
            for neighbor in neighbors:
                if neighbor in nodes_in_depth:
                    G.add_edge(node, neighbor)
            
        # Draw with color-coded depth levels
        self.ax.clear()
        pos = nx.spring_layout(G, k=0.5, iterations=50)
        
        # Color nodes by their distance from center
        node_colors = []
        for node in G.nodes():
            if node == center_node:
                node_colors.append('red')
            else:
                # Approximate depth by BFS distance
                node_colors.append('lightblue')
        
        nx.draw(G, pos, ax=self.ax, with_labels=True, node_color=node_colors, 
                edge_color='gray', node_size=300, font_size=8, arrows=True, 
                arrowsize=10, alpha=0.8)
        nx.draw_networkx_nodes(G, pos, nodelist=[center_node], node_color='red', 
                              node_size=500, ax=self.ax)
        
        self.ax.set_title(f"Neighborhood of Node {center_node} (Depth {depth})")
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = NeuroNetApp(root)
    root.mainloop()
