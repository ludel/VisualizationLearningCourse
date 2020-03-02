from tulip import tlp

graph = tlp.newGraph()

new_nodes = [graph.addNode()]
for i in range(5):
    tmp_main_nodes, new_nodes = new_nodes, []
    for main_node in tmp_main_nodes:
        for _ in range(5):
            new_nodes.append(graph.addNode())
            graph.addEdge(main_node, new_nodes[-1])

tlp.saveGraph(graph, 'dataset/table.tlpbz')
