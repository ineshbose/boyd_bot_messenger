$(document).ready(function(){
    $("#remember").change(function(){
        if ($('#remember').prop('checked')) {
            $("#subscribe").prop("disabled", false);
        }
        else{
            $("#subscribe").prop("disabled", true);
            $("#subscribe").prop("checked", false);
        }
    });
});