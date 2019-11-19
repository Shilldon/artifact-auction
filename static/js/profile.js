$(document).ready(function() {    
    //Function to display name of image selected to upload for profile picture
    $('#id_profile_picture').change(function(e){
        var fileName = e.target.files[0].name;
        var file = e.target.files[0];
        //Display file name
        $("#profile-picture-selected").html("File selected: "+fileName+"<br>Click 'Update' to upload image.");
        //Display option to clear image selected for upload
        $('#id_profile--clear-image-selection, #id_profile--clear-image-selection-label').show();
        if(file) {
            //If user selects a file to upload hide the option to delete profile picture
            $('#id_profile_picture-clear').prop("checked", false);
            $("#profile--current-image").hide();    
        }
    });
    
    //Function to show the profile picture if the user decides not to upload a new image 
    $("#id_profile--clear-image-selection").change(function() {
        if($(this).prop("checked")==true) {
            //Delete the form entry for a new profile picture
            $('#id_profile_picture').val('');
            //hide the name of the file selected to upload
            $("#profile-picture-selected").html("");
            //Remove option to clear the file selected for upload
            $('#id_profile--clear-image-selection, #id_profile--clear-image-selection-label').hide();
            //Reshow the current profile image
            $('#profile--current-image').show(); 
            $(this).prop("checked", false)
        }            
    });

    //Function to handle selection to delete current profile picture
    $('#id_profile_picture-clear').change(function(e){
        if($('input[name="profile_picture-clear"]').prop('checked')) {
            //Hide the profile picture
            $("#profile-picture").hide();
            $("#profile--remove-profile-picture-info").text("Now click 'Update' to remove your profile picture.");
            //Delete the form entry for the current profile picture
            $('#id_profile_picture').val('');   
            //Hide the option to choose a new profile picture
            $('#profile--choose-new-image').hide();            
        }    
        else {
            //Show the profile picture
            $("#profile-picture").show();    
            //Remove instructions to update having selected remove picture
            $("#profile--remove-profile-picture-info").text("");
            //Show option to choose a new profile picture
            $('#profile--choose-new-image').show();            
        }
    });
    
    //Function to switch information and options on selecting or deselecting 'remain anonymous'
    $('#id_remain_anonymous').change(function(e){
        if($('input[name="remain_anonymous"]').prop('checked')) {
            $("#remain-anonymous-text").text("Your username and profile picture will not be displayed on bids or artifact ownership");   
        }
        else {
            $("#remain-anonymous-text").text("Select this option to ensure that your username and profile picture are not displayed on bids or artifact ownership.");   
        }
    });   
    

    
})    