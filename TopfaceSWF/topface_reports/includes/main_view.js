/**
 * Created with PyCharm.
 * User: ngavrish
 * Date: 09.10.12
 * Time: 12:02
 * To change this template use File | Settings | File Templates.
 */

$(document).ready(function() {

    $("#refresh_main_view").click(function() {
        $.ajax({
            url: "http://tester84:8889/update"
        });
    });

    $("#start_tests").click(function() {
        $("#starting_tests_panel").toggle();
    });

    $("#ajax_start_tests").click(function() {
        var param_string = $("#ajax_test_params").val();
        $.ajax({
            type: "POST",
            data: {params : param_string},
            url: "http://tester84:8889/start",
            success: function(data) {
                alert(data);
            }
        })
    });

});