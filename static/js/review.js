//Function to highlight the 'rating stars' on hover/click
$('[id*="review-star-"]').on("mouseover click", function(){
    var id=$(this).attr('id').split("-");
    var starNumber=id.slice(-1)[0];
    for(i=1;i<=5;i++) {
        if(i<=starNumber) {
            //highlight stars in gold up to the current rating value
            $("#review-star-"+i).removeClass("review-empty-star far");
            $("#review-star-"+i).addClass("review-star fas");
        }
        else {
            //Change stars to outline for those above current review rating
            $("#review-star-"+i).removeClass("review-star fas");
            $("#review-star-"+i).addClass("review-empty-star far");
        }
    }
    //Add the form entry for the rating value based on number of stars selected
    $("#id_rating").val(starNumber);
});