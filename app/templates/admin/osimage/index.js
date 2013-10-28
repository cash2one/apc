$(document).ready(function() {
    $("#sunstone_name").typeahead({
        source: function(query, process) {
            objects = [];
            map = {};
            $.ajax({
                url: $("#cluster_id option:selected").attr("data-api-url"),
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

    //cluster_id change
    $("#cluster_id").change(function() {
        $("#sunstone_name").val('');
        $("#sunstone_id").val('');
    });

    //edit button
    $(".action .edit").click(function() {
        eid = "#" + $(this).parent().attr("data-trid");
        $(eid + " span").hide();
        $(eid + " .edit").hide();
        $(eid + " .remove").hide();
        $(eid + " input").show();
        $(eid + " .save").show();
        $(eid + " .cancle").show();
        return false;
    });

    //save button
    $(".action .save").click(function() {
        eid = "#" + $(this).parent().attr("data-trid");
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
                    flash(ret.msg, 'success')
                } else {
                    flash(ret.msg, 'error')
                }

                $(".action .cancle").click();
            }
        });

        return false;
    });

    //cancle button
    $(".action .cancle").click(function() {
        id = "#" + $(this).parent().attr("data-trid");
        $(id + " input").hide();
        $(id + " .save").hide();
        $(id + " .cancle").hide();
        $(id + " span").show();
        $(id + " .edit").show();
        $(id + " .remove").show();
        return false;
    });


    //delete button
    $(".action .remove").click(function() {
        if(!confirm("你确认要删除吗！")) {
            return false;
        }

        trid = "#" + $(this).parent().attr("data-trid");
        $.ajax({
            type: "POST",
            url: $(trid + " .remove").attr("href"),
            dataType: "json",
            success: function(ret) {
                if(ret.status) {
                    flash(ret.msg, 'success');
                    $(trid).remove();
                } else {
                    flash(ret.msg, 'error');
                }
            }
        });
        return false;
    });
});
