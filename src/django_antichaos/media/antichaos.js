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
                $('<li>' + to.html() + ' = ' + from.html() + '</li>')
            );
            var from_count = eval(from.find('sup').html());
            var from_size = from.css('font-size');
            from_size = eval(from_size.substring(0, from_size.length - 2));

            var to_count   = eval(to.find('sup').html());
            var to_size = to.css('font-size');
            to_size = eval(to_size.substring(0, to_size.length - 2));

            // TODO add real new size calculation, based on relative counts
            var new_size =  to_size + from_size / (to_size/to_count + from_size/from_count);

            to.find('sup').html(to_count + from_count);
            to.animate({
                fontSize: '+=0.25em',
            });

            ui.draggable.effect('explode');
        },
    });
});
