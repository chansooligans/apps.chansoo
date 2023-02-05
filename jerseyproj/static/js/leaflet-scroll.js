import { updateMap } from './leaflet.js';
import { clearMap } from './leaflet.js';

var scrolly = document.querySelector("#scrolly");
var article = scrolly.querySelector("article");

// initialize the scrollama
var scroller = scrollama();

// scrollama event handlers
function handleStepEnter(response) {
    // response = { element, direction, index }
    // console.log(response.element);
    d3.select(response.element)
        .select(".placeholder")
        .style("display", "none")
    if (response.element.hasAttribute("value")) {
        mapContainers[response.element.getAttribute("value")].appendChild(mapObject);
        updateMap(response.element.getAttribute("value"), response.element.getAttribute("map"));
    }
    // add to color to current step
    response.element.classList.add("is-active");
}

function handleStepExit(response) {
    // response = { element, direction, index }
    d3.select(response.element)
        .select(".placeholder")
        .style("display", "")
    // remove color from current step
    clearMap();
    response.element.classList.remove("is-active");
}

function init() {
    // find the halfway point of the initial viewport height
    // (it changes on mobile, but by just using the initial value
    // you remove jumpiness on scroll direction change)
    var midpoint = Math.floor(window.innerHeight * 0.5) + "px";
    // 1. setup the scroller with the bare-bones options
    // 		this will also initialize trigger observations
    // 2. bind scrollama event handlers (this can be chained like below)
    scroller
        .setup({
            step: "#scrolly article .step",
            debug: false,
            offset: midpoint
        })
        .onStepEnter(handleStepEnter)
        .onStepExit(handleStepExit);
}

// kick things off
init();