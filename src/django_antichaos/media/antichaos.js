var Antichaos = {
    tag_cloud_selector: 'ul.tag-cloud',
    history_selector: 'ul.history',
    form_selector: 'form.tag-cloud',
    undo_selector: 'input.undo',
    cloud_json_url: '?json=1',
    font_size_from: 1,
    font_size_to: 4,
    stack: [],
    more_click: false,
    tooltip_timer: undefined,
    num_previews: 5,
    stack_position: 0,
    on_cloud_load_start: function(){},
    on_cloud_load_end: function(){}
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
    Antichaos = $.extend(Antichaos, params)
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

    var cloud = $(Antichaos.tag_cloud_selector);
    $.each(data.objects, function(i, tag) {
        var size = get_tag_size(tag.count);
        cloud.append('<li id="tag_' + tag.id + '" class="tag" style="font-size: ' + size + 'em"><span>' + tag.name + '</span><sup>' + tag.count + '</sup></li> ');
    });
}

function push_stack(params)
{
    var form_item = '<input name="changes" type="hidden" value="';

    $.each(params.data, function(key, value) {
        form_item += key + '=' + value + ','
    });
    form_item += '" />';
    form_item = $(form_item);

    var history_item = $('<li>' + params.message + '</li>');

    params.data.history_item = history_item;
    params.data.form_item = form_item;
    params.data.undo = params.undo;

    Antichaos.stack[Antichaos.stack_position++] = params.data;
    Antichaos.history.append(history_item);
    Antichaos.changes_form.append(form_item);
    $('form.tag-cloud input[disabled]').attr('disabled', false);
}

function pop_stack()
{
    var stack_item = Antichaos.stack[--Antichaos.stack_position];
    stack_item.undo(stack_item);
    delete Antichaos.stack[Antichaos.stack_position];
    if (Antichaos.stack_position == 0) {
        $('form.tag-cloud input').attr('disabled', true);
    }
}

function init_undo_button()
{
    $(Antichaos.undo_selector).click(function(evt) {
        evt.preventDefault();
        pop_stack();
    });
}

function base_item_undo(item)
{
    item.history_item.remove();
    item.form_item.remove();
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

            push_stack({
                data: {
                    action: 'merge',
                    from_tag:   from_tag_id,
                    to_tag:     to_tag_id,
                },
                message: to.find('span').html() + ' = ' + from.find('span').html(),
                undo: function(item) {
                    base_item_undo(item);

                    to.find('sup').html(to_count);
                    to.animate({
                        fontSize: get_tag_size(to_count) + 'em',
                    });

                    ui.draggable.show().css('opacity', 0).animate({
                        opacity: 1,
                        left: 0,
                        top: 0
                    });
                }
            });
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
                    push_stack({
                        data: {
                            action:    'rename',
                            tag_id:    get_tag_id(tag.id),
                            new_value: new_value
                        },
                        message: old_value + ' -> ' + new_value,
                        undo: function(item) {
                            base_item_undo(item);
                            $(tag).find('span').html(old_value);
                        }
                    });

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
    Antichaos.history = $(Antichaos.history_selector);
    Antichaos.changes_form = $(Antichaos.form_selector);
    Antichaos.on_cloud_load_start();

    $.getJSON(
        Antichaos.cloud_json_url,
        function(data) {
            create_tags(data);
            make_tags_draggable();
            add_tooltips();
            make_tags_editable();
            init_undo_button();
            Antichaos.on_cloud_load_end();
        }
    )
}

$(document).ready(function() {
    var actions = $('#recent-actions-module');
    var chaos_bin = $('<ul id="chaos-bin"></ul>')
        .css('height', '200px')
        .css('overflow', 'hidden')
        .droppable({
            accept: '.tag',
            activeClass: 'active',
            hoverClass:  'hover',
            drop: function(ev, ui) {
                var obj = $(ui.draggable);
                obj
                    .css('top', 'auto')
                    .css('left', 'auto')
                    .css('margin-bottom', '0.5em')
                    .css('list-style', 'none');
                $(this).append(obj);
            }
        }
    );

    actions
        .css('position', 'relative')
        .css('width', '500px');
    actions.find('h2').after(chaos_bin);

    var actions_initial_x = actions.position().top;

    $(window).scroll(function (ev) {
        actions.css('top', $(window).scrollTop());
    });

    create_tag_cloud();
});
