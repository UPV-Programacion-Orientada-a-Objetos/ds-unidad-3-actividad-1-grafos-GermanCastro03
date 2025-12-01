#include "GrafoDisperso.h"
#include <algorithm>
#include <chrono>
#include <fstream>
#include <limits>
#include <queue>
#include <sstream>

GrafoDisperso::GrafoDisperso() : numNodos(0), numAristas(0) {
  std::cout << "[C++ Core] Inicializando GrafoDisperso..." << std::endl;
}

GrafoDisperso::~GrafoDisperso() {}

void GrafoDisperso::cargarDatos(const std::string &archivo) {
  std::cout << "[C++ Core] Cargando dataset '" << archivo << "'..."
            << std::endl;
  std::ifstream file(archivo);
  if (!file.is_open()) {
    std::cerr << "Error: No se pudo abrir el archivo " << archivo << std::endl;
    return;
  }

  std::vector<std::pair<int, int>> edges;
  int u, v;
  int maxNode = -1;

  std::string line;
  while (std::getline(file, line)) {
    if (line.empty() || line[0] == '#')
      continue;
    std::stringstream ss(line);
    if (ss >> u >> v) {
      edges.push_back({u, v});
      if (u > maxNode)
        maxNode = u;
      if (v > maxNode)
        maxNode = v;

      // Assuming undirected graph for connectivity, or directed?
      // SNAP web-Google is directed.
      // User prompt: "analizar la robustez... ante fallos en cascada".
      // Usually implies directed, but "web-Google" is directed.
      // Let's stick to the input as-is (Directed).
      // If undirected is needed, we'd add {v, u} too.
      // Let's assume Directed for now as it's more general for CSR.
    }
  }
  file.close();

  numNodos = maxNode + 1;
  numAristas = edges.size();

  // Sort edges by source, then destination
  std::sort(edges.begin(), edges.end());

  // Build CSR
  row_ptr.assign(numNodos + 1, 0);
  col_indices.reserve(numAristas);
  values.assign(numAristas, 1); // Default weight 1

  int current_row = 0;
  for (const auto &edge : edges) {
    int src = edge.first;
    int dst = edge.second;

    // Fill row_ptr gaps if we skip nodes
    while (current_row < src) {
      current_row++;
      row_ptr[current_row + 1] = row_ptr[current_row];
    }

    // Actually, a better way for row_ptr:
    // row_ptr[i] is the starting index in col_indices for row i.
    // We can count degrees first or just fill as we go if sorted.
    // Since we sorted, we can just iterate.
  }

  // Re-doing CSR construction properly
  row_ptr.assign(numNodos + 1, 0);
  std::vector<int> degrees(numNodos, 0);
  for (const auto &edge : edges) {
    degrees[edge.first]++;
  }

  // Cumulative sum for row_ptr
  int cum_sum = 0;
  for (int i = 0; i < numNodos; ++i) {
    row_ptr[i] = cum_sum;
    cum_sum += degrees[i];
  }
  row_ptr[numNodos] = cum_sum;

  // Fill col_indices
  col_indices.resize(numAristas);
  std::vector<int> current_pos = row_ptr; // Tracker for insertion position
  for (const auto &edge : edges) {
    int src = edge.first;
    int dst = edge.second;
    col_indices[current_pos[src]] = dst;
    current_pos[src]++;
  }

  std::cout << "[C++ Core] Carga completa. Nodos: " << numNodos
            << " | Aristas: " << numAristas << std::endl;
  std::cout << "[C++ Core] Estructura CSR construida. Memoria estimada: "
            << (getMemoriaEstimada() / (1024.0 * 1024.0)) << " MB."
            << std::endl;
}

std::vector<int> GrafoDisperso::BFS(int nodoInicio, int nodoDestino) {
  std::cout << "[C++ Core] Ejecutando BFS nativo..." << std::endl;
  auto start_time = std::chrono::high_resolution_clock::now();

  if (nodoInicio < 0 || nodoInicio >= numNodos)
    return {};

  std::queue<int> q;
  q.push(nodoInicio);

  std::vector<int> dist(numNodos, -1);
  std::vector<int> parent(numNodos, -1);

  dist[nodoInicio] = 0;

  bool found = false;

  while (!q.empty()) {
    int u = q.front();
    q.pop();

    if (u == nodoDestino) {
      found = true;
      break;
    }

    // Iterate neighbors using CSR
    int start_idx = row_ptr[u];
    int end_idx = row_ptr[u + 1];

    for (int i = start_idx; i < end_idx; ++i) {
      int v = col_indices[i];
      if (dist[v] == -1) {
        dist[v] = dist[u] + 1;
        parent[v] = u;
        q.push(v);
      }
    }
  }

  // Reconstruct path
  std::vector<int> path;
  if (found) {
    int curr = nodoDestino;
    while (curr != -1) {
      path.push_back(curr);
      curr = parent[curr];
    }
    std::reverse(path.begin(), path.end());
  }

  auto end_time = std::chrono::high_resolution_clock::now();
  std::chrono::duration<double, std::milli> elapsed = end_time - start_time;
  std::cout << "[C++ Core] Nodos encontrados: " << path.size()
            << ". Tiempo ejecución: " << elapsed.count() << "ms." << std::endl;

  return path;
}

