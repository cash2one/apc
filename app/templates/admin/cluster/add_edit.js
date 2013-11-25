$(document).ready(function() {
    $("#ds_name").typeahead({
        source: function(query, process) {
            objects = [];
            map = {};
            $.ajax({
                type: "POST",
                url: datastore_api,
                data: "sunstone_api="+ $("#sunstone_api").val()  +"&sunstone_auth="+ $("#sunstone_auth").val(),
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
            $('#ds_id').val(map[item].sunstone_id);
            return item;
        }
    });
});

