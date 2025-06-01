#include "IGraph.h"
#include <vector>
#include <cassert>


class ArcGraph: public IGraph{
public:
    // virtual ~IGraph() {}
    ArcGraph(int size);
    ArcGraph(const IGraph &graph);
        
    virtual void AddEdge(int from, int to)  override;
    virtual int VerticesCount() const  override;

    virtual std::vector<int> GetNextVertices(int vertex) const override;
    virtual std::vector<int> GetPrevVertices(int vertex) const override;
private:
    int verticesCount;
    std::vector<std::pair<int, int>> edges;
};