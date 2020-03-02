from tulip import tlp
from tulipgui import tlpgui

graph = tlp.loadGraph('save/airport.tlpbz')

for n in graph.nodes():
    graph['viewMetric'][n] = float(graph['Timezone'][n])

ds = tlp.getDefaultPluginParameters('Color Mapping')
ds['color scale'] = {0: (255, 25, 28, 200), 0.33: (253, 174, 97, 200), 0.66: (171, 221, 164, 200),
                     1: (43, 131, 186, 200)}
ds['input property'] = graph['viewMetric']

graph.applyColorAlgorithm('Color Mapping', ds)
graph['viewColor'].setAllEdgeValue((200, 200, 200, 200))
nodeLinkView = tlpgui.createView("Geographic view", graph, {}, True)
