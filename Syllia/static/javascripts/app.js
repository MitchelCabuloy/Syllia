(function() {
    $(document).foundation();

    $("#account-button").click(function() {
        $(".account-pane").toggle();
    });
    $("#h-login-button").click(function() {
        $(".h-login-pane").toggle();
    });
})();
