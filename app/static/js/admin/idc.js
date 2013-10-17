$(document).ready(function() {
    //edit button
    $(".action .edit").click(function() {
        trid = "#" + $(this).parent().attr("data-trid");
        $(trid + " span").hide();
        $(trid + " .edit").hide();
        $(trid + " .remove").hide();
        $(trid + " input").show();
        $(trid + " .save").show();
        $(trid + " .cancle").show();
        return false;
    });

    //save button
    $(".action .save").click(function() {
        trid = "#" + $(this).parent().attr("data-trid");
        tr = $(trid);
        name = $(trid + " input.name").val();
        cname = $(trid + " input.cname").val();
        $.ajax({
            type: "POST",
            url: tr.attr("data-edit-url"),
            data: "name="+ name +"&chinese_name="+ cname,
            dataType: "json",
            success: function(ret){
                if(ret.status) {
                    $(trid + " span.name").html(name);
                    $(trid + " span.cname").html(cname);
                    $(trid + " input.name").val(name);
                    $(trid + " input.cname").val(cname);
                    flash(ret.msg, 'success');
                } else {
                    for(m in ret.msg) { flash(ret.msg[m], 'error'); }
                }

                $(".action .cancle").click();
            }
        });

        return false;
    });

    //cancle button
    $(".action .cancle").click(function() {
        trid = "#" + $(this).parent().attr("data-trid");
        $(trid + " input").hide();
        $(trid + " .save").hide();
        $(trid + " .cancle").hide();
        $(trid + " span").show();
        $(trid + " .edit").show();
        $(trid + " .remove").show();
        return false;
    });

    //delete button
    $(".action .remove").click(function() {
        trid = "#" + $(this).parent().attr("data-trid");
        if(confirm("你确认要删除吗！")) {
            $.ajax({});
        }
        return false;
    });
});
