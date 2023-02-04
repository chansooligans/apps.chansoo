const carouselCells = document.querySelectorAll('.carousel-cell');

carouselCells.forEach(function (cell) {
    cell.classList.append('testing')
    cell.addEventListener('change', function () {
        console.log(1)
        if (cell.classList.contains('is-selected')) {
            // run function when "is-selected" is added
            console.log("added")
            console.log(selectedCell)
        } else {
            // run function when "is-selected" is removed
            console.log("removed")
            console.log(selectedCell)
        }
    });
});