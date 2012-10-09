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

});