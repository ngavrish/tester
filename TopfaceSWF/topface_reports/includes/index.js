$(document).ready(function() {

    $(".test_case").click(function(){
       var test_case_id = $(this).attr('id');
       $("#" + test_case_id + "_content").toggle();
    });
    // Handler for .ready() called.
});
