new Vue({
  el: '#app',
  data: {
	map: null,
	tileLayer: null,
	articleurl: null,
  },
  mounted() {
	this.initMap();
	this.initLayers();
  },
  methods: {
	initMap() {
		this.map = L.map('map').setView([41.1621376,-8.6569731], 11);
		this.tileLayer = L.tileLayer('https://cartodb-basemaps-{s}.global.ssl.fastly.net/rastertiles/voyager/{z}/{x}/{y}.png',
			{
				maxZoom: 18,
				attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, &copy; <a href="https://carto.com/attribution">CARTO</a>',
			}
		);
		this.tileLayer.addTo(this.map);
	},
	initLayers() {

	},
	articlechanged() {
	  eau = btoa(this.articleurl)
	  m = this.map
	  var request = new XMLHttpRequest()
	  request.open('GET', process.env.GEOARTICLE_URL+'/geo/'+eau, true)

		request.onload = function() {
		  var data = JSON.parse(this.response)
		  
		  cities = data.ret
		  for (var city in cities) 
		  {
			  console.log(cities[city])
			  leafletObject = L.marker(cities[city]).bindPopup(city);
			  leafletObject.addTo(m);
		  }
		}
	  request.send()
	}
  },
});
