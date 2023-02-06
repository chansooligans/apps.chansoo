import { updateMap } from './leaflet.js';
import { clearMap } from './leaflet.js';

// MAIN

var $carousel = $('.main-carousel');

$carousel.on('change.flickity', function (event, index) {
    var steps = $(this).find('.step');
    var stepsArray = [];
    steps.each(function () {
        stepsArray.push(this);
    });
    mapContainers[stepsArray[index].getAttribute("value")].appendChild(mapObject);
    console.log("carousel-update-map")
    clearMap();
    updateMap(stepsArray[index].getAttribute("value"), stepsArray[index].getAttribute("map"));
});

// DEMOGRAPHICS

var $carousel_demographics = $('.main-carousel-demographics');

$carousel_demographics.on('change.flickity', function (event, index) {
    var steps = $(this).find('.step');
    var stepsArray = [];
    steps.each(function () {
        stepsArray.push(this);
    });
    mapContainers[stepsArray[index].getAttribute("value")].appendChild(mapObject);
    console.log("carousel-update-map")
    clearMap();
    updateMap(stepsArray[index].getAttribute("value"), stepsArray[index].getAttribute("map"));
});

// OCCUPATIONS

var $carousel_occupations = $('.main-carousel-occupations');

$carousel_occupations.on('change.flickity', function (event, index) {
    var steps = $(this).find('.step');
    var stepsArray = [];
    steps.each(function () {
        stepsArray.push(this);
    });
    mapContainers[stepsArray[index].getAttribute("value")].appendChild(mapObject);
    console.log("carousel-update-map")
    clearMap();
    updateMap(stepsArray[index].getAttribute("value"), stepsArray[index].getAttribute("map"));
});

// DIALECTS

var $carousel_dialects = $('.main-carousel-dialects');

$carousel_dialects.on('change.flickity', function (event, index) {
    var steps = $(this).find('.step');
    var stepsArray = [];
    steps.each(function () {
        stepsArray.push(this);
    });
    mapContainers[stepsArray[index].getAttribute("value")].appendChild(mapObject);
    console.log("carousel-update-map")
    clearMap();
    updateMap(stepsArray[index].getAttribute("value"), stepsArray[index].getAttribute("map"));
});

// PREDICTIONS

var $carousel_predictions = $('.main-carousel-predictions');

$carousel_predictions.on('change.flickity', function (event, index) {
    var steps = $(this).find('.step');
    var stepsArray = [];
    steps.each(function () {
        stepsArray.push(this);
    });
    mapContainers[stepsArray[index].getAttribute("value")].appendChild(mapObject);
    console.log("carousel-update-map")
    clearMap();
    updateMap(stepsArray[index].getAttribute("value"), stepsArray[index].getAttribute("map"));
});