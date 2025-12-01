#ifndef GRAFOBASE_H
#define GRAFOBASE_H

#include <string>
#include <vector>

class GrafoBase {
public:
  virtual ~GrafoBase() {}
  virtual void cargarDatos(const std::string &archivo) = 0;
  virtual std::vector<int>
  BFS(int nodoInicio, int nodoDestino) = 0; // Returns path or distances
  virtual std::vector<int>
  BFSWithDepth(int nodoInicio,
               int profundidadMax) = 0; // Returns nodes within depth
  virtual std::vector<int>
  DFS(int nodoInicio) = 0; // Returns DFS traversal order
  virtual int obtenerGrado(int nodo) = 0;
  virtual std::vector<int> getVecinos(int nodo) = 0;
  virtual int getNumNodos() = 0;
  virtual int getNumAristas() = 0;
};

#endif // GRAFOBASE_H
