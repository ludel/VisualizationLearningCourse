import csv

from tulip import tlp

graph = tlp.newGraph()
f = open('dataset/flight_airports.dat', 'r', newline='', encoding='utf-8')
airports = csv.DictReader(f, delimiter=',', quotechar='"')

f1 = open('dataset/flight_flow.dat', 'r', newline='', encoding='utf-8')
flows = csv.DictReader(f1, delimiter=',', quotechar='"')

airport_id = {}
for airport in airports:
    n = graph.addNode()
    for k in airport.keys():
        graph[k][n] = airport[k]
        airport_id[airport['Airport ID']] = n

for flow in flows:
    source = airport_id.get(flow['Source airport ID'])
    target = airport_id.get(flow['Destination airport ID'])

    if target is not None and source is not None:
        e = graph.existEdge(source, target, True)

        if not e.isValid():
            graph.addEdge(source, target)

tlp.getDoubleAlgorithmPluginsList()

tlp.getDefaultPluginParameters('Degree')

for i in range(10):
    print(graph["viewMetric"][graph.nodes()[i]])

for n in graph.nodes():
    if graph.deg(n) == 0:
        graph.delNode(n)

for n in graph.nodes():
    graph['LongDouble'][n] = float(graph['Long'][n])
    graph['LatDouble'][n] = float(graph['Lat'][n])

for n in graph.nodes():
    graph['viewLayout'][n] = tlp.Coord(graph['LongDouble'][n], graph['LatDouble'][n], 0)

# tlp.saveGraph(graph, 'save/airport.tlpbz')
# nodeLinkView = tlpgui.createView("Node Link Diagram view", graph, {}, True)
# nodeLinkView.centerView()
f.close()
f1.close()
