'use strict';

function displayQty(response){
  var qty = response['qty'];
  console.log('qty');

  var div_id = "#plant_number" + response['user_plant_id'];
  console.log(div_id);

  $(div_id).html('<div>' + 'You have ' + qty + ' of these plants in your garden' + '</div>');
}

function addNum(evt){
  evt.preventDefault();
  console.log($(this));

  var formInputs = $(this).serialize();
  console.log(formInputs);

  $.post('/addqty.json', formInputs, displayQty);
  console.log('#7');
}
  
$('.ajaxform').on('submit', addNum);