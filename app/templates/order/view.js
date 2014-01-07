$(document).ready(function() {
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
        api = $(this).attr('href');
        hostname = $(trid + " input.hostname").val();
        $.ajax({
            type: "POST",
            url: api,
            data: "hostname="+ hostname,
            dataType: "json",
            success: function(ret){
                if(ret.status) {
                    $(trid + " span.hostname").html(hostname);
                    $(trid + " input.hostname").val(hostname);
                    flash("修改成功", 'success');
                } else {
                    flash("修改失败", 'error');
                }

                $(trid + " .cancle").click();
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


    $(".action .remove").click(function() {
        if(!confirm("你确定要删除吗？")) {
            return false;
        }

        e = $(this);
        $.ajax({
            type: 'POST',
            url: e.attr('href'),
            dataType: 'json',
            success: function(ret) {
                if(ret.status) {
                    e.parent().parent().remove();
                } else {
                    flash("删除失败", 'error');
                }
            }
        });
        return false;
    });


    //Edit state
    $("#order-state .edit").click(function() {
        $("#order-state span").hide();
        $("#order-state a.edit").hide();
        $("#order-state select").show();
        $("#order-state a.save").show();
        $("#order-state a.cancle").show();
        return false;
    });

    $("#order-state .cancle").click(function() {
        $("#order-state select").hide();
        $("#order-state a.save").hide();
        $("#order-state a.cancle").hide();
        $("#order-state span").show();
        $("#order-state a.edit").show();
        return false;
    });

    $("#order-state .save").click(function() {
        url = $(this).attr('data-api') + "?state=" + $("#order-state select").val();
        window.location.href = url;
    });
});
