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
    console.log("blob8")
    $('#filterModal input[name="category"]').each(function() {
        $(this).attr("checked",true);
    });
    $('#filterModal input[name="type"]').each(function() {
        $(this).attr("checked",true);
    });  
})

$('#filterModal input[id="id_sold"]').change(function() {
    if($(this).prop("checked") == true) {
        $('#filterModal input[id="id_unsold"]').prop("checked",false);
    }
})


$('#filterModal input[id="id_unsold"]').change(function() {
    if($(this).prop("checked") == true) {
        $('#filterModal input[id="id_sold"]').prop("checked",false);
    }
})


$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})