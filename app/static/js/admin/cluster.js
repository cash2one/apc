$(document).ready(function() {
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
