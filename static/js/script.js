$(document).ready(function() {
    $(".artifact-timer").each(function() {

        var startTime = Date.parse($(".startTime", this).val());
        var endTime = Date.parse($(".endTime", this).val());
        var currentTime = new Date().getTime();
        var auctionText;
        if (startTime && endTime) {
            if (currentTime > startTime) {
                auctionText = "Auction time remaining:";
                displayTimer($(this), endTime, auctionText, true)
            }
            else if (currentTime < startTime) {
                auctionText = "Time to start of auction:";
                displayTimer($(this), startTime, auctionText, false)
            }
        }
        else {
            $(".auction-status", this).text("Not yet listed for auction.");
        }
    })

})

function displayTimer(artifactTimer, referenceTime, auctionText, showBidder) {
    var timer = setInterval(function() {
        if(showBidder==true) {
            $(".artifact-bid-status", artifactTimer).show()
        }
        var currentTime = new Date().getTime();
        $(".timer ", artifactTimer).show();
        $(".auction-status", artifactTimer).text(auctionText);
        var timeLeft = referenceTime - currentTime;

        var days = Math.floor(timeLeft / (1000 * 60 * 60 * 24));
        var hours = Math.floor((timeLeft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);
        var dayString = " days "
        var hourString = " hours "
        var minuteString = " minutes "
        var secondString = " seconds";

        if (days == 0) { days = "";
            dayString = "" }
        else if (days == 1) { dayString = " day " }
        
        if (hours == 0) { hours = "";
            hourString = "" }
        else if (hours == 1) { hourString = " hour " }
        
        if (minutes == 0) { minutes = "";
            minuteString = "" }
        else if (minutes == 1) { minuteString = " minute " }
        
        if (seconds == 0) { seconds = "";
            secondString = "" }
        else if (seconds == 1) {  secondString = " second" }
        
        $(".timer", artifactTimer).text(days + dayString + hours + hourString + minutes + minuteString + seconds + secondString);

        if (timeLeft <= 0) {
            clearInterval(timer);
            $(".timer h5", artifactTimer).text("Auction over");
        }

    }, 1000);
}
