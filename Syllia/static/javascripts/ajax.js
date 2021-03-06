var AjaxModule = (function($) {
    var MODULE = {};

    MODULE.init = function() {
        var csrftoken = $.cookie('csrftoken');

        $(document).on('ajaxBeforeSend', function(e, xhr, options) {
            if (!MODULE.csrfSafeMethod(options.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }

            $('#saveBtn').toggle();
            $('#savingBtn').toggle();
        });

        $(document).on('ajaxSuccess', function(e, xhr, options) {
            $('#savingBtn').toggle();
            $('#savedBtn').toggle();
            setTimeout(function() {
                $('#savedBtn').toggle();
                $('#saveBtn').toggle();
            }, 5000);
        });

        $(document).on('ajaxError', function(e, xhr, options) {
            error = $.parseJSON(xhr.response);
            $('#savingBtn').toggle();
            $('#errorBtn').toggle();
            $('#sectionErrors').show();
            $('ul.messages').append($('<li></li>').attr('class', 'error').text(error.message));

            setTimeout(function() {
                $('#errorBtn').toggle();
                $('ul.messages').empty();
                $('#sectionErrors').hide();
                $('#saveBtn').toggle();
            }, 5000);
        });
    };

    MODULE.csrfSafeMethod = function(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    };

    return MODULE;
})(jQuery);

$(document).ready(function() {
    AjaxModule.init();
});
