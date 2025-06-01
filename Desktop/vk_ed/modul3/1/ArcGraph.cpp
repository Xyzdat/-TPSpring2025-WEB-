#include "ArcGraph.h"
#include <cassert>

ArcGraph::ArcGraph(int size) : verticesCount(size) {}

ArcGraph::ArcGraph(const IGraph& graph) {
    verticesCount = graph.VerticesCount();
    for (int from = 0; from < verticesCount; ++from) {
        for (int to : graph.GetNextVertices(from)) {
            edges.emplace_back(from, to);
        }
    }
}

void ArcGraph::AddEdge(int from, int to) {
    assert(from >= 0 && from < verticesCount);
    assert(to >= 0 && to < verticesCount);
    edges.emplace_back(from, to);
}

int ArcGraph::VerticesCount() const {
    return verticesCount;
}

std::vector<int> ArcGraph::GetNextVertices(int vertex) const {
    std::vector<int> result;
    for (auto& [from, to] : edges) {
        if (from == vertex) result.push_back(to);
    }
    return result;
}

std::vector<int> ArcGraph::GetPrevVertices(int vertex) const {
    std::vector<int> result;
    for (auto& [from, to] : edges) {
        if (to == vertex) 
            result.push_back(from);
    }
    return result;
}
