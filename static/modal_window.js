
'use strict'; 

// display modal window

function displayModal() {
  var id = $(this).attr('id');
  $('#modal'+ id).css('display', 'block');
}
// event handler that calls the function that displays the modal window
$('.modalbutton').on('click', displayModal);

// When 'submit' button is clicked, submit a form

$(".userform").on("submit", function(){
      var formInputs = $(this);
      console.log(formInputs);
  })

  
