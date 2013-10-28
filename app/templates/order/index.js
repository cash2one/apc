$(document).ready(function() {
    //cpu
    $(".btn-cpu").click(function(){
        btn = $(this);
        $(".btn-cpu").removeClass('active');
        btn.addClass('active');
        $("#cpu").val(btn.attr('value'));

        $("#group-mem .controls").html('');
        $.ajax({
            url: btn.attr('data-mem-api') + "?cpu=" + $("#cpu").val(),
            dataType: "json",
            success: function(ret) {
                template = $("#mem-template").html();
                for(i in eval(ret)) {
                    html = template.replace(/\{mem\}/g, ret[i]);
                    $("#group-mem .controls").append(html);
                }
                $(".controls .btn-mem:first-child").click();
            }
        });
    });


    //mem
    $('#group-mem').on('click', '.btn-mem', function() {
        btn = $(this);
        $(".btn-mem").removeClass('active');
        btn.addClass('active');
        $("#mem").val(btn.attr('value'));
    });


    //disk
    function disk_update() {
        disk_arr = [];
        $("#disk-label span").each(function(i) {
            disk_arr.push($(this).attr('value'));
        });
        $("#disk").val(disk_arr);
    }

    $("#disk-slider").slider({
        range: "min",
        value: 50,
        min: 10,
        max: 500,
        step: 10,
        slide: function(event, ui) {
            $("#disk-input").val(ui.value);
        }
    });

    $("#disk-input").change(function() {
        $("#disk-slider").slider({ value: $(this).val() });
        $("#disk-input").val($("#disk-slider").slider("value"));
    });

    $("#disk-add-btn").click(function() {
        template = $("#disk-label-template").html();
        html = template.replace(/{disksize}/g, $("#disk-input").val());
        $("#disk-label").append(html);
        disk_update();
    });

    $("#disk-label").on('click', '.close', function() {
        $(this).parent().remove();
        disk_update();
    });


    //network
    function nic_init() {
        api = $("#nic-option").attr('data-api');
        api = api + "?cluster_id=" + $("#cluster_id").val();
        $.ajax({
            url: api,
            success: function(ret) {
                ret = eval(ret)
                $("#nic-option").html('');
                template = $("#nic-template").html();
                for(i in ret) {
                    html = template.replace(/\{value\}/g, ret[i].id).replace(/\{label\}/g, ret[i].name);
                    $("#nic-option").append(html);
                }
            }
        });
    }

    function nic_update() {
        nic_arr = [];
        $("#nic-label span").each(function(i) {
            nic_arr.push($(this).attr('value'));
        });
        $("#network").val(nic_arr);
    }

    $("#nic-add-btn").click(function() {
        html = $("#nic-label-template").html();
        html = html.replace(/\{value\}/g, $("#nic-option").val())
        html = html.replace(/\{label\}/g, $("#nic-option option:selected").html())
        $("#nic-label").append(html);
        nic_update();
    });

    $("#nic-label").on('click', '.close', function() {
        $(this).parent().remove();
        nic_update();
    });


    //os image
    function osimage_init() {
        api = $("#os-id").attr('data-api');
        api = api + "?cluster_id=" + $("#cluster_id").val();
        $.ajax({
            url: api,
            success: function(ret) {
                ret = eval(ret)
                $("#os-id").html('');
                template = $("#os-template").html();
                for(i in ret) {
                    html = template.replace(/\{value\}/g, ret[i].id).replace(/\{label\}/g, ret[i].name);
                    $("#os-id").append(html);
                }
            }
        });
    }


    //cluster
    $("#cluster_id").change(function() {
        nic_init();
        osimage_init();
    });


    //init action
    nic_init();
    osimage_init();
    $(".btn-cpu:first-child").click();
    $("#disk-input").val($("#disk-slider").slider("value"));
});
