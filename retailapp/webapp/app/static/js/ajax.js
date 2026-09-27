$(document).ready(function(){
 $(".search-results").css("display", "none")
		$("body").on("click", function(){
		  	$(".search-results").css("display", "none")
		})

		if($('[data-toggle="tooltip"]').length>0) {  // check if element exists
			$('[data-toggle="tooltip"]').tooltip()
		} 

		$(".search input").on("keyup", function(e){
		    value = $(".search input").val();
		      $(".search-results").css("display", "block")
		    $.ajax({
		        url:`/ajax/search?query=${encodeURIComponent(value.toLowerCase())}`
		    }).done(function(data){
		      showResults(data)
		    })

})

function showResults(data){
if(data.length === 0 ){
$(".search-results .container").text("No Search Results Found")
}
else if (data.length <=4 ){
  // build elements with .text()/.attr() so product fields are never parsed as HTML
  var rows = data.map(item =>
    $('<div class="row">').append(
      $('<div class="col p-2 ml-3">').append(
        $('<a>').attr("href", `/products/view?id=${encodeURIComponent(item.id)}`).text(item.name)
      )
    )
  )
  $(".search-results").empty().append(rows)

}


}

}); 
