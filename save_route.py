import gpxpy

def save_route_as_gpx(G, euler_circuit, file):
    gpx = gpxpy.gpx.GPX()

    create_route = True
    if create_route:
        # create gpx with route
        gpx_route = gpxpy.gpx.GPXRoute()
        gpx.routes.append(gpx_route)
        
        for e in euler_circuit:
            #if(e[2].get(0) is not None): # workaround for ulmenweg
            lat = G.nodes()[e[1]].get('lat')
            long = G.nodes()[e[1]].get('long')
            gpx_route.points.append(gpxpy.gpx.GPXRoutePoint(long, lat))

    else:
        # create gpx with track
        gpx_track = gpxpy.gpx.GPXTrack()
        gpx.tracks.append(gpx_track)
        
        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)

        for e in euler_circuit:
            #if(e[2].get(0) is not None): # workaround for ulmenweg
            lat = G.nodes()[e[1]].get('lat')
            long = G.nodes()[e[1]].get('long')
            gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(long, lat))

    file.write(gpx.to_xml())
    file.flush()