$(document).ready(function() {
    $("#disk-slider").slider({
        range: "min",
        value: 50,
        min: 0,
        max: 300,
        step: 50,
        slide: function(event, ui) {
            $("#disk-input").val(ui.value);
        }
    });

    $("#disk-input").val($("#disk-slider").slider("value"));

    $("#disk-input").change(function() {
        $("#disk-slider").slider({ value: $(this).val() });
        $("#disk-input").val($("#disk-slider").slider("value"));
    });
});
