$(function() {
    var timer = null;
    var xhr = null;
    $('.user_popup').hover(
        function(event) {
            // обработчик события mouse in
            var elem = $(event.currentTarget);
            timer = setTimeout(function() {
                timer = null;
                xhr = $.ajax(
                    '/user/' + elem.attr("id") + '/popup').done(
                        function(data) {
                            xhr = null
                            elem.popover({
                                    trigger: 'manual',
                                    html: true,
                                    animation: false,
                                    container: elem,
                                    content: data
                                }).popover('show');
                                flask_moment_render_all();                        }
                    );
            }, 1000);
        },
        function(event) {
            // обработчик события mouse out
            var elem = $(event.currentTarget);
            if (timer) {
                clearTimeout(timer);
                timer = null;
            }
            else if (xhr) {
                xhr.abort();
                xhr = null;
            }
            else {
		    elem.popover('hide');
            }
        }
    )
});