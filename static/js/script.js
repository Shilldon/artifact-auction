//Function to update the artifacts and display_artifact templates with current auction status of artifacts
$(document).ready(function() {
    var artifactIds = [];
    var artifactContainers = [];
    $(".artifact-information").each(function() {
        //iterate through all artifacts displayed on page and retrieve artifact ID from hidden div
        var artifactId = $(".auction-artifactid", this).data("artifactid");
        var artifactContainer = $(this);
        //Create array of artifacts for ajax request for information
        if(artifactId) {
            artifactIds.push(artifactId);
            artifactContainers.push(artifactContainer);
        }
    })
    for (i=0; i<artifactIds.length; i++) {
        //call getBidData to get information on the artifact
        getBidData(artifactIds[i], artifactContainers[i]); 
    }
})

//Function to initialise the page with all artifact auction information
function initialisePage(artifactId, startTime, endTime, currentBid, artifactContainer) {
    var currentTime = new Date().getTime();
    var auctionTimer=$(".auction-timer-container", artifactContainer);
    var auctionBidStatus=$(".auction-bid-status", artifactContainer);
    var auctionButtons=$(".auction-buttons", artifactContainer);
    var auctionSoldStatus=$(".auction-sold-status", artifactContainer);        
    var auctionStatus=$(".auction-status", artifactContainer)
    
    var auctionText;
    
    //Display information on each auction if it has a start and end time
    if (startTime && endTime) {
        //Auction is currently live - send information to template to show time left and bid status
        if (currentTime > startTime && currentTime < endTime) {
            auctionText = "Time left: ";
            auctionTimer.show(); //show the auction timer
            auctionBidStatus.show(); //show the current bids
            auctionButtons.show(); //show the bid and buy now buttons
            auctionSoldStatus.hide(); //hide the sold status of the artifact
            displayTimer(artifactContainer, artifactId, endTime, auctionText, true);
            checkBid(artifactId, currentBid, artifactContainer);
        }
        //Auction is not yet live - send information to template with countdown for time left to start
        else if (currentTime < startTime) {
            auctionText = "Starts in: ";
            auctionTimer.show(); //show the auction timer 
            auctionBidStatus.hide(); //hide the status of the current bids (there are none)
            auctionButtons.hide(); //hide the bid and buy now buttons
            auctionSoldStatus.hide(); //hide the sold status of the artifact
            displayTimer(artifactContainer, artifactId, startTime, auctionText, false);
        }
        else {
            //If the current time is after the end of the auction hide all the auction
            //status, timer and bids but show the sold status
            auctionTimer.hide();
            auctionBidStatus.hide();
            auctionButtons.hide();
            auctionSoldStatus.show();
            auctionText="Auction finished.";
        }
    }
    else {
        //If no auction has been created for the artifact hide all auction and sold information and 
        //show as not yet listed for auction 
        auctionTimer.hide();
        auctionBidStatus.hide();
        auctionButtons.hide();
        auctionSoldStatus.show();
        auctionText="Not yet listed for auction.";
    }
    auctionStatus.text(auctionText);
}

//Function to display the time left in or until auction - refreshes every second
function displayTimer(artifactContainer, artifactId, referenceTime, auctionText, auctionStarted) {
    var timer = setInterval(function() {
        var currentTime = new Date().getTime();
        var timeLeft = referenceTime - currentTime;

        var days = Math.floor(timeLeft / (1000 * 60 * 60 * 24));
        var hours = Math.floor((timeLeft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);
        var dayString = "d "
        var hourString = "h "
        var minuteString = "m "
        var secondString = "s";

        if (days == 0) { days = "";
            dayString = "" }
        
        if (hours == 0) { hours = "";
            hourString = "" }
        
        if (minutes == 0) { minutes = "";
            minuteString = "" }
        
        if (seconds == 0) { seconds = "";
            secondString = "" }
        //update text on page with time left
        $(".auction-timer", artifactContainer).text(days + dayString + hours + hourString + minutes + minuteString + seconds + secondString);

        //If there is no time left hide the auction timer, bid and buynow buttons and reload the page
        if (timeLeft <= 0) {
            clearInterval(timer);
            $(".auction-buttons", artifactContainer).hide();
            $(".auction-bid-status", artifactContainer).hide();
            $(".auction-timer-container", artifactContainer).hide();
            location.reload();
        }

    }, 1000);
}

//Ajax call to backend every 10 seconds to check wheterha new high bid has been placed. 
//If so update the page to display the new highest bid
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

//Function called on page load to get auction information on artifact to initialise
//the display.
function getBidData(artifactId, artifactContainer) {
    $.ajax({
        type:"GET",
        url: "get_bid",
        data: { "artifact_id" : artifactId },
        //send artifact ID to back end
        success: function(data) {
            //If there is a live auction for the artifact return bid and auction details to initialisepage function
            if(data.in_auction) {
                var currentBid = data['current_bid']
                var startTime = Date.parse(data['start_time']);
                var endTime = Date.parse(data['end_time']);
                initialisePage(artifactId, startTime, endTime, currentBid, artifactContainer)
            }
            //If not return blank to initialisepage function
            else {
                initialisePage(artifactId, "", "", 0, artifactContainer)
            }
        }
    })
}
