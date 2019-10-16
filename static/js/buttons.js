$(".collapse-button").click(function() {
    var collapsible=$(this).attr("data-target")
    
    if($(collapsible).hasClass("show")) {
        $("i", this).addClass("fa-caret-down");    
        $("i", this).removeClass("fa-caret-up");  
    }
    else {
        $("i", this).addClass("fa-caret-up");    
        $("i", this).removeClass("fa-caret-down");  
        
    }

})


$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})