
'use strict'; 

// display modal window

var span = document.getElementsByClassName("close")[0];

function displayModal() {
  var id = $(this).attr('id');
  $('#modal'+ id).css('display', 'block');
  
  span.onclick = function() {
    $('#modal'+ id).css('display', 'none');
}}

// event handler that calls the function that displays the modal window
$('.modalbutton').on('click', displayModal);



// When 'submit' button is clicked, submit a form

$(".userform").on("submit", function(){
      var formInputs = $(this);
      console.log(formInputs);
  })


  
