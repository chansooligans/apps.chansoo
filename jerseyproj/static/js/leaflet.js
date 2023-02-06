if (window.innerWidth < 500) {
    var map = L.map('map', { zoomSnap: 0.5 }).setView([39.960349997613395, -74.65969244237529], 7.5);
} else {
    var map = L.map('map', { zoomSnap: 0.5 }).setView([40.19699338909772, -74.29685434135924], 8);
}
var legend = L.control({ position: 'bottomright' });
var colors = [
    '#F13D16',
    '#F09D8B',
    '#8BBDF0',
    '#0153A7',
    '#c2c2c2'
]
var reverseColors = [
    '#0153A7',
    '#8BBDF0',
    '#F09D8B',
    '#F13D16',
    '#c2c2c2'
]
var reverseColumns = [
    "wawa_id",
    "pork_roll",
    "drawer",
    "occu_Service occupations:",
]
var predcolors = [
    '#F13D16',
    '#ebd58d',
    '#b9f0ea',
    '#0153A7',
    '#c2c2c2'
]
var labels = [
    "0-25 Percentile",
    "25-50 Percentile",
    "50-75 Percentile",
    "75-100 Percentile",
    "N/A"
];

var reverse_labels = [
    "75-100 Percentile",
    "50-75 Percentile",
    "25-50 Percentile",
    "0-25 Percentile",
    "N/A"
];

var predict_labels = [
    "0-25%",
    "25-50%",
    "50-75%",
    "75-100%",
    "N/A"
];

let geojson = {};

export const updateMap = function (column, geojson_url) {
    console.log("updateMap")
    var percentile = 25;
    var values = []
    var buckets = {}

    if (geojson[geojson_url]) {
        console.log("use cached data")
        processData(geojson[geojson_url]);
    } else {
        d3.json(geojson_url, function (error, data) {
            console.log("load data")
            if (error) throw error;

            geojson[geojson_url] = data;
            processData(geojson[geojson_url]);
        });
    }

    function processData(geojson) {
        geojson.features.forEach(feature => {
            values.push(parseFloat(feature.properties[column]));
        });
        const sortedValues = values.sort(function (a, b) { return a - b });
        for (let i = 0; i <= 100; i += percentile) {
            const index = Math.floor((sortedValues.length - 1) * i / 100);

            if (column != "loc") {
                buckets[i + "%"] = Math.round(sortedValues[index] * 10000) / 10000;
            } else {
                buckets[i + "%"] = i / 100;
            }
        }

        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19
        }).addTo(map);

        function style(feature) {
            var value = feature.properties[column];

            if (column != "loc") {
                var tempcolors = (reverseColumns.includes(column)) ? reverseColors : colors;
            } else {
                var tempcolors = predcolors;
            }


            // Define the fill color based on the value
            var fillColor;
            if (value >= 0 && value < buckets['25%']) {
                fillColor = tempcolors[0];
            } else if (value >= buckets['25%'] && value < buckets['50%']) {
                fillColor = tempcolors[1];
            } else if (value >= buckets['50%'] && value < buckets['75%']) {
                fillColor = tempcolors[2];
            } else if (value >= buckets['75%']) {
                fillColor = tempcolors[3];
            } else {
                fillColor = tempcolors[4];
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
                "Value: " + Math.round(feature.properties[column] * 1000) / 1000,
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
            // console.log(bucket_values)
            var div = L.DomUtil.create('div', 'info legend')

            var tempcolors = (reverseColumns.includes(column)) ? reverseColors : colors;

            if (column != "loc") {
                var templabels = (reverseColumns.includes(column)) ? reverse_labels : labels;
            } else {
                var templabels = predict_labels
            }
            // loop through our density intervals and generate a label with a colored square for each interval
            for (var i = 0; i < bucket_values.length; i++) {
                div.innerHTML +=
                    '<i style="background:' + tempcolors[i] + '"></i> ' +
                    templabels[i] + '<br>'
                // bucket_values[i] + (bucket_values[i + 1] ? '&ndash;' + bucket_values[i + 1] + '<br>' : '+');
            }

            return div;
        };

        legend.addTo(map);
    };
}

export const clearMap = function () {
    map.eachLayer(function (layer) {
        map.removeLayer(layer);
    });
    map.removeControl(legend);
}
