$(document).ready(function() {
    $(window).on('load resize', function() {
        var titleWidth = $(".title-image").width();
        var titleHeight = titleWidth * .7331;
        $(".title-image").css("height", titleHeight + "px")
    });
});
    