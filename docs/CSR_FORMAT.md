# Compressed Sparse Row (CSR) Format

## Overview

The **Compressed Sparse Row (CSR)** format is a memory-efficient way to store sparse matrices, particularly useful for representing large graphs where most nodes are not connected to each other.

## Why CSR?

### Memory Comparison

For a graph with **N nodes** and **E edges**:

| Representation | Memory Usage | Example (1M nodes, 3M edges) |
|----------------|--------------|------------------------------|
| **Dense Adjacency Matrix** | O(N²) | 1M × 1M × 4 bytes = **4 TB** |
| **Adjacency List** | O(N + E) | ~24 MB + overhead |
| **CSR Format** | O(N + 2E) | **~24 MB** (optimal) |

For sparse graphs (where E << N²), CSR provides **massive memory savings** while maintaining fast neighbor access.

## CSR Structure

CSR uses three arrays to represent a sparse adjacency matrix:

### 1. **values** (size: E)
- Stores edge weights
- For unweighted graphs, all values are 1
- `values[i]` = weight of the i-th edge

### 2. **col_indices** (size: E)
- Stores destination node IDs
- `col_indices[i]` = destination of the i-th edge

### 3. **row_ptr** (size: N+1)
- Stores starting indices in `col_indices` for each row
- `row_ptr[i]` = index where row i starts in `col_indices`
- `row_ptr[i+1] - row_ptr[i]` = out-degree of node i

## Example

### Graph Representation

Consider this directed graph:

```
0 → 1
0 → 2
1 → 3
2 → 3
2 → 4
```

**Adjacency Matrix** (5×5):
```
     0  1  2  3  4
  ┌─────────────────┐
0 │  0  1  1  0  0  │
1 │  0  0  0  1  0  │
2 │  0  0  0  1  1  │
3 │  0  0  0  0  0  │
4 │  0  0  0  0  0  │
  └─────────────────┘
```

**CSR Representation**:

```cpp
values:      [1, 1, 1, 1, 1]
col_indices: [1, 2, 3, 3, 4]
row_ptr:     [0, 2, 3, 5, 5, 5]
```

### Interpretation

- **Row 0** (node 0):
  - Starts at index `row_ptr[0] = 0`
  - Ends at index `row_ptr[1] = 2`
  - Neighbors: `col_indices[0..1] = [1, 2]`
  - Out-degree: `2 - 0 = 2`

- **Row 1** (node 1):
  - Starts at index `row_ptr[1] = 2`
  - Ends at index `row_ptr[2] = 3`
  - Neighbors: `col_indices[2..2] = [3]`
  - Out-degree: `3 - 2 = 1`

- **Row 2** (node 2):
  - Starts at index `row_ptr[2] = 3`
  - Ends at index `row_ptr[3] = 5`
  - Neighbors: `col_indices[3..4] = [3, 4]`
  - Out-degree: `5 - 3 = 2`

- **Rows 3-4** (nodes 3-4):
  - No outgoing edges
  - `row_ptr[3] = row_ptr[4] = row_ptr[5] = 5`
  - Out-degree: 0

## Operations

### Get Neighbors of Node i

```cpp
int start = row_ptr[i];
int end = row_ptr[i + 1];

for (int j = start; j < end; j++) {
    int neighbor = col_indices[j];
    int weight = values[j];
    // Process neighbor
}
```

**Time Complexity**: O(degree(i))

### Get Out-Degree of Node i

```cpp
int degree = row_ptr[i + 1] - row_ptr[i];
```

**Time Complexity**: O(1)

### Check if Edge (i, j) Exists

```cpp
int start = row_ptr[i];
int end = row_ptr[i + 1];

for (int k = start; k < end; k++) {
    if (col_indices[k] == j) {
        return true;  // Edge exists
    }
}
return false;  // Edge doesn't exist
```

**Time Complexity**: O(degree(i))

## Construction Algorithm

### From Edge List

Given edges: `[(u₁, v₁), (u₂, v₂), ..., (uₑ, vₑ)]`

