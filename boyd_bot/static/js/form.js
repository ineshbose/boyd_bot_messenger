$(document).ready(function(){
    $("#remember").change(function(){
        if ($('#remember').prop('checked')) {
            $('#subscribe [id^="subscribe-"]').prop("disabled", false);
        }
        else{
            $('#subscribe [id^="subscribe-"]').prop("disabled", true);
            $('#subscribe [id^="subscribe-"]').prop("checked", false);
        }
    });
});