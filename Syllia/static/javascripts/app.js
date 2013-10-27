(function() {
    $(document).foundation();

    $("#account-button").click(function() {
        $(".account-pane").toggle();
    });
    $("#login-button").click(function() {
        $(".login-pane").toggle();
    });
})();
