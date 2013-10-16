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
    $(".os-action .edit").click(function() {
        eid = "#" + $(this).parent().attr("data-id");
        $(eid + " span").hide();
        $(eid + " .edit").hide();
        $(eid + " .remove").hide();
        $(eid + " input").show();
        $(eid + " .save").show();
        $(eid + " .cancle").show();
        return false;
    });

    //save button
    $(".os-action .save").click(function() {
        eid = "#" + $(this).parent().attr("data-id");
        tr = $(eid);
        os_name = $(eid + " input.os_name").val();
        $.ajax({
            type: "POST",
            url: tr.attr("data-edit-url"),
            data: "name=" + os_name,
            dataType: "json",
            success: function(ret){
                if(ret.status) {
                    $(eid + " span.os_name").html(ret.os_name);
                    $(eid + " input.os_name").val(ret.os_name);
                } else {
                    alert("error");
                }

                $(".os-action .cancle").click();
            }
        });

        return false;
    });

    //cancle button
    $(".os-action .cancle").click(function() {
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
    $(".os-action .remove").click(function() {
        return confirm("你确认要删除吗！");
    });
});
