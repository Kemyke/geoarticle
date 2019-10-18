new Vue({
  el: '#app',
  data: {
	map: null,
	tileLayer: null,
	articleurl: null,
	articletext: null,
	marked_articletext: '== Article extracted text ==',
	markers: [],
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
		vm = this
                this.map.on('popupopen', function (e) {
			vm.marked_articletext = vm.articletext.split(e.popup._source._city).join("<mark>"+e.popup._source._city+"</mark>");
                });

	},
	articlechanged() {
	  eau = btoa(this.articleurl)
	  vm = this
	  var request = new XMLHttpRequest()

	  for (var marker in this.markers)
	  this.markers.forEach(function (marker, index) {	
             vm.map.removeLayer(marker);
	  });
	  request.open('GET', 'https://geoarticleapi.kemy.cc/geo/'+eau, true)

		request.onload = function() {
		  var data = JSON.parse(this.response)
		  
		  vm.map.setView([data.ret['centroid'][0], data.ret['centroid'][1]], data.ret['init_zoom_level']);
		  vm.articletext = data.ret['article']
	          vm.marked_articletext = vm.articletext
		  cities = data.ret['cities']
		  for (var city in cities) 
		  {
			  marker = L.marker(cities[city])
			  leafletObject = marker.bindPopup(city);
			  leafletObject._city = city;
			  leafletObject.addTo(vm.map);
			  vm.markers.push(marker);
		  }
		}
	  request.send()
	}
  },
});
