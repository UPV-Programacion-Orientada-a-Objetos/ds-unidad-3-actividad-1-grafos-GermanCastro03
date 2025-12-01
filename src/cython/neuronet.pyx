# distutils: language = c++

from libcpp.vector cimport vector
from libcpp.string cimport string
from neuronet cimport GrafoDisperso

# Import standard library for string conversion if needed
# But Cython handles python str <-> std::string automatically

cdef class PyGrafo:
    cdef GrafoDisperso* c_grafo  # Hold a pointer to the C++ instance

    def __cinit__(self):
        self.c_grafo = new GrafoDisperso()

    def __dealloc__(self):
        del self.c_grafo

    def cargar_datos(self, archivo: str):
        """Loads graph data from a file."""
        # Encode python string to bytes for std::string conversion
        cdef string c_archivo = archivo.encode('utf-8')
        self.c_grafo.cargarDatos(c_archivo)

    def bfs(self, start_node: int, end_node: int):
        """Runs BFS and returns the path."""
        print(f"[Cython] Solicitud recibida: BFS desde Nodo {start_node}, Profundidad (ignorada/auto).")
        result = self.c_grafo.BFS(start_node, end_node)
        print("[Cython] Retornando lista de adyacencia local a Python.")
        return result

    def bfs_with_depth(self, start_node: int, max_depth: int):
        """Runs BFS with maximum depth and returns all nodes within that depth."""
        print(f"[Cython] Solicitud recibida: BFS con profundidad {max_depth} desde Nodo {start_node}.")
        result = self.c_grafo.BFSWithDepth(start_node, max_depth)
        print("[Cython] Retornando nodos encontrados a Python.")
        return result

    def dfs(self, start_node: int):
        """Runs DFS and returns the traversal order."""
        print(f"[Cython] Solicitud recibida: DFS desde Nodo {start_node}.")
        result = self.c_grafo.DFS(start_node)
        print("[Cython] Retornando orden de recorrido DFS a Python.")
        return result

    def obtener_grado(self, node: int):
        """Returns the degree of a node."""
        return self.c_grafo.obtenerGrado(node)

    def get_vecinos(self, node: int):
        """Returns a list of neighbors for a node."""
        return self.c_grafo.getVecinos(node)

    def get_num_nodos(self):
        return self.c_grafo.getNumNodos()

    def get_num_aristas(self):
        return self.c_grafo.getNumAristas()

    def get_nodo_mas_critico(self):
        return self.c_grafo.getNodoMasCritico()

    def get_memoria_estimada(self):
        return self.c_grafo.getMemoriaEstimada()
    
    def imprimir_estadisticas(self):
        self.c_grafo.imprimirEstadisticas()
