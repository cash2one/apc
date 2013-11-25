$(document).ready(function() {
    $(".action .delete").click(function() {
        if(!confirm("你确认要删除吗！")) {
            return false;
        }

        e = $(this);

        $.ajax({
            type: "POST",
            url: e.attr("href"),
            dataType: "json",
            success: function(ret) {
                if(ret.status) {
                    flash(ret.msg, 'success');
                    e.parent().parent().remove();
                } else {
                    flash(ret.msg, 'error');
                }
            }
        });

        return false; 
    });
});
