"""
Description:
    This example solves and visualizes the CPP on the network derived from the Sleeping Giant State Park trail map.

    This example produces the following in `/output`.  The output is contained within this repo for convenience,
    and so I can embed the visualizations in the documentation throughout.
      - an SVG of the optimal route with edges annotated by order
      - a GIF that animates the static images with the walk order of each edge
      - a directory of static PNGs needed to create the GIF
      - a dot graph representation (file) of the static network augmented with Eulerian circuit info.

Usage:
    The simplest way to run this example is at the command line with the code below.  To experiment within an
    interactive python environment using an interpreter (ex, Jupyter notebook), remove the `if __name__ == '__main__':`
    line, and you should be good to go.

        ```
        chinese_postman_sleeping_giant
        ```

        If that entry point doesn't work, you can always run the script directly:
        ```
        python postman_problems/examples/sleeping_giant/cpp_sleeping_giant.py
        ```

    To run just the CPP optimization (not the viz) from the command line with different parameters, for example
    starting from a different node, try:
        ```
        chinese_postman \
        --edgelist_filename 'postman_problems/examples/sleeping_giant/edgelist_sleeping_giant.csv' \
        --start_node 'rs_end_south'
        ```
"""

import logging
import pandas as pd
import argparse
from postman_problems.solver import cpp
from postman_problems.stats import calculate_postman_solution_stats

import fetch_data as fd
import save_route as sr
import plot_path as pp
import constants

def main():
    """Solve the CPP and create visualizations and gpx tracks"""

    ps = argparse.ArgumentParser(description="Chinese postman problem")
    ps.add_argument("--place",
                    type=str,
                    help="Specify place to search. Example: 'Klosterneuburg, Austria")
    ps.add_argument("--address",
                    type=str,
                    help="Specify address to search. Example: 'Südtiroler Weg 5, 3400 Klosterneuburg")
    ps.add_argument("--weight",
                    type=str,
                    choices=['distance', 'impedance'],
                    default="impedance",
                    help="Specify weigth for edges.")
    args = ps.parse_args()


    # setup logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # fetching data
    edgelist, nodelist, startnode, fileprefix = fd.get_data(args.place, args.address)

    # SOLVE CPP -------------------------------------------------------------------------

    logger.info('Solve CPP')
    circuit, graph = cpp(edgelist, startnode, edge_weight=args.weight, verbose=True)

    logger.debug('Print the CPP solution:')
    for e in circuit:
        logger.debug(e)

    logger.info('Solution summary stats:')
    for k, v in calculate_postman_solution_stats(circuit).items():
        logger.info(str(k) + ' : ' + str(v))

    # VIZ -------------------------------------------------------------------------------
    try:
        from postman_problems.viz import (
            add_pos_node_attribute, add_node_attributes, plot_circuit_graphviz, make_circuit_images, make_circuit_video
        )

        logger.info('Add node attributes to graph')
        nodelist_df = pd.read_csv(nodelist, dtype={"id": str})
        graph = add_node_attributes(graph, nodelist_df)  # add attributes
        graph = add_pos_node_attribute(graph, origin='topleft')  # add X,Y positions in format for graphviz

        # gif creation disabled
        #logger.info('Creating single SVG of CPP solution')
        #plot_circuit_graphviz(circuit=circuit,
        #                      graph=graph,
        #                      filename=constants.CPP_SVG_FILENAME,
        #                      format='svg',
        #                      engine='neato',
        #                      graph_attr=constants.GRAPH_ATTR,
        #                      edge_attr=constants.EDGE_ATTR,
        #                      node_attr=constants.NODE_ATTR)
        #
        #logger.info('Creating PNG files for GIF')
        #make_circuit_images(circuit=circuit,
        #                    graph=graph,
        #                    outfile_dir=constants.PNG_PATH,
        #                    format='png',
        #                    engine='neato',
        #                    graph_attr={'label': 'Base Graph: Chinese Postman Solution', 'labelloc': 't'})
        #
        #logger.info('Creating GIF')
        #video_message = make_circuit_video(infile_dir_images=constants.PNG_PATH,
        #                                   outfile_movie=constants.CPP_GIF_FILENAME,
        #                                   fps=5)
        #
        #logger.info(video_message)
        #logger.info("and that's a wrap, checkout the output!")

    except FileNotFoundError(OSError) as e:
        print(e)
        print("Sorry, looks like you don't have all the needed visualization dependencies.")


    logger.info('Create GPX')
    sr.save_route_as_gpx(graph, circuit, open(constants.OUTPUT_PATH + fileprefix + "_" + args.weight + ".gpx", "w"))

    logger.info('Plot route')
    lat, long = pp.route_to_long_lat(graph, circuit)
    pp.plot_path(lat, long, graph.nodes()[startnode], graph.nodes()[startnode])

if __name__ == '__main__':
    main()
