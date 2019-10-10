$(document).ready(function() {

    var artifactIds = [];
    var artifactContainers = [];
    $(".artifact-information").each(function() {
        var artifactId = $(".auction-artifactid", this).data("artifactid");
        var artifactContainer = $(this);
        if(artifactId) {
            artifactIds.push(artifactId);
            artifactContainers.push(artifactContainer);
        }
    })
    for (i=0; i<artifactIds.length; i++) {
        getBidData(artifactIds[i], artifactContainers[i]); 
    }
})


function initialisePage(artifactId, startTime, endTime, currentBid, artifactContainer) {
    var currentTime = new Date().getTime();
    var auctionTimer=$(".auction-timer-container", artifactContainer);
    var auctionBidStatus=$(".auction-bid-status", artifactContainer);
    var auctionButtons=$(".auction-buttons", artifactContainer);
    var auctionSoldStatus=$(".auction-sold-status", artifactContainer);        
    
    var auctionText;
    
    if (startTime && endTime) {
        if (currentTime > startTime && currentTime < endTime) {
            auctionTimer.show();
            auctionBidStatus.show();
            auctionButtons.show();
            auctionSoldStatus.hide();
            auctionText = "Auction time remaining:";
            displayTimer(artifactContainer, artifactId, endTime, auctionText, true);
            checkBid(artifactId, currentBid, artifactContainer);
        }
        else if (currentTime < startTime) {
            auctionTimer.show();
            auctionBidStatus.hide();
            auctionButtons.hide();
            auctionSoldStatus.hide();
            auctionText = "Time to start of auction:";
            displayTimer(artifactContainer, artifactId, startTime, auctionText, false);
        }
        else {
            auctionTimer.hide();
            auctionBidStatus.hide();
            auctionButtons.hide();
            auctionSoldStatus.show();
            auctionText="Auction finished.";
        }
    }
    else {
        auctionTimer.hide();
        auctionBidStatus.hide();
        auctionButtons.hide();
        auctionSoldStatus.show();
        auctionText="Not yet listed for auction.";
    }
    $(".auction-status", artifactContainer).text(auctionText);
}

function displayTimer(artifactContainer, artifactId, referenceTime, auctionText, auctionStarted) {
    var timer = setInterval(function() {
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

        if (timeLeft <= 0) {
            clearInterval(timer);
            $(".auction-buttons", artifactContainer).hide();
            $(".auction-bid-status", artifactContainer).hide();
            $(".auction-timer-container", artifactContainer).hide();
            location.reload();
        }

    }, 1000);
}

function checkBid(artifactId, currentBid, artifactContainer) {
    var timer = setInterval(function() {
    $.ajax({
        type:"GET",
        url: "get_bid",
        data: { "artifact_id" : artifactId },
        success: function(data) {
        if (data['current_bid']>currentBid) {
                location.reload();
            }
        }
    })
    }, 10000);
}

function getBidData(artifactId, artifactContainer) {
    $.ajax({
        type:"GET",
        url: "get_bid",
        data: { "artifact_id" : artifactId },
        success: function(data) {
            if(data.in_auction) {
                var currentBid = data['current_bid']
                var startTime = Date.parse(data['start_time']);
                var endTime = Date.parse(data['end_time']);
                initialisePage(artifactId, startTime, endTime, currentBid, artifactContainer)
            }
            else {
                console.log(data['message']);
                initialisePage(artifactId, "", "", 0, artifactContainer)
            }
        }
    })
}
