var Antichaos = {
    tag_cloud_id: 'ul.tag-cloud',
    cloud_json_url: '?json',
    font_size_from: 1,
    font_size_to: 4,
    stack: [],
    more_click: false,
    tooltip_timer: undefined,
    num_previews: 5
};

function get_tag_id(tag_id)
{
    // cut real tag id from HTML's id
    return tag_id.substring(4, tag_id.length);
}

function stop_timer()
{
    clearTimeout(Antichaos.tooltip_timer);
    Antichaos.tooltip_timer = undefined;
}

function update_tooltip(tooltip, data)
{
    var div = $(data);
    div.find('a.more').click( function(evt) {
        evt.preventDefault();
        Antichaos.more_click = true;
        stop_timer();
        $.get(this, function(data) {
            update_tooltip(tooltip, data);
        });
    });
    tooltip.update(div);
}

function init_antichaos(params)
{
    Antichaos.num_previews = params.top;
    Antichaos.cloud_json_url = params.cloud_json_url;
}

function get_tag_size(count) {
    count = Math.log(count) * Antichaos.max_count / Math.log(Antichaos.max_count);
    return Antichaos.font_size_from + (Antichaos.font_size_to - Antichaos.font_size_from) * count / Antichaos.max_count;
}

function create_tags(data) {
    var max = 0;
    var min = 65535;
    $.each(data.objects, function(i, tag) {
        var cnt = tag.count;
        max = cnt > max ? cnt : max;
        min = cnt < min ? cnt : min;
    });
    Antichaos.max_count = max;
    Antichaos.min_count = min;

    var cloud = $(Antichaos.tag_cloud_id);
    $.each(data.objects, function(i, tag) {
        var size = get_tag_size(tag.count);
        cloud.append('<li id="tag_' + tag.id + '" class="tag" style="font-size: ' + size + 'em"><span>' + tag.name + '</span><sup>' + tag.count + '</sup></li> ');
    });
}

function make_tags_draggable()
{
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
            Antichaos.changes_form.append(
                '<input name="changes" type="hidden" value="' +
                'merge|' + to_tag_id + '|' + from_tag_id + '" />');

            Antichaos.stack[Antichaos.stack.length] = {
                action: 'merge',
                from: from_tag_id,
                to:     to_tag_id
            };
            Antichaos.history.append(
                $('<li>' + to.find('span').html() + ' = ' + from.find('span').html() + '</li>')
            );
            $('form.tag-cloud input[disabled]').attr('disabled', false);
            // end history update

            var from_count = eval(from.find('sup').html());
            var from_size = from.css('font-size');
            from_size = eval(from_size.substring(0, from_size.length - 2));

            var to_count   = eval(to.find('sup').html());
            var to_size = to.css('font-size');
            to_size = eval(to_size.substring(0, to_size.length - 2));

            var new_size = get_tag_size(to_count + from_count);

            to.find('sup').html(to_count + from_count);
            to.animate({
                fontSize: new_size + 'em',
            });

            ui.draggable.effect('explode');
        }
    });
}

function add_tooltips()
{
    Antichaos.tooltips_cache = {};

    $('.tag').each(function (i, tag) {
        $(tag).simpletip({
            content: '',
            position: [$(tag).width(), 0],
            onBeforeShow: function() {
                var tooltip = this;
                var tag_id = get_tag_id($(tag).attr('id'));

                if (Antichaos.tooltips_cache[tag_id]) {
                    if (Antichaos.more_click == true) {
                        Antichaos.more_click = false;
                    } else {
                        update_tooltip(tooltip, Antichaos.tooltips_cache[tag_id]);
                    }
                } else {
                    Antichaos.tooltip_timer = setTimeout(function() {
                            var url = 'preview/' + tag_id + '/?top=' + Antichaos.num_previews;
                            $.get(url, function(data) {
                                Antichaos.tooltips_cache[tag_id] = data;
                                update_tooltip(tooltip, data);
                            });
                    }, 3000);
                }
            },
            onHide: function() {
                stop_timer();
            }
        });
    });
}

function make_tags_editable()
{
    $('.tag').each(function (i, tag) {
        $(tag).dblclick(function() {
            stop_timer();

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
                    Antichaos.changes_form.append(
                        '<input name="changes" type="hidden" value="' +
                        'rename|' + tag_id + '|' + new_value + '" />');

                    Antichaos.stack[Antichaos.stack.length] = {
                        action: 'rename',
                        tag_id: tag_id,
                        new_value: new_value
                    };
                    Antichaos.history.append(
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
}

function create_tag_cloud()
{
    $.getJSON(
        Antichaos.cloud_json_url,
        function(data) {
            create_tags(data);
            make_tags_draggable();
            add_tooltips();
            make_tags_editable();
        }
    )
}

$(document).ready(function() {
    Antichaos.history = $('.history');
    Antichaos.changes_form = $('form.tag-cloud');
    create_tag_cloud();
});
