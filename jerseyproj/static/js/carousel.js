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
    console.log(stepsArray[index].getAttribute("value"))
    console.log(stepsArray[index].getAttribute("map"))
    mapContainers[stepsArray[index].getAttribute("value")].appendChild(mapObject);
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
    console.log(stepsArray[index].getAttribute("value"))
    console.log(stepsArray[index].getAttribute("map"))
    mapContainers[stepsArray[index].getAttribute("value")].appendChild(mapObject);
    clearMap();
    updateMap(stepsArray[index].getAttribute("value"), stepsArray[index].getAttribute("map"));
});

// OCCUPATIONS

var $carousel_demographics = $('.main-carousel-occupations');

$carousel_demographics.on('change.flickity', function (event, index) {
    var steps = $(this).find('.step');
    var stepsArray = [];
    steps.each(function () {
        stepsArray.push(this);
    });
    console.log(stepsArray[index].getAttribute("value"))
    console.log(stepsArray[index].getAttribute("map"))
    mapContainers[stepsArray[index].getAttribute("value")].appendChild(mapObject);
    clearMap();
    updateMap(stepsArray[index].getAttribute("value"), stepsArray[index].getAttribute("map"));
});