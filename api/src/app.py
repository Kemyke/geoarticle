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
        ret[result["providedLocation"]["location"]] = [result["locations"][0]["latLng"]["lat"], result["locations"][0]["latLng"]["lng"]]
     return ret


@app.route('/geo/<articleurl>')
def geo(articleurl):
    url=base64.b64decode(articleurl).decode('utf-8')
    article = Article(url)
    article.download()
    article.parse()
    places = GeoText(article.text)
    cities = numpy.unique(places.cities).tolist()

    ret = {}
    ret['cities'] = mapquest_batch_geocode(cities)
    #ret['cities']={}
    #for city in cities:
    #    coord = locationiq_geocode(city)
    #    if len(coord) > 0:
    #        ret['cities'][city] = coord
    ret['article']=article.text
    return jsonify(ret=ret) 
