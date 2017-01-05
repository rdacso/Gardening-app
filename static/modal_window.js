
'use strict'; 

// display modal window for plant tasks

var span = document.getElementsByClassName("close")[0];

function displayPlantModal() {
  var id = $(this).attr('id');
  $('#modal'+ id).css('display', 'block');
  
  span.onclick = function() {
    $('#modal'+ id).css('display', 'none');
}}

// event handler that calls the function that displays the modal window
$('.modalbutton').on('click', displayPlantModal);




  
