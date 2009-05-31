var stack = [];
var tip;

function get_tag_id(tag_id)
{
    // cut real tag id from HTML's id
    return tag_id.substring(4, tag_id.length);
}

$(document).ready(function() {
    var history = $('.history');
    var changes_form = $('form.tag-cloud');
    var tooltips_cache = {};
    var tooltip_timer;

    $('.tag').each(function (i, tag) {
        $(tag).simpletip({
            content: '',
            position: [$(tag).width(), 0],
            onBeforeShow: function() {
                var tooltip = this;

                tooltip_timer = setTimeout(function() {
                    var tag_id = get_tag_id($(tag).attr('id'));
                    if (tooltips_cache[tag_id]) {
                        this.update(tooltips_cache[tag_id]);
                    } else {
                        var url = 'preview/' + tag_id + '/';
                        $.get(url, function(data) {
                            tooltips_cache[tag_id] = data;
                            tooltip.update(data);
                        });
                    }
                }, 3000);
            },
            onHide: function() {
                clearTimeout(tooltip_timer);
            }
        });

        $(tag).dblclick(function() {
            clearTimeout(tooltip_timer);

            var old_value = $(tag).find('span').html();
            var form = $('<form><input name="text" type="text" value="' + old_value + '" /></form>');
            form.find('input').width($(tag).find('span').width());

            form.submit(function(evt) {
                var new_value = form[0].text.value;
                $(tag).find('span').show();
                form.remove();

                if (new_value != old_value) {
                    // start history update
                    // TODO refactor this code duplication!
                    var tag_id = get_tag_id(tag.id);
                    changes_form.append(
                        '<input name="changes" type="hidden" value="' +
                        'rename|' + tag_id + '|' + new_value + '" />');

                    stack[stack.length] = {
                        action: 'rename',
                        tag_id: tag_id,
                        new_value: new_value,
                    };
                    history.append(
                        $('<li>' + old_value + ' -> ' + new_value + '</li>')
                    );
                    $('form.tag-cloud input[disabled]').attr('disabled', false);
                    // end history update

                    $(tag).find('span').html(new_value);
                }
                evt.preventDefault();
            });

            $(tag).find('span').hide();
            $(tag).prepend(form);
            form.find('input').focus();
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

            // end history update
            changes_form.append(
                '<input name="changes" type="hidden" value="' +
                'merge|' + to_tag_id + '|' + from_tag_id + '" />');

            stack[stack.length] = {
                action: 'merge',
                from: from_tag_id,
                to:     to_tag_id,
            };
            history.append(
                $('<li>' + to.html() + ' = ' + from.html() + '</li>')
            );
            $('form.tag-cloud input[disabled]').attr('disabled', false);
            // end history update

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
