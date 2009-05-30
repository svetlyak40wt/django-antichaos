var stack = [];

$(document).ready(function() {
    var history = $('.history');

    $('.tag').draggable().droppable({
        accept: '.tag',
        activeClass: 'active',
        hoverClass:  'hover',
        drop: function(ev, ui) {
            stack[stack.length] = {
                action: 'merge',
                from: ui.draggable[0].id,
                to: $(this)[0].id
            };
            history.append(
                $('<li>' + ui.draggable.html() + '->' + $(this).html() + '</li>')
            );
            ui.draggable.effect('explode');
        },
    });
});
