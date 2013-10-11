$(document).ready(function() {
    //network select
    function update_select(ele, data, idc_id) {
        $(ele).html("");

        for(var i in data) {
            if(data[i].idc_id==idc_id) {
                html = '<option value="'+ data[i].sunstone_id +'">'+ data[i].sunstone_name +'</option>';
                $(ele).append(html);
            }
        }
    }

    update_select($("#sunstone_id"), vnet_sunstone, $("#idc_id").val());
    $("#sunstone_name").val($("#sunstone_id option:selected").text());

    $("#idc_id").change(function() {
        update_select($("#sunstone_id"), vnet_sunstone, $(this).val());
    });

    $("#sunstone_id").change(function() {
        $("#sunstone_name").val($(this).children("option:selected").text());
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
