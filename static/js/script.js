$(document).ready(function() {
    $(".artifact-information").each(function() {

        var startTime = Date.parse($(".startTime", this).val());
        var endTime = Date.parse($(".endTime", this).val());
        var currentTime = new Date().getTime();
        var auctionText;
        if (startTime && endTime) {
            if (currentTime > startTime && currentTime < endTime) {
                $(".auction-button-buynow-container", this).hide();
                auctionText = "Auction time remaining:";
                displayTimer($(this), endTime, auctionText, true)
            }
            else if (currentTime < startTime) {
                $(".auction-button-bid-container", this).hide();
                auctionText = "Time to start of auction:";
                displayTimer($(this), startTime, auctionText, false);
            }
            else {
                $(".auction-button-bid-container", this).hide();
                auctionText="Auction finished.";
            }
        }
        else {
            $(".auction-button-bid-container", this).hide();
            auctionText="Not yet listed for auction.";
        }
        $(".auction-status", this).text(auctionText);
    })

})

function displayTimer(artifactContainer, referenceTime, auctionText, showBidder) {
    var timer = setInterval(function() {
        if(showBidder==true) {
            $(".auction-bid-status", artifactContainer).show()
        }
        $(".auction-timer-container", artifactContainer).show();
        $(".auction-button-bid-container", this).show();
        var currentTime = new Date().getTime();
        
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
        
        $(".auction-timer", artifactContainer).text(days + dayString + hours + hourString + minutes + minuteString + seconds + secondString);
        $(".auction-current-bid", artifactContainer).load(location.href + " .auction-current-bid");
        if (timeLeft <= 0) {
            clearInterval(timer);
            $(".auction-button-bid-container", this).hide();
            $(".auction-timer", artifactContainer).hide();
            location.reload();
        }

    }, 1000);
}
