$(document).ready(function() {    
    $('#id_profile_picture').change(function(e){
        var fileName = e.target.files[0].name;
        $("#profile-picture-selected").text("File selected: "+fileName);
    });
    
    $('#id_remain_anonymous').change(function(e){
        if($('input[name="remain_anonymous"]').prop('checked')) {
            $("#remain-anonymous-text").text("Your username will not be displayed on bids or artifact ownership");   
        }
        else {
            $("#remain-anonymous-text").text("Select this option to ensure that your username is not displayed on bids or artifact ownership.");   
        }
    });    
    
})    