from flask import Flask, escape, request
from flask import jsonify
from flask_cors import CORS
from newspaper import Article
from geotext import GeoText
import base64
import numpy
import requests
import json
import os
import time
from haversine import haversine, Unit

app = Flask(__name__)
CORS(app)

def nexogen_geocode(city):
    geocodeurl = os.environ.get('GEOARTICLE_GEOCODE_URL') + '/gis/v1/geocode?Address=' + city + '&Limit=1&Structured=false&Priority=Low'
    response = requests.get(geocodeurl, headers={'Authorization': 'Bearer ' + os.environ.get('GEOARTICLE_GEOCODE_APIKEY')})
    results = json.loads(response.text)
    if len(results['results']) > 0:
        return [ results['results'][0]['centerPoint']['latitude'], results['results'][0]['centerPoint']['longitude'] ]
    return []

def locationiq_geocode(city):
    geocodeurl = os.environ.get('GEOARTICLE_GEOCODE_URL') + '/v1/search.php?key=' + os.environ.get('GEOARTICLE_GEOCODE_APIKEY') + '&q=' + city + '&format=json'
    response = requests.get(geocodeurl)
    results = json.loads(response.text)
    time.sleep(0.5)
    if len(results) > 0:
        return [ results[0]['lat'], results[0]['lon'] ]
    return []

def mapquest_batch_geocode(cities):
     lq="&".join(['location='+city for city in cities])
     geocodeurl = os.environ.get('GEOARTICLE_GEOCODE_URL') + '/geocoding/v1/batch?key=' + os.environ.get('GEOARTICLE_GEOCODE_APIKEY') + "&" + lq
     response = requests.get(geocodeurl)
     results = json.loads(response.text)
     ret = {}
     for result in results['results']:
        if len(result["locations"]) > 0:
            ret[result["providedLocation"]["location"]] = [result["locations"][0]["latLng"]["lat"], result["locations"][0]["latLng"]["lng"]]
     return ret

def calculate_centroid(cities):
    x = [p[0] for p in cities]
    y = [p[1] for p in cities]
    centroid = (sum(x) / len(cities), sum(y) / len(cities))
    return centroid

def get_initial_zoom(cities):
    maxd = 0
    for city1 in cities:
        for city2 in cities:
            d = haversine(city1, city2)
            if(d > maxd):
                maxd = d
    if maxd > 10000:
        return 3
    if maxd > 5000:
        return 4
    if maxd > 2500:
        return 5
    if maxd > 1200:
        return 6
    if maxd > 600:
        return 7
    return 8

@app.route('/geo/<articleurl>')
def geo(articleurl):
    url=base64.b64decode(articleurl).decode('utf-8')
    article = Article(url)
    article.download()
    article.parse()
    places = GeoText(article.text)
    cities = numpy.unique(places.cities).tolist()

    ret = {}
    if len(cities) > 0:
        ret['cities'] = mapquest_batch_geocode(cities)
        ret['centroid'] = calculate_centroid(ret['cities'].values())
        ret['init_zoom_level'] = get_initial_zoom(ret['cities'].values())
    #ret['cities']={}
    #for city in cities:
    #    coord = locationiq_geocode(city)
    #    if len(coord) > 0:
    #        ret['cities'][city] = coord
    ret['article']=article.text
    return jsonify(ret=ret) 
