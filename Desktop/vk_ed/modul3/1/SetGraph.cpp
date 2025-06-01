#include "SetGraph.h"

SetGraph::SetGraph(int size) : adjacencySets(size) {}

SetGraph::SetGraph(const IGraph& graph) {
    int size = graph.VerticesCount();
    adjacencySets.resize(size);
    for (int from = 0; from < size; ++from) {
        for (int to : graph.GetNextVertices(from)) {
            adjacencySets[from].insert(to);
        }
    }
}

void SetGraph::AddEdge(int from, int to) {
    assert(from >= 0 && from < adjacencySets.size());
    assert(to >= 0 && to < adjacencySets.size());
    adjacencySets[from].insert(to);
}

int SetGraph::VerticesCount() const {
    return (int)adjacencySets.size();
}

std::vector<int> SetGraph::GetNextVertices(int vertex) const {
    return std::vector<int>(adjacencySets[vertex].begin(), adjacencySets[vertex].end());
}

std::vector<int> SetGraph::GetPrevVertices(int vertex) const {
    std::vector<int> result;
    for (int from = 0; from < adjacencySets.size(); ++from) {
        if (adjacencySets[from].find(vertex) != adjacencySets[from].end()) {
            result.push_back(from);
        }
    }
    return result;
}
