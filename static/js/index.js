//Function to alter size of main title display image depending on screen width
$(window).on('load resize refresh', function() {
    var titleWidth = $(".index--title-image").width();
    var titleHeight = titleWidth * 0.7331; //This is the height width ratio of the original image
    $(".index--title-image").css("height", titleHeight + "px");
    if($(window).width()>=992) {
        $(".index--title-image").css("width", "92%");
        $(".index--title-image").css("margin", "5vh auto");   
    }
});
    