# Python 3
import requests
import os
import json

from geojson import LineString

# initialisation with your API KEY
AUTH_TOKEN = os.environ.get('SEAROUTES_API_TOKEN')
# base url for the subsequent requests
ENDPOINT = "https://api.searoutes.com/gr/route"
# custom headers with our API key
HEADERS = {
    'accept': 'application/json',
    'x-api-key': AUTH_TOKEN
}


def to_geojson(response):
    '''to GEOJSON'''
    geojson_response = {
        "type": "FeatureCollection",
        "features": []
    }
    route = json.loads(response.content)
    for route_json in route.get("getRouteJson"):
        geom = LineString([(p["lon"], p["lat"]) for p in route_json.get("routepoints")])
        del route_json["routepoints"]
        geojson_response["features"].append({
            "type":"Feature",
            "properties": route_json,
            "geometry": geom
        })
    return geojson_response


# Fetch route
def query_data(from_point, to_point, request_params={}):
    print("Start Querying Searoutes API...")
    url = f'{ENDPOINT}/{from_point}/{to_point}'
    response = requests.get(url, headers=HEADERS, params=request_params)
    route = to_geojson(response)
    return route


if __name__ == "__main__":
    # distance and ETA only
    from_point = 'lon:-4.5lat:49.6'
    to_point = 'lon:48lat:67.9'
    request_params = {'downsamplingRate': 100}
    route = query_data(from_point, to_point, request_params)
    print("--- --- copy this to geojson.io --- --- --- --- --- --->")
    print(route)
    print("--- --- --- --- --- --- --- --- --- --- --- --- --- --->")

    # route with avoid secazones
    from_point = 'lon:-4.5lat:49.6'
    to_point = 'lon:48lat:67.9'
    request_params = {'avoidSeca': 'true'}
    route = query_data(from_point, to_point, request_params)
    print("--- --- copy this to geojson.io --- --- --- --- --- --->")
    print(route)
    print("--- --- --- --- --- --- --- --- --- --- --- --- --- --->")
