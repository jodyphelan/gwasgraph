def graph2adj(graph):
    nodeObj = {}
    for node in tqdm(graph["nodes"]):
        nid = node["id"]
        nodeSet = set()
        for edge in graph["edges"]:
            if edge["source"]==nid:
                nodeSet.add(edge["target"])
            if edge["target"]==nid:
                nodeSet.add(edge["source"])
        node["adj"] = list(nodeSet)
        nodeObj[nid] = node
    return nodeObj
