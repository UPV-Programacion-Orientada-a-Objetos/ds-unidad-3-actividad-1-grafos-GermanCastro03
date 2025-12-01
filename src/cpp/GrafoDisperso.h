#ifndef GRAFODISPERSO_H
#define GRAFODISPERSO_H

#include "GrafoBase.h"
#include <iostream>
#include <string>
#include <vector>


class GrafoDisperso : public GrafoBase {
private:
  // CSR Format
  // We assume unweighted graph for basic structure, but values can be added if
  // needed. For unweighted, 'values' might be redundant if we only care about
  // connectivity, but we'll keep it to strictly follow "values, column_indices,
  // row_ptr" if required, or just use column_indices and row_ptr for adjacency.
  // The prompt asks for "tres vectores: valores, índices de columnas y punteros
  // de fila". So we will include 'values' even if just 1s.
  std::vector<int> values;
  std::vector<int> col_indices;
  std::vector<int> row_ptr;

  int numNodos;
  int numAristas;

public:
  GrafoDisperso();
  ~GrafoDisperso();

  void cargarDatos(const std::string &archivo) override;
  std::vector<int> BFS(int nodoInicio, int nodoDestino) override;
  std::vector<int> BFSWithDepth(int nodoInicio, int profundidadMax) override;
  std::vector<int> DFS(int nodoInicio) override;
  int obtenerGrado(int nodo) override;
  std::vector<int> getVecinos(int nodo) override;
  int getNumNodos() override;
  int getNumAristas() override;

  // New metrics
  int getNodoMasCritico();
  long long getMemoriaEstimada();

  // Helper to print stats
  void imprimirEstadisticas();
};

#endif // GRAFODISPERSO_H
