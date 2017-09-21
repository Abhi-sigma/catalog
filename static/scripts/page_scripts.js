
$('.modal-social-icons').bind({
	click:function(){
		$('#opaque-layer').toggle('display');
	}

})


$('.logout-text').bind({
	click:function(){
		$('#opaque-layer').toggle('display');
	}

})

$(document).ready(function(){
$('#login-modal').on('show.bs.modal', function () {
	// console.log("clicked");
	document.getElementById("g_sign").onclick=function(){
	// console.log("clicked");
	$("#signInButton button").click();
		}
	})
})

function request_options(){
	var sel_element=$("#item_category");
	sel_element_loaded=false;
	if (sel_element_loaded == false){
	$.get( "/get_all_categories", function( data ) {
	  // $( ".result" ).html( data );
	  // alert( data );
	  var response=JSON.parse(data);
	  // console.log(response.length);
	  if (response.length==0){
	  	$("#item_form").attr("disabled", "disabled");
	  }
	  // console.log(response)
	  var counter=0;
	  response.forEach(function(category){
	  	sel_element.append("<option>"+category["name"]+"</option")
	  	counter++;
	  })
	  sel_element_loaded=true;
	  $("#item_category").off()
	  return
	   })

       }
   }

function blink(selector){
		$(selector).fadeOut('slow', function(){
    	$(selector).fadeIn('slow', function(){
        blink(this);
    		});
		});
	 }

function flash_messages(){
	var message = $(".messages");
	var count=0;
	if(($(".messages").text().length) >0) {
		var $text=$(".messages").text();
	    var interval = setInterval(function(){
		count++
		blink(message)
		console.log(count);
		 if(count>6){
		 	$(message).remove();
		 	// $('.message_container').append('<div class="messages">'+$text+'</div>')
			clearInterval(interval);
  }
	},500)

 }

}

$(document).ready(function(){
	request_options();
	flash_messages();
	})

$(document).ready(function(){
	// // $("form #category-form button").on("click",request_options)
	// request_options();
	if (window.location.pathname !="/")
		{
			$("#modal-launcher").remove()}
})

