'use strict';

$(document).ready(function() {
    $('#registrationform').validate({
        rules: {
            firstname: {
                required: true,
            },
            lastname: {
                required: true, 
            },
            email: {
                required: true,
                email: true
            },
            password: {
                required: true,
                minlength: 5
            },
             confirm_password: {
                required: true,
                minlength: 5,
                equalTo: '#password'

            },
        messages:{
            firstname: 'Please enter your first name',
            lastname: 'Please enter your last name',
            email: {
                required: 'Please enter your email'
            },
            password:{
                required: 'Please provide a password',
                minlength: 'Your password must be at least 5 characters long'
            },
            confirm_password:{
                required: 'Please provide a password',
                minlength: 'Your password must be at least 5 characters long',
                equalTo: 'Please enter the same password as above'
            }

        }}})});


    // $('#email').focus(function()){
    //     var firstname = $('#firstname').val();
    //     var lastname = $('#lastname').val();
    //     if (firstname && lastname && :this.value) {
    //         this.value = firstname + '.' + lastname;
    //     }
    // };
