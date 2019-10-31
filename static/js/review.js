    $('[id*="review-star-"]').on("mouseover click", function(){
        console.log("hovering over star")
        var id=$(this).attr('id').split("-")
        var starNumber=id.slice(-1)[0];
        for(i=1;i<=5;i++) {
            if(i<=starNumber) {
                $("#review-star-"+i).removeClass("review-empty-star far")
                $("#review-star-"+i).addClass("review-star fas")
            }
            else {
                $("#review-star-"+i).removeClass("review-star fas")
                $("#review-star-"+i).addClass("review-empty-star far")
            }
        }
        $("#id_rating").val(starNumber);
    })