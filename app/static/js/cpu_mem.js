$(document).ready(function() {
    $("#addForm .btn-primary").click(
        function() {
            cpu = $("#add_cpu").val();
            mem = $("#add_mem").val();
            $.post(
                "/admin/cpu_mem/add/",
                {"cpu":cpu, "mem":mem},
                function(res){
                    if(res["id"]) {
                        new_row = '<div class="row-fluid table-row"> <div class="span3"><em>'+res["id"]+'</em></div> <div class="span4"><font color="#009900">'+cpu+'</font></div> <div class="span3"><font color="#009900">'+mem+'</font></div> </div> ';
                        $(".row-fluid:last").after(new_row);
                        sort_table();
                        $("#add_cpu").val("");
                        $("#add_mem").val("");
                    } else {
                        $("#message").html('<div class="alert alert-error"><button class="close" data-dismiss="alert">&times;</button>'+res["msg"]+'</div>');
                        $("#message").show().delay(3000);
                        $("#message").slideUp('slow');
                    }
                },
                "json"
                );
        }
);

$(this).on("mouseenter",".table-row",function(){
    if($(this).has("input")[0]) {
        return;
    }
    $(this).append(' <div class="span2"><a href="javascript:void(0)"><i class="icon-edit icon-large"></i></a>&nbsp;&nbsp;&nbsp;&nbsp;<a href="javascript:void(0)"><i class="icon-remove icon-large"></i></a></div> ');
    $(this).css("background-color","#EEEEEE");
}).on("mouseleave",".table-row",function(){
    if($(this).has("input")[0]) {
        return;
    }
    $(this).children("div:eq(3)").remove();
    $(this).css("background-color","#FFFFFF");
});


$(this).on("click",".table-row .icon-remove",function(){
    $row = $(this).closest(".table-row");
    id = $row.children("div:first").text();
    $.post("/admin/cpu_mem/delete/",
        {"id":id},
        function(res) {
            if(res['flag']) {
                $row.remove();
            }
        },
        "json"
        );
});
$(this).on("click",".table-row .icon-edit",function(){
    if($(".table-row").has(".icon-trash")[0]) {
        $(".table-row .icon-trash").trigger("click");
    }
    $row = $(this).closest(".table-row");
    id = $row.children("div:first").text();
    $cpu = $row.children("div:eq(1)");
    $mem = $row.children("div:eq(2)");
    $action = $mem.next();
    cpu = $cpu.text();
    mem = $mem.text();

    $cpu.html('<input type="text" class="input-mini" value='+cpu+'>');
    $mem.html('<input type="text" class="input-mini" value='+mem+'>');
    $action.html(' <a href="javascript:void(0)"><i class="icon-save icon-large"></i></a> &nbsp;&nbsp;&nbsp;&nbsp; <a href="javascript:void(0)"><i class="icon-trash icon-large"></i></a> ');
});

$(this).on("click",".table-row .icon-save",function(){
    $row = $(this).closest(".table-row");
    var id = $row.children("div:first").text();
    $cpu = $row.children("div:eq(1)");
    $mem = $row.children("div:eq(2)");
    $action = $mem.next();
    var cpu = $cpu.children().val();
    var mem = $mem.children().val();
    $.post("/admin/cpu_mem/update/",
        {"id":id, "cpu":cpu, "mem":mem},
        function(res) {
            if(!res["flag"]) {
                $("#message").html('<div class="alert alert-error"><button class="close" data-dismiss="alert">&times;</button>'+res["msg"]+'</div>');
                $("#message").show().delay(3000);
                $("#message").slideUp('slow');
                return;
            }
            $cpu.html('<font color="#009900">'+cpu+'</font>');
            $mem.html('<font color="#009900">'+mem+'</font>');
            $action.remove();
            sort_table();
        },
        "json"
        );
});

$(this).on("click",".table-row .icon-trash",function(){
    $row = $(this).closest(".table-row");
    id = $row.children("div:first").text();
    $cpu = $row.children("div:eq(1)");
    $mem = $row.children("div:eq(2)");
    $action = $mem.next();
    <!--cpu = $cpu.children().val();-->
    <!--mem = $mem.children().val();-->
    $cpu.html('<font color="#009900">'+cpu+'</font>');
$mem.html('<font color="#009900">'+mem+'</font>');
$action.remove();
});

sort_table();

function sort_table(){
    var cmp = function(a, b){
        var a_val = parseInt($(a).children("div:eq(1)").text());
        var b_val = parseInt($(b).children("div:eq(1)").text());
        flag = a_val - b_val;
        if(flag == 0) {
            var a_val = parseInt($(a).children("div:eq(2)").text());
            var b_val = parseInt($(b).children("div:eq(2)").text());
            return a_val - b_val;
        }
        return flag;
    };
    $(".table-row").sort(cmp).appendTo("#cpu_mem_table");
}

});
