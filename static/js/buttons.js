$("#options-collapse-button").click(function() {
    var collapsible=$(this).attr("data-target")
    
    if($(collapsible).hasClass("show")) {
        $("i", this).addClass("fa-caret-down");    
        $("i", this).removeClass("fa-caret-right");  
    }
    else {
        $("i", this).addClass("fa-caret-right");    
        $("i", this).removeClass("fa-caret-down");  
        
    }

})


$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})