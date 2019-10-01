$(document).ready(function() {

    var startTime = Date.parse($("#startTime").val());
    var endTime = Date.parse($("#endTime").val());

    var timer = setInterval(function() {
        var currentTime = new Date().getTime();

        if (currentTime > startTime) {
            $("#timer-container").show();
            var timeLeft = endTime - currentTime;

            var days = Math.floor(timeLeft / (1000 * 60 * 60 * 24));
            var hours = Math.floor((timeLeft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            var minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
            var seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);
            var dayString=" days "
            var hourString=" hours "
            var minuteString=" minutes "
            var secondString=" seconds";

            if (days==0) { dayString="" }
            else if (days==1) { dayString=" day " }
            if (hours==0) { hourString="" }
            else if (hours==1) { hourString=" hour "}
            if (minutes==0) { minuteString="" }
            else if (minutes==1) { minuteString=" minute " }
            if (seconds==0) { secondString="" }
            else if (seconds==1) { secondString=" second" }
          
            $("#timer").text(days + dayString + hours + hourString + minutes + minuteString + seconds + secondString);

            if (timeLeft <= 0) {
                clearInterval(timer);
                $("#timer").text("Auction over");
            }
        }
    }, 1000);
})
