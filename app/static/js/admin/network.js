$(document).ready(function() {
    $("#sunstone_name").typeahead({
        source: function(query, process) {
            objects = [];
            map = {};
            $.ajax({
                url: $("#idc_id option:selected").attr("data-api-url"),
                success: function(ret) {
                    $.each(eval(ret), function(i, object) {
                        map[object.sunstone_name] = object;
                        objects.push(object.sunstone_name);
                    });
                    process(objects);
                }
            });
        },
        updater: function(item) {
            $('#sunstone_id').val(map[item].sunstone_id);
            return item;
        }
    });

    //idc_id change
    $("#idc_id").change(function() {
        $("#sunstone_name").val('');
        $("#sunstone_id").val('');
    });

    //edit button
    $(".net-action .edit").click(function() {
        id = "#" + $(this).parent().attr("data-id");
        $(id + " span").hide();
        $(id + " .edit").hide();
        $(id + " .remove").hide();
        $(id + " input").show();
        $(id + " .save").show();
        $(id + " .cancle").show();
        return false;
    });

    //save button
    $(".net-action .save").click(function() {
        eid = "#" + $(this).parent().attr("data-id");
        tr = $(eid);
        net_name = $(eid + " input.net_name").val();
        $.ajax({
            type: "POST",
            url: tr.attr("data-edit-url"),
            data: "name=" + net_name,
            dataType: "json",
            success: function(ret){
                if(ret.status) {
                    $(eid + " span.net_name").html(ret.net_name);
                    $(eid + " input.net_name").val(ret.net_name);
                } else {
                    alert("error");
                }

                $(".net-action .cancle").click();
            }
        });

        return false;
    });

    //cancle button
    $(".net-action .cancle").click(function() {
        id = "#" + $(this).parent().attr("data-id");
        $(id + " input").hide();
        $(id + " .save").hide();
        $(id + " .cancle").hide();
        $(id + " span").show();
        $(id + " .edit").show();
        $(id + " .remove").show();
        return false;
    });

    //delete button
    $(".net-action .remove").click(function() {
        return confirm("你确认要删除吗！");
    });
});
