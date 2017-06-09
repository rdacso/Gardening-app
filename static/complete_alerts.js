'use strict';

function completeTask(){
  var checkboxid = $(this).attr('id');
  console.log(this);
  var id = 'divalert'+ checkboxid;
  console.log(id);
  if($(this).prop(":checked"));{  
    console.log('3');
    $('#'+ id).hide();
    console.log('4');
  }
}

$('.completedalert').on('click', completeTask)

function hideAlert(response){
  var completion = response['completion'];
  console.log('5');
  var div_id = "#alert" + response['user_plant_id'];
  console.log('6');
}

function addAlertCompletion(evt){
  evt.preventDefault();
  console.log('7')
  var formInputs = $(this).serialize();
  console.log(formInputs);
  console.log('8');
  $.post('/completealert.json', formInputs, hideAlert);
  console.log('9');
}
  
$('.alertajaxform').on('click', addAlertCompletion);
console.log('10');
