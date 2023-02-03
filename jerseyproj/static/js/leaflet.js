var map = L.map('map').setView([40.11851, -74.671826], 8);
var legend = L.control({ position: 'bottomright' });
var colors = [
    '#F13D16',
    '#F09D8B',
    '#8BBDF0',
    '#0153A7',
    '#c2c2c2'
]
var geojson;
var values = [];
var buckets = {};

export const updateMap = function (column, geojson_url) {
    var percentile = 25;
    var values = []
    var buckets = {}

    d3.json(geojson_url, function (error, data) {
        if (error) throw error;

        geojson = data;
        geojson.features.forEach(feature => {
            values.push(parseFloat(feature.properties[column]));
        });
        const sortedValues = values.sort(function (a, b) { return a - b });
        for (let i = 0; i <= 100; i += percentile) {
            const index = Math.floor((sortedValues.length - 1) * i / 100);
            buckets[i + "%"] = Math.round(sortedValues[index] * 100) / 100;
        }

        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }).addTo(map);

        function style(feature) {
            var value = feature.properties[column];


            // Define the fill color based on the value
            var fillColor;
            if (value >= 0 && value < buckets['25%']) {
                fillColor = colors[0];
            } else if (value >= buckets['25%'] && value < buckets['50%']) {
                fillColor = colors[1];
            } else if (value >= buckets['50%'] && value < buckets['75%']) {
                fillColor = colors[2];
            } else if (value >= buckets['75%']) {
                fillColor = colors[3];
            } else {
                fillColor = colors[4];
            }

            return {
                fillColor: fillColor,
                weight: 1,
                opacity: 0.4,
                color: 'white',
                dashArray: '3',
                fillOpacity: 0.4
            };
        }

        function onEachFeature(feature, layer) {
            layer.bindTooltip(
                "Value: " + feature.properties[column],
                { permanent: false, direction: 'center', className: 'myCSSClass' }
            );
            layer.on({
                mouseover: function (e) {
                    this.openTooltip();
                },
                mouseout: function (e) {
                    this.closeTooltip();
                }
            });
        }

        L.geoJSON(geojson, { style: style, onEachFeature: onEachFeature }).addTo(map);

        legend.onAdd = function (map) {
            var bucket_values = Object.values(buckets);
            console.log(bucket_values)
            var div = L.DomUtil.create('div', 'info legend'),
                grades = bucket_values,
                labels = [];

            // loop through our density intervals and generate a label with a colored square for each interval
            for (var i = 0; i < grades.length; i++) {
                div.innerHTML +=
                    '<i style="background:' + colors[i] + '"></i> ' +
                    grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
            }

            return div;
        };

        legend.addTo(map);
    });
}

export const clearMap = function () {
    map.eachLayer(function (layer) {
        map.removeLayer(layer);
    });
    map.removeControl(legend);
}

