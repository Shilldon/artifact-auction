    $(window).on('load resize refresh', function() {
        var titleWidth = $(".index--title-image").width();
        var titleHeight = titleWidth * .7331;
        $(".index--title-image").css("height", titleHeight + "px")
        if($(window).width()>=1280) {
            $(".index--title-image").css("width", "92%");
            $(".index--title-image").css("margin", "5vh auto")   
        }
    });
    