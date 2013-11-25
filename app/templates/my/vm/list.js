$(document).ready(function() {
    $("thead input[type='checkbox']").click(function() {
        $("tbody input[type='checkbox']").click();
    });

    $("tbody input:checkbox").click(function() {
        update_vmlist();
    });

    function update_vmlist() {
        var vm_arr = [];
        $("tbody tr").each(function(i) {
            ele = $(this);
            id = $(this).attr("data-id");
            if_checked = $("#vm_"+ id +" td input:checkbox:checked").val();
            if(if_checked == "on") {
                vm_arr.push(id);
                ele.addClass("selected");
            } else {
                ele.removeClass("selected");
            }
        });

        $("#vmlist").val(vm_arr);
    }

    $("#vmop-btn .delete").click(function() {
        if(!confirm("你确定要删除吗!")) {
            return false;
        }

        $("#action").val("delete");
        update_vmlist();
        $("#vmop").submit();
    });
});
