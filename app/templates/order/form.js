$(document).ready(function() {
    init = true;

    //cpu
    $(".btn-cpu").click(function(){
        btn = $(this);
        $(".btn-cpu").removeClass('active');
        btn.addClass('active');
        $("#cpu").val(btn.attr('value'));

        $.ajax({
            url: btn.attr('data-mem-api') + "?cpu=" + $("#cpu").val(),
            dataType: "json",
            async: false,
            success: function(ret) {
                $("#group-mem .controls").html('');
                template = $("#mem-template").html();
                for(i in eval(ret)) {
                    html = template.replace(/\{mem\}/g, ret[i]);
                    $("#group-mem .controls").append(html);
                }
                $(".btn-mem:first-child").click();
            }
        });
    });


    //mem
    $('#group-mem').on('click', '.btn-mem', function() {
        btn = $(this);
        $(".btn-mem").removeClass('active');
        btn.addClass('active');
        if(!init) { $("#mem").val(btn.attr('value')); }
        price_calc();
    });


    //disk
    function disk_update() {
        disk_arr = [];
        $("#disk-label span").each(function(i) {
            disk_arr.push($(this).attr('value'));
        });
        $("#disk").val(disk_arr);
        price_calc();
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
            async: false,
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
        price_calc();
    }

    $("#nic-add-btn").click(function() {
        html = $("#nic-label-template").html();
        html = html.replace(/\{value\}/g, $("#nic-option").val())
        html = html.replace(/\{label\}/g, $("#nic-option option:selected").html())
        $("#nic-label").append(html);
        if(!init) { nic_update(); }
    });

    $("#nic-label").on('click', '.close', function() {
        $(this).parent().remove();
        nic_update();
    });


    //os image
    function osimage_init() {
        api = $("#os_id").attr('data-api');
        api = api + "?cluster_id=" + $("#cluster_id").val();
        $.ajax({
            url: api,
            async: false,
            success: function(ret) {
                ret = eval(ret)
                $("#os_id").html('');
                template = $("#os-template").html();
                for(i in ret) {
                    html = template.replace(/\{value\}/g, ret[i].id).replace(/\{label\}/g, ret[i].name);
                    $("#os_id").append(html);
                }
            }
        });
    }


    function days_init() {
        $.ajax({
            url: "/api/cluster/" + $("#cluster_id").val(),
            dataType: "json",
            success: function(ret) {
                if(ret.if_test) {
                    $("#days").parent().parent().show();
                }
            }
        });
    }

    //cluster
    $("#cluster_id").change(function() {
        $("#network").val("");
        $("#nic-label").html("");
        $("#disk").val("");
        $("#disk-label").html("");
        nic_init();
        osimage_init();
        days_init();
    });


    //price calc
    function price_calc() {
        cpu = $("#cpu").val();
        mem = $("#mem").val();
        nic = $("#network").val();
        nicnum = (nic=="") ? 0 : nic.split(',').length;
        disk = $("#disk").val();
        disk_arr = (disk=="") ? [] : disk.split(',')

        result = price.base;
        result += cpu*price.cpu + mem*price.mem + nicnum*price.nic;
        for(x in disk_arr) {
            result += price.disk * disk_arr[x];
        }
        $("#price").html(result);
    }

    //init action
    nic_init();
    osimage_init();
    days_init();

    if(edit) {
        cpu = $("#cpu").val();
        mem = $("#mem").val();
        $(".btn-cpu[value='"+ cpu +"']").click();
        $(".btn-mem[value='"+ mem +"']").click();
        disk_arr = $("#disk").val().split(',');
        if(disk_arr[0] != '') {
            for(a in disk_arr) {
                html = $("#disk-label-template").html().replace(/{disksize}/g, disk_arr[a]);
                $("#disk-label").append(html);
            }
        }
        nic_arr = $("#network").val().split(',');
        if(nic_arr[0] != '') {
            for(a in nic_arr) {
                $("#nic-option option[value='" + nic_arr[a] +"']").attr("selected","selected");
                $("#nic-add-btn").click();
            }
        }
        $("#os_id option[value='" + $("#osid-pre").val() + "']").attr("selected","selected");
        $("#disk-input").val($("#disk-slider").slider("value"));
        price_calc();
        init = false;
    } else {
        init = false;
        $(".btn-cpu:first-child").click();
        $(".btn-mem:first-child").click();
        $("#disk-input").val($("#disk-slider").slider("value"));
        price_calc();
    }
});
