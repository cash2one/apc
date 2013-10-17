$(document).ready(function() {
    //edit button
    $(".cpumem-action .edit").click(function() {
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
    $(".cpumem-action .save").click(function() {
        eid = "#" + $(this).parent().attr("data-id");
        tr = $(eid);
        cpu = $(eid + " input.cpu").val();
        mem = $(eid + " input.mem").val();
        $.ajax({
            type: "POST",
            url: tr.attr("data-edit-url"),
            data: "cpu="+ cpu +"&mem="+ mem,
            dataType: "json",
            success: function(ret){
                if(ret.status) {
                    $(eid + " span.cpu").html(cpu);
                    $(eid + " span.mem").html(mem);
                    $(eid + " input.cpu").val(cpu);
                    $(eid + " input.mem").val(mem);
                    flash(ret.msg, 'success');
                } else {
                    for(m in ret.msg) { flash(ret.msg[m], 'error'); }
                }

                $(".cpumem-action .cancle").click();
            }
        });

        return false;
    });

    //cancle button
    $(".cpumem-action .cancle").click(function() {
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
    $(".cpumem-action .remove").click(function() {
        return confirm("你确认要删除吗！");
    });
});
