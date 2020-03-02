from tulip import tlp

graph = tlp.newGraph()
for i in range(10):
    graph.addNode()
print(graph.numberOfNodes())

for n1 in graph.nodes():
    for n2 in graph.nodes():
        graph.addEdge(n1, n2)

print(graph.numberOfEdges())

graph.delEdges(graph.edges())

for n1 in graph.nodes():
    for n2 in graph.nodes():
        if not graph.existEdge(n1, n2, False).isValid() and n1.id != n2.id:
            graph.addEdge(n1, n2)

print(graph.numberOfEdges())

pair_nodes = [n for n in graph.nodes() if n.id % 2 == 0]
graph.delNodes(pair_nodes)

print(graph.numberOfNodes())
print(graph.numberOfEdges())


# tlp.saveGraph(graph, 'dataset/example_copy.tlpbz')
