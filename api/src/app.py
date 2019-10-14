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

app = Flask(__name__)
CORS(app)

@app.route('/geo/<articleurl>')
def geo(articleurl):
    url=base64.b64decode(articleurl).decode('utf-8')
    article = Article(url)
    article.download()
    article.parse()
    places = GeoText(article.text)
    cities = numpy.unique(places.cities).tolist()

    ret = {}
    for city in cities:
        geocodeurl = os.environ.get('GEOARTICLE_GEOCODE_URL') + '/gis/v1/geocode?Address=' + city + '&Limit=1&Structured=false&Priority=Low'
        response = requests.get(geocodeurl, headers={'Authorization': 'Bearer ' + os.environ.get('GEOARTICLE_GEOCODE_APIKEY')})
        results = json.loads(response.text)
        ret[city] = [ results['results'][0]['centerPoint']['latitude'], results['results'][0]['centerPoint']['longitude'] ]

    return jsonify(ret=ret) 
