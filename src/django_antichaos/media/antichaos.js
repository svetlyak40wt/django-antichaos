var stack = [];

function get_tag_id(tag_id)
{
    // cut real tag id from HTML's id
    return tag_id.substring(4, tag_id.length);
}

$(document).ready(function() {
    var history = $('.history');
    var form = $('form.tag-cloud');

    $('.tag').each(function (i, tag) {
        $(tag).simpletip({
            persistent: true,
            position: [$(tag).width(), 0],
            onBeforeShow: function() {
                var tag_id = get_tag_id($(tag).attr('id'));
                var url = 'preview/' + tag_id + '/';
                this.load(url);
            }
        });
    });

    $('.tag').draggable().droppable({
        accept: '.tag',
        activeClass: 'active',
        hoverClass:  'hover',
        drop: function(ev, ui) {
            var from = ui.draggable;
            var to = $(this);

            var from_tag_id = from[0].id;
            from_tag_id = from_tag_id.substring(4, from_tag_id.length);

            var to_tag_id = to[0].id;
            to_tag_id = to_tag_id.substring(4, to_tag_id.length);

            form.append(
                '<input name="changes" type="hidden" value="' +
                'merge ' + to_tag_id + ' ' + from_tag_id + '" />');

            stack[stack.length] = {
                action: 'merge',
                from: from_tag_id,
                to:     to_tag_id,
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
            $('form.tag-cloud input[disabled]').attr('disabled', false);
        },
    });
});