```cpp
// Step 1: Sort edges by source node
sort(edges.begin(), edges.end());

// Step 2: Count out-degrees
vector<int> degrees(N, 0);
for (auto [u, v] : edges) {
    degrees[u]++;
}

// Step 3: Build row_ptr using cumulative sum
row_ptr[0] = 0;
for (int i = 0; i < N; i++) {
    row_ptr[i + 1] = row_ptr[i] + degrees[i];
}

// Step 4: Fill col_indices
vector<int> current_pos = row_ptr;  // Track insertion position
for (auto [u, v] : edges) {
    col_indices[current_pos[u]] = v;
    values[current_pos[u]] = 1;  // Or actual weight
    current_pos[u]++;
}
```

**Time Complexity**: O(E log E) for sorting + O(N + E) for construction = **O(E log E)**

## Advantages

1. **Memory Efficient**: Only stores non-zero entries
2. **Cache Friendly**: Sequential memory access for neighbors
3. **Fast Neighbor Access**: O(degree) time
4. **Fast Degree Calculation**: O(1) time
5. **Immutable**: Once built, structure is fixed (good for read-heavy workloads)

## Disadvantages

1. **Slow Edge Insertion**: Requires rebuilding entire structure
2. **Slow Edge Deletion**: Requires rebuilding entire structure
3. **No Fast Edge Lookup**: O(degree) to check if edge exists
4. **Directed Only**: Undirected graphs need to store both (u,v) and (v,u)

## Use Cases

CSR is ideal for:
- ✅ **Static graphs** (no frequent modifications)
- ✅ **Sparse graphs** (E << N²)
- ✅ **Read-heavy workloads** (many queries, few updates)
- ✅ **Large-scale graphs** (millions of nodes)
- ✅ **Graph algorithms** (BFS, DFS, PageRank, etc.)

CSR is **not ideal** for:
- ❌ **Dynamic graphs** (frequent edge insertions/deletions)
- ❌ **Dense graphs** (E ≈ N²)
- ❌ **Undirected graphs** (unless you store both directions)

## Implementation in NeuroNet

In our `GrafoDisperso` class:

```cpp
class GrafoDisperso {
private:
    std::vector<int> values;       // Edge weights (all 1s for unweighted)
    std::vector<int> col_indices;  // Destination nodes
    std::vector<int> row_ptr;      // Row pointers
    int numNodos;                  // Number of nodes
    int numAristas;                // Number of edges
    
public:
    // Load graph from edge list file
    void cargarDatos(const std::string& archivo);
    
    // Get neighbors of a node
    std::vector<int> getVecinos(int nodo);
    
    // Get out-degree of a node
    int obtenerGrado(int nodo);
};
```

### Memory Usage

For a graph with **N = 1,000,000** nodes and **E = 3,000,000** edges:

```
values:      3,000,000 × 4 bytes = 12 MB
col_indices: 3,000,000 × 4 bytes = 12 MB
row_ptr:     1,000,001 × 4 bytes = 4 MB
                        Total    = 28 MB
```

Compare this to a dense adjacency matrix:
```
1,000,000 × 1,000,000 × 4 bytes = 4,000,000 MB = 4 TB
```

**Memory savings: 99.9993%**

## Further Reading

- [Wikipedia: Sparse Matrix](https://en.wikipedia.org/wiki/Sparse_matrix#Compressed_sparse_row_(CSR,_CRS_or_Yale_format))
- [SciPy CSR Matrix Documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csr_matrix.html)
- [Intel MKL Sparse Matrix Storage](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-c/2023-0/sparse-matrix-storage-formats.html)

## Summary

CSR is a powerful format for representing sparse graphs efficiently. It trades off dynamic modification capabilities for:
- **Massive memory savings** (99%+ for sparse graphs)
- **Fast neighbor iteration** (cache-friendly sequential access)
- **Constant-time degree queries**

For static, large-scale graph analysis (like NeuroNet's use case), CSR is the optimal choice.
