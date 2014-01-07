$(document).ready(function() {
    //Refresh
    $('body').on('click', '#vm_refresh', function() {
        e = $(this);
        origin = e.html();
        e.html("loading");
        $.ajax({
            url: e.attr("href"),
            success: function(ret) {
                e.html(origin);
                $("#myModal .modal-body").html(ret);
                $(".nav-tabs a[href='"+ $("#tabs_active").html() +"']").click();
            }
        });
        return false;
    });

    $('body').on('click', '.nav-tabs a[data-toggle="tab"]', function() {
        tab = $(this).attr("href");
        if(tab != "refresh") { $("#tabs_active").html(tab); }
    });


    //Basic information
    $('body').on('click', ".basic_action .edit", function() {
        e = $(this).parent();
        e.children("span").hide();
        e.children(".edit").hide();
        e.children(".detail").hide();
        e.children("input:text").show();
        e.children(".save").show();
        e.children(".cancle").show();
        return false;
    });

    $('body').on('keypress', ".basic_action input", function(event) {
        e = $(this).parent();
        var code = event.keyCode || event.which;
        if(code == 13) {
            e.children(".save").click();
        }
    });

    $('body').on('click', ".basic_action .save", function() {
        e = $(this).parent();
        api = $(this).attr("href");
        data = e.children("input").val();
        $.ajax({
            type: "POST",
            url: api,
            data: "data=" + data,
            dataType: "json",
            success: function(ret) {
               if(ret.status) {
                    e.children("span").html(data);
                    e.children("input").val(data);
                    flash("修改成功", 'success');
                } else {
                    flash("修改失败", 'error');
                }

                e.children(".cancle").click();
            }
        });

        return false;
    });

    $('body').on('click', ".basic_action .cancle", function() {
        e = $(this).parent();
        e.children("input:text").hide();
        e.children(".save").hide();
        e.children(".cancle").hide();
        e.children("span").show();
        e.children(".edit").show();
        e.children(".detail").show();
        return false;
    });


    //CPU Memory option
    $('body').on('change', '#cpu_select', function() {
        mem_init();
    });

    function mem_init() {
        $("#mem_select").html("");
        $.ajax({
            url: $("#mem_select").attr("data-api") + "?cpu=" + $("#cpu_select").val(),
            async: false,
            success: function(ret) {
                ret = eval(ret);
                for(x in ret) {
                    $("#mem_select").append('<option value="'+ ret[x] +'">'+ ret[x] +'G</option>');
                }
            }
        });
    }

    $('body').on('click', '#resize_btn', function() {
        api = $("#resize").attr("action");
        cpu = $("#cpu_select").val();
        mem = $("#mem_select").val();
        $.ajax({
            type: "POST",
            url: api,
            data: "cpu="+ cpu +"&mem="+ mem,
            dataType: "json",
            success: function(ret) {
                if(ret.status) {
                    $("#vm_refresh").click();
                } else {
                    flash("修改失败", 'error');
                }
            }
        });
    });


    //Network
    $('body').on('click', '#nic_attach_btn', function() {
        e = $(this);
        e.prop('disabled', true);
        api = $("#nic_attach").attr("action");
        network_id = $("#nic_select").val();
        $.ajax({
            type: "POST",
            url: api,
            data: "network_id=" + network_id,
            success: function(ret) {
                if(ret.status) {
                    $("#vm_refresh").click();
                } else {
                    flash("添加失败", 'error');
                }
            }
        });
    });

    $('body').on('click', ".nic_dettach", function() {
        if(!confirm("你确定要detach网卡吗？")) {
            return false;
        }

        api = $(this).attr("href");
        nic_id = $(this).attr("data-nicid");
        $.ajax({
            type: "POST",
            url: api,
            data: "nic_id=" + nic_id,
            success: function(ret) {
                if(ret.status) {
                    $("#vm_refresh").click();
                } else {
                    flash("操作失败", 'error');
                }
            }
        });
        return false;
    });
});
