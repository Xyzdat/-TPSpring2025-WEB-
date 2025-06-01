#include "IGraph.h"
#include <vector>
#include <cassert>


class ListGraph: public IGraph{
public:
    // virtual ~IGraph() {}
    ListGraph(int size);
    ListGraph(const IGraph &graph);
    ~ListGraph() override = default;
        
    virtual void AddEdge(int from, int to) override;
    virtual int VerticesCount() const  override;

    virtual std::vector<int> GetNextVertices(int vertex) const override;
    virtual std::vector<int> GetPrevVertices(int vertex) const override;
private:
    std::vector<std::vector<int>> adjacencyLists;
};