std::vector<int> GrafoDisperso::BFSWithDepth(int nodoInicio,
                                             int profundidadMax) {
  std::cout << "[C++ Core] Ejecutando BFS con profundidad máxima "
            << profundidadMax << "..." << std::endl;
  auto start_time = std::chrono::high_resolution_clock::now();

  if (nodoInicio < 0 || nodoInicio >= numNodos)
    return {};

  std::queue<std::pair<int, int>> q; // (node, depth)
  q.push({nodoInicio, 0});

  std::vector<bool> visited(numNodos, false);
  std::vector<int> result;

  visited[nodoInicio] = true;
  result.push_back(nodoInicio);

  while (!q.empty()) {
    auto [u, depth] = q.front();
    q.pop();

    if (depth >= profundidadMax)
      continue;

    // Iterate neighbors using CSR
    int start_idx = row_ptr[u];
    int end_idx = row_ptr[u + 1];

    for (int i = start_idx; i < end_idx; ++i) {
      int v = col_indices[i];
      if (!visited[v]) {
        visited[v] = true;
        result.push_back(v);
        q.push({v, depth + 1});
      }
    }
  }

  auto end_time = std::chrono::high_resolution_clock::now();
  std::chrono::duration<double, std::milli> elapsed = end_time - start_time;
  std::cout << "[C++ Core] Nodos encontrados: " << result.size()
            << ". Tiempo ejecución: " << elapsed.count() << "ms." << std::endl;

  return result;
}

std::vector<int> GrafoDisperso::DFS(int nodoInicio) {
  std::cout << "[C++ Core] Ejecutando DFS nativo..." << std::endl;
  auto start_time = std::chrono::high_resolution_clock::now();

  if (nodoInicio < 0 || nodoInicio >= numNodos)
    return {};

  std::vector<bool> visited(numNodos, false);
  std::vector<int> result;
  std::vector<int> stack;

  stack.push_back(nodoInicio);

  while (!stack.empty()) {
    int u = stack.back();
    stack.pop_back();

    if (visited[u])
      continue;

    visited[u] = true;
    result.push_back(u);

    // Iterate neighbors using CSR (in reverse to maintain left-to-right DFS
    // order)
    int start_idx = row_ptr[u];
    int end_idx = row_ptr[u + 1];

    for (int i = end_idx - 1; i >= start_idx; --i) {
      int v = col_indices[i];
      if (!visited[v]) {
        stack.push_back(v);
      }
    }
  }

  auto end_time = std::chrono::high_resolution_clock::now();
  std::chrono::duration<double, std::milli> elapsed = end_time - start_time;
  std::cout << "[C++ Core] Nodos visitados: " << result.size()
            << ". Tiempo ejecución: " << elapsed.count() << "ms." << std::endl;

  return result;
}

int GrafoDisperso::obtenerGrado(int nodo) {
  if (nodo < 0 || nodo >= numNodos)
    return 0;
  return row_ptr[nodo + 1] - row_ptr[nodo];
}

std::vector<int> GrafoDisperso::getVecinos(int nodo) {
  std::vector<int> vecinos;
  if (nodo < 0 || nodo >= numNodos)
    return vecinos;

  int start_idx = row_ptr[nodo];
  int end_idx = row_ptr[nodo + 1];

  for (int i = start_idx; i < end_idx; ++i) {
    vecinos.push_back(col_indices[i]);
  }
  return vecinos;
}

int GrafoDisperso::getNumNodos() { return numNodos; }
int GrafoDisperso::getNumAristas() { return numAristas; }

int GrafoDisperso::getNodoMasCritico() {
  int maxDegree = -1;
  int maxNode = -1;
  for (int i = 0; i < numNodos; ++i) {
    int degree = row_ptr[i + 1] - row_ptr[i];
    if (degree > maxDegree) {
      maxDegree = degree;
      maxNode = i;
    }
  }
  return maxNode;
}

long long GrafoDisperso::getMemoriaEstimada() {
  return (values.size() + col_indices.size() + row_ptr.size()) * sizeof(int);
}

void GrafoDisperso::imprimirEstadisticas() {
  std::cout << "Nodos: " << numNodos << ", Aristas: " << numAristas
            << std::endl;
  size_t memSize =
      (values.size() + col_indices.size() + row_ptr.size()) * sizeof(int);
  std::cout << "Memoria estimada (CSR vectors): " << memSize / (1024.0 * 1024.0)
            << " MB" << std::endl;
}
