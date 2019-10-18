new Vue({
  el: '#app',
  data: {
	map: null,
	tileLayer: null,
	articleurl: null,
	articletext: '== Article extracted text ==',
  },
  mounted() {
	this.initMap();
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
	articlechanged() {
	  eau = btoa(this.articleurl)
	  vm = this
	  var request = new XMLHttpRequest()
	  request.open('GET', 'http://192.168.0.120:5000/geo/'+eau, true)

		request.onload = function() {
		  var data = JSON.parse(this.response)
		  
		  vm.map.setView([data.ret['centroid'][0], data.ret['centroid'][1]], data.ret['init_zoom_level']);
		  vm.articletext = data.ret['article']
		  cities = data.ret['cities']
		  for (var city in cities) 
		  {
			  leafletObject = L.marker(cities[city]).bindPopup(city);
			  leafletObject.addTo(vm.map);
		  }
		}
	  request.send()
	}
  },
});
