#! /usr/bin/python

import json
import sys
from tqdm import tqdm
from copy import deepcopy

candidates = [x.rstrip() for x in open("candidates").readlines()]
main_graph = json.loads(open(sys.argv[1]).readline())


def traverse(temp_graph,depth,graph,node_id,d_max):
    if node_id not in main_graph:
        return
    if node_id not in temp_graph["nset"]:
        temp_graph["nset"].add(node_id)
        temp_graph["nodes"].append(main_graph[node_id])
    if int(main_graph[node_id]["drug"])==int(1):
        temp_graph["dr"].append((depth,node_id))
    if depth>=d_max:
        for nid in main_graph[node_id]["adj"]:
            if nid in temp_graph["nset"]:
                string_edge = node_id+"-"+nid
                if string_edge not in temp_graph["eset"]:
                    temp_graph["eset"].add(string_edge)
                    temp_graph["edges"].append({"source":node_id,"target":nid})
        return
    for nid in main_graph[node_id]["adj"]:
        string_edge = node_id+"-"+nid
        if string_edge not in temp_graph["eset"]:
            temp_graph["eset"].add(string_edge)
            temp_graph["edges"].append({"source":node_id,"target":nid})
        traverse(temp_graph,depth+1,main_graph,nid,d_max)


for candidate in tqdm(candidates):
    new_graph = {"nodes":[],"nset":set(),"edges":[],"eset":set(),"dr":[]}
    traverse(new_graph,0,main_graph,candidate,int(sys.argv[2]))
    if len(new_graph["dr"])>0:
        new_graph = deepcopy(new_graph)
        for n in new_graph["nodes"]:
            if n["drug"] == 1:
                n["col"] = "red"
            if n["id"]==candidate:
                n["col"] = "blue"

        open(candidate+".graph.json","w").write(json.dumps({"nodes":new_graph["nodes"],"edges":new_graph["edges"]}))
