function flash(message, category) {
    $.globalMessenger().post({
        message: message,
        type: category,
        showCloseButton: true
    });
}

$(document).ready(function() {
    $(".table-hover tbody tr").hover(
        function () {
            $(this).addClass("hover");
        },
        function () {
            $(this).removeClass("hover");
        }
    );

    $("table input[type='checkbox']").css({"margin-top":"0"});
});
