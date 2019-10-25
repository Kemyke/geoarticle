# geoarticle

## Overview

During our trip to Porto we read a lot of articles with the best locations around. None of the articles contain a map so it was hard to find which cities are in the
same direction or close to each other. It was a pain to find all the places on Google Maps.
This project came to life to solve this problem. Just paste the article URL and location names will be extracted and visualized.

Try it on [https://geoarticle.kemy.cc](https://geoarticle.kemy.cc)! 

## Techinal details

The project supports multiple geocode services. Curreently [MapQuest](https://www.mapquest.com) is used because the support of batch geocode query api which 
only generates one geocode request per article. 

The article text is extracted from the webpage with the help of [Newspaper](https://github.com/codelucas/newspaper). This library works perfectly well during my tests.

The hard part is to recognize locations and cities in the article. The [GeoText](https://github.com/elyase/geotext) library is a decent solution to get city names 
from the article. However it will fail when it comes to recognize rivers, mountains, museums, valleys, and everything except cities. I will definitely do some experiment
with spaCy and named entity recognition in the future.


