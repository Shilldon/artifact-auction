$(document).ready(function() {    
    $('#id_profile_picture').change(function(e){
        var fileName = e.target.files[0].name;
        var file = e.target.files[0];
        console.log("file="+$(this).val())
        $("#profile-picture-selected").html("File selected: "+fileName+"<br>Click 'Update' to upload image.");
        $('#id_profile--clear-image-selection, #id_profile--clear-image-selection-label').show();
    });
    
    $("#id_profile--clear-image-selection").change(function() {
        $('#id_profile_picture').val('');  
        $("#profile-picture-selected").html("");
        $('#id_profile--clear-image-selection, #id_profile--clear-image-selection-label').hide();
        $(this).prop("checked", false)
    })
    
    $('#id_remain_anonymous').change(function(e){
        if($('input[name="remain_anonymous"]').prop('checked')) {
            $("#remain-anonymous-text").text("Your username and profile picture will not be displayed on bids or artifact ownership");   
        }
        else {
            $("#remain-anonymous-text").text("Select this option to ensure that your username and profile picture are not displayed on bids or artifact ownership.");   
        }
    });   
    
    $('#id_profile_picture-clear').change(function(e){
        if($('input[name="profile_picture-clear"]').prop('checked')) {
            $("#profile-picture").hide();
        }    
        else {
            $("#profile-picture").show();    
        }
    })
    
})    