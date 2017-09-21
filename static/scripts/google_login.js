function signInCallback(authResult) {
  if (authResult['code']) {

    // Hide the sign-in button now that the user is authorized
    $('#signinButton').attr('style', 'display: none');
    var state=document.getElementById("template-data").dataset.state;
    // console.log(authResult)

    // Send the one-time-use code to the server, if the server responds, write a 'login successful' message to the web page and then redirect back to the main restaurants page
    $.ajax({
      type: 'POST',
      url: '/gconnect?state='+state,
      processData: false,
      data: authResult['code'],
      contentType: 'application/octet-stream; charset=utf-8',
      success: function(result) {
        console.log("sucesss ajax")
        console.log(result);
        // Handle or verify the server response if necessary.
        if (result) {
          $('#login-modal').modal('hide');
          $('#login-status').html(result);
          $('#login-status').toggle('display');
          $('#login-modal').modal('hide');
          // $(".container-fluid ~ div ").hide();
          $('#opaque-layer').toggle("display");
         setTimeout(function() {
          window.location.href = "/";
         }, 4000);


      }
      else if (authResult['error']) {

    console.log('There was an error: ' + authResult['error']);
  } else {
        $('#result').html('Failed to make a server-side call. Check your configuration and console.');
         }

      }

  });
  }
}


 function renderButton() {
      gapi.signin2.render('signInButton', {
        'scope': 'profile email',
        'width': 200,
        'height': 30,
        'longtitle': true,
        'theme': 'dark',
        'onsuccess':'signInCallback'
      });
    }