$(".collapse-button").click(function() {
    var collapsible=$(this).attr("data-target")
    
    if($(collapsible).hasClass("show")) {
        $("i", this).addClass("fa-caret-down");    
        $("i", this).removeClass("fa-caret-up");  
    }
    else {
        $("i", this).addClass("fa-caret-up");    
        $("i", this).removeClass("fa-caret-down"); 
         $("html, body").animate({ scrollTop: $(collapsible).height()+"50px" }, 250);
    }
        

})

$("#resetSearch").click(function() {
    $('#filterModal textarea').each(function() {
        $(this).text('');
    })
    $('#filterModal input[type="number"]').each(function() {
        $(this).attr("value", "");
        console.log("clearing "+$(this).attr("id"))
    })    
    $('#filterModal input[type="checkbox"]').attr("checked", false);
    $('#filterModal input[name="category"]').each(function() {
        $(this).attr("checked",true);
    });
    $('#filterModal input[name="type"]').each(function() {
        $(this).attr("checked",true);
    });  
})

$('.opposite-switch').change(function() {
    var checked = $(this).prop("checked"); 
    var thisId = $(this).attr("id")
    var oppositeButton=$("input[value="+thisId+"]");
    if(checked==true && oppositeButton.prop("checked")==true) {
        oppositeButton.prop("checked",false);
    }    
})

$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})