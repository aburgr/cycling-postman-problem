import osmnx as ox
import csv

import constants


def get_data(place, address):
    ox.settings.log_console=True

    if place is not None:
        G = ox.graph_from_place(place, network_type='drive')
        fileprefix = place.lower().split(",")[0]
    else:
        G = ox.graph_from_address(address, network_type='drive')
        fileprefix = address.lower().split(",")[0]

    G = ox.add_node_elevations_google(G, 
        None,
        "https://api.opentopodata.org/v1/aster30m?locations={}&key={}",
        max_locations_per_batch=100)
    G = ox.add_edge_grades(G)

    G = ox.utils_graph.get_undirected(G)

    # write edges file
    edgelist = "{}{}_edges.csv".format(constants.INPUT_PATH, fileprefix)
    header = ['node1', 'node2', 'trail', 'color', 'distance', 'estimate', 'required', 'grade', 'rise', 'impedance']
    with open(edgelist, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)

        edges = []
        for e in G.edges(data=True):
            rise = e[2]['length']*e[2]['grade_abs']
            impedance = e[2]['length'] + (e[2]['length']*e[2]['grade_abs'])**2
            edges.append([e[0], e[1], 'trail', 'red', e[2]['length'], '0', '1', e[2]['grade'], rise, impedance])
        
        writer.writerows(edges)

    # write nodes file
    nodelist = "{}{}_nodes.csv".format(constants.INPUT_PATH, fileprefix)
    header = ['id', 'X', 'Y', 'lat', 'long']
    with open(nodelist, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)

        # get min/max of nodes to scale x & y
        max_x = max([node[1]['x'] for node in G.nodes(data=True)])
        min_x = min([node[1]['x'] for node in G.nodes(data=True)])
        max_y = max([node[1]['y'] for node in G.nodes(data=True)])
        min_y = min([node[1]['y'] for node in G.nodes(data=True)])

        nodes = []
        for n in G.nodes(data=True):
            # scale lat and long to 1000 pixels
            x = (n[1]['x'] - min_x)/(max_x - min_x) * 1000
            y = (max_y - n[1]['y'])/(max_y - min_y) * 1000

            nodes.append([n[0], int(x), int(y), n[1]['x'], n[1]['y']])
        
        writer.writerows(nodes)
    
    return (edgelist,
            nodelist,
            str(list(G.nodes().keys())[0]), # first node
            fileprefix
            )