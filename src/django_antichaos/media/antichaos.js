$(document).ready(function() {
    $('.tag').draggable().droppable({
        accept: '.tag',
        activeClass: 'active',
        hoverClass:  'hover',
    });
});
