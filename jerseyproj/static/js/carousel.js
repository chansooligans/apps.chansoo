var $carousel = $('.main-carousel');

$carousel.on('change.flickity', function (event, index) {
    var steps = $(this).find('.step');
    var stepsArray = [];
    steps.each(function () {
        stepsArray.push(this);
    });
    console.log(stepsArray[index].getAttribute("value"))
});