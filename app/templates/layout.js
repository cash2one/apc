function flash(message, category) {
    $.globalMessenger().post({
        message: message,
        type: category,
        showCloseButton: true
    });
}
