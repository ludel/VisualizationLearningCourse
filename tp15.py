import csv

from tulip import tlp
from tulipgui import tlpgui

graph = tlp.newGraph()
viewLabel = graph.getStringProperty("viewLabel")


def set_node(field, cache_key=None):
    if cache_key is None:
        cache_key = field

    for value in project[field].split(';'):
        if value not in cache[cache_key].keys():
            node = graph.addNode()
            cache[cache_key][value] = node


with open('dataset/cordis-fp7projects.csv', 'r', newline='', encoding='utf-8') as f:
    projects = csv.DictReader(f, delimiter='\t', quotechar='"')
    print(projects.fieldnames)
    cache = {name: {} for name in projects.fieldnames}
    cache['project'] = {}

    small_projects = list(projects)[:10]
    for project in small_projects:
        p = graph.addNode()
        cache['project'][project['id']] = p

        set_node('coordinatorCountry')
        set_node('coordinator')
        # set_node('participantCountries', cache_key='coordinatorCountry')
        set_node('participants')

    for project in small_projects:
        e = graph.addEdge(cache['project'][project['id']], cache['coordinatorCountry'][project['coordinatorCountry']])
        viewLabel[e] = 'pays'
        graph.addEdge(cache['coordinatorCountry'][project['coordinatorCountry']], cache['coordinator'][project['coordinator']])
        for participant, linked_node in cache['participants'].items():
            graph.addEdge(cache['coordinator'][project['coordinator']], linked_node)

print(graph.numberOfNodes())

params = tlp.getDefaultPluginParameters('Random layout')
graph.applyLayoutAlgorithm('Random layout', params)

tlp.saveGraph(graph, 'save/project.tlpbz')

nodeLinkView = tlpgui.createView("Node Link Diagram view", graph, {}, True)
nodeLinkView.centerView()
