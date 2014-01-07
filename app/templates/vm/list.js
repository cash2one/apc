$(document).ready(function() {
    //Checkbox
    $("thead input:checkbox").click(function() {
        checked = $(this).is(":checked");
        $("tbody input:checkbox").each(function(i) {
            if($(this).is(":checked") != checked) {
                $(this).click();
            }
        });
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


    //Start
    $("#vmop-btn .start").click(function() {
        update_vmlist();
        $("#action").val("start");
        $("#vmop").submit();
    });


    //Power Off
    $("#vmop-btn .poweroff").click(function() {
        if(confirm("你确定要关机吗!")) {
            update_vmlist();
            $("#action").val("poweroff");
            $("#vmop").submit();
        }

    });


    //Power Off Hard
    $("#vmop-btn .poweroff_hard").click(function() {
        if(confirm("你确定要强制关机吗!")) {
            update_vmlist();
            $("#action").val("poweroff_hard");
            $("#vmop").submit();
        }

    });


    //Reboot
    $("#vmop-btn .reboot").click(function() {
        if(confirm("你确定要重启机器吗!")) {
            update_vmlist();
            $("#action").val("reboot");
            $("#vmop").submit();
        }
    });


    //Reboot Hard
    $("#vmop-btn .reboot_hard").click(function() {
        if(confirm("你确定要强制重启机器吗!")) {
            update_vmlist();
            $("#action").val("reboot_hard");
            $("#vmop").submit();
        }
    });


    //Recreate
    $("#vmop-btn .recreate").click(function() {
        if(!confirm("你确定要重建吗!")) {
            return false;
        }
        if(!confirm("请再次确认重建!")) {
            return false;
        }

        update_vmlist();
        $("#action").val("recreate");
        $("#vmop").submit();
    });


    //Delete
    $("#vmop-btn .delete").click(function() {
        if(!confirm("你确定要删除吗!")) {
            return false;
        }
        if(!confirm("请再次确认删除!")) {
            return false;
        }

        update_vmlist();
        $("#action").val("delete");
        $("#vmop").submit();
    });


    //Detail
    $("tbody tr").dblclick(function() {
        e = $(this);
        hostname = e.children(".hostname").children("span").html();
        $("#myModalLabel").html(hostname);
        $('#myModal').modal({
            remote: e.attr("data-detail"),
        });
        return false;
    });

    $('body').on('hidden', '.modal', function () {
        $(this).removeData('modal');
    });

    $('body').on('hidden', '#myModal', function () {
        window.location.reload();
    })

    $('body').on('shown', '#myModal', function () {
        $(".nav-tabs a[href='"+ $("#tabs_active").html() +"']").click();
    })
});
