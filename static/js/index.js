    $(window).on('load resize refresh', function() {
        var titleWidth = $(".index--title-image").width();
        var titleHeight = titleWidth * .7331;
        $(".index--title-image").css("height", titleHeight + "px")
    });
    