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

$("#resetSearch").click(function() {
    $('#filterModal input[name="category"]').each(function() {
        $(this).attr("checked",true);
    });
    $('#filterModal input[name="type"]').each(function() {
        $(this).attr("checked",true);
    });  
})


$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})