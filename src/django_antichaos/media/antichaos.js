var stack = [];

$(document).ready(function() {
    var history = $('.history');

    $('.tag').draggable().droppable({
        accept: '.tag',
        activeClass: 'active',
        hoverClass:  'hover',
        drop: function(ev, ui) {
            var from = ui.draggable;
            var to = $(this)
            stack[stack.length] = {
                action: 'merge',
                from: from[0].id,
                to:     to[0].id,
            };
            history.append(
                $('<li>' + from.html() + '->' + to.html() + '</li>')
            );
            ui.draggable.effect('explode');
        },
    });
});
