from libcpp.vector cimport vector
from libcpp.string cimport string

cdef extern from "../cpp/GrafoBase.h":
    cdef cppclass GrafoBase:
        pass

cdef extern from "../cpp/GrafoDisperso.h":
    cdef cppclass GrafoDisperso(GrafoBase):
        GrafoDisperso() except +
        void cargarDatos(string archivo)
        vector[int] BFS(int nodoInicio, int nodoDestino)
        vector[int] BFSWithDepth(int nodoInicio, int profundidadMax)
        vector[int] DFS(int nodoInicio)
        int obtenerGrado(int nodo)
        vector[int] getVecinos(int nodo)
        int getNumNodos()
        int getNumAristas()
        int getNodoMasCritico()
        long long getMemoriaEstimada()
        void imprimirEstadisticas()
