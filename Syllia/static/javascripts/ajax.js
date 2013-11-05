var AjaxModule = (function($) {
    var MODULE = {};

    MODULE.init = function() {
        var csrftoken = $.cookie('csrftoken');
        $.ajaxSettings.beforeSend = function(xhr, settings) {
            if (!MODULE.csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        };
    };

    MODULE.csrfSafeMethod = function(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    };

    return MODULE;
})(Zepto);

$(document).ready(function() {
    AjaxModule.init();
});