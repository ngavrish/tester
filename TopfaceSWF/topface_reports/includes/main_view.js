/**
 * Created with PyCharm.
 * User: ngavrish
 * Date: 09.10.12
 * Time: 12:02
 * To change this template use File | Settings | File Templates.
 */

$(document).ready(function() {

    $("#refresh_main_view").click(function() {
        refresh_view();
    });

    $("#start_tests").click(function() {
        $("#starting_tests_panel").toggle();
        if ($("#ajax_test_params").attr('class') == 'ajax_test_params_active') {
            $("#ajax_test_params").attr('class','ajax_test_params_nonactive')
        }
    });

    $("#ajax_test_params").click(function() {
        if ($("#ajax_test_params").attr('class') == 'ajax_test_params_nonactive') {
            $("#ajax_test_params").val(null);
        }
        $(this).attr('class','ajax_test_params_active');
    });

    $("#ajax_start_tests").click(function() {
        var param_string = $("#ajax_test_params").val();
        $.ajax({
            type: "POST",
            data: {params : param_string},
            url: "http://tester84:8888/start",
            success: function(data) {
                alert(data);
            }
        })
    });

    $("#describe_test_params_button").click(function() {
        if ($(this).html() == "Что сюда писать:") {
            $(this).html("Все понял");
        } else {
            $(this).html("Что сюда писать:");
        }

        $("#test_params_description_div").toggle()
    });

    function refresh_view() {
        $.ajax({
            type: "GET",
            url: "http://tester84:8888/update",
            success: function(data) {
                $("#buildhistory_wrapper").empty();
                var html_string;
                for (var item in data) {
    //                failed test suite
                    if (data[item][2] == 0) {
                        html_string = "<p><a class=\"failed\" href=\"" + data[item][0] + "\">" + data[item][1] + "</a></p>";
                    } else {
                        html_string = "<p><a href=\"" + data[item][0] + "\">" + data[item][1] + "</a></p>";
                    }
                    $("#buildhistory_wrapper").append(html_string);
                }
                AmCharts.ready();
            }
        });
    }
    refresh_view();
    setInterval(refresh_view, 300000);
});

