import numpy as np
import plotly.graph_objects as go

def route_to_long_lat(G, route):
    """
    :param G: the graph
    :param route: list of nodes
    :return: list of longitude and latitude of those nodes
    """
    long = []
    lat = []
    for i in route:
        point = G.nodes()[i[0]]
        long.append(point.get('long'))
        lat.append(point.get('lat'))
    return long, lat

def plot_path(lat, long, origin_point, destination_point):
    """
    Plot a path on a map
    :param lat: list of latitudes
    :param long: list of longitudes
    :param origin_point: co-ordinates of origin
    :param destination_point: co-ordinates of destination
    """
    # adding the lines joining the nodes
    fig = go.Figure(go.Scattermapbox(
        name="Path",
        mode="lines",
        lon=long,
        lat=lat,
        marker={'size': 10},
        line=dict(width=2.5, color='blue')))

    # getting center for plots:
    lat_center = np.mean(lat)
    long_center = np.mean(long)
    # defining the layout using mapbox_style
    fig.update_layout(mapbox_style="stamen-terrain",
                      mapbox_center_lat=30, mapbox_center_lon=-80)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                      mapbox={
                          'center': {'lat': lat_center,
                                     'lon': long_center},
                          'zoom': 13})
    fig.show()