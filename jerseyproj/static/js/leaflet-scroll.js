import { updateMap } from './leaflet.js';
import { clearMap } from './leaflet.js';

var scrolly = document.querySelector("#scrolly");
var article = scrolly.querySelector("article");
// initialize the scrollama
var scroller = scrollama();
var step;

// scrollama event handlers
function handleStepEnter(response) {
    // response = { element, direction, index }
    // console.log(response.element);
    var step = $(response.element).find('.carousel-cell.is-selected').find('.step')[0]
    console.log(step)
    if (step.hasAttribute("value")) {
        mapContainers[step.getAttribute("value")].appendChild(mapObject);
        updateMap(step.getAttribute("value"), step.getAttribute("map"));
    }
    // add to color to current step
    step.classList.add("is-active");
}

function handleStepExit(response) {
    // response = { element, direction, index }
    console.log("scrollama-exit")
    // remove color from current step
    clearMap();
    step.classList.remove("is-active");
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
            step: "#scrolly article .carousel",
            debug: false,
            offset: midpoint
        })
        .onStepEnter(handleStepEnter)
        .onStepExit(handleStepExit);
}

// kick things off
init();