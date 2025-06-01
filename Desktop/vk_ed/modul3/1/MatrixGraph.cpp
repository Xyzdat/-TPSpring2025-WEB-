#include "MatrixGraph.h"

MatrixGraph::MatrixGraph(int size): adjacencyMatrix(size, std::vector<bool>(size, false)){}
    
MatrixGraph::MatrixGraph(const IGraph& graph) {
    int size = graph.VerticesCount();
    adjacencyMatrix.assign(size, std::vector<bool>(size, false));
    for (int from = 0; from < size; ++from) {
        for (int to : graph.GetNextVertices(from)) {
            adjacencyMatrix[from][to] = true;
        }
    }
}

void MatrixGraph::AddEdge(int from, int to) {
    assert(from >= 0 && from < adjacencyMatrix.size());
    assert(to >= 0 && to < adjacencyMatrix.size());
    adjacencyMatrix[from][to] = true;
}

int MatrixGraph::VerticesCount() const {
    return (int)adjacencyMatrix.size();
}

std::vector<int> MatrixGraph::GetNextVertices(int vertex) const {
    std::vector<int> result;
    for (int to = 0; to < adjacencyMatrix.size(); ++to) {
        if (adjacencyMatrix[vertex][to]) result.push_back(to);
    }
    return result;
}

std::vector<int> MatrixGraph::GetPrevVertices(int vertex) const {
    std::vector<int> result;
    for (int from = 0; from < adjacencyMatrix.size(); ++from) {
        if (adjacencyMatrix[from][vertex]) result.push_back(from);
    }
    return result;
}