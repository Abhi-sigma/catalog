  window.fbAsyncInit = function() {
  FB.init({
    appId      : '112369232788720',
    cookie     : true,  // enable cookies to allow the server to access 
                        // the session
    xfbml      : true,  // parse social plugins on this page
    version    : 'v2.10' // use version 2.10
  });

  };



  // Load the SDK asynchronously
  (function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) 
      return;
    js = d.createElement(s); 
    js.id = id;
    js.src = "//connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
  }(document, 'script', 'facebook-jssdk'));


  // Here we run a very simple test of the Graph API after login is
  // successful.  See statusChangeCallback() for when this call is made.
  function sendTokenToServer() {
    var access_token = FB.getAuthResponse()['accessToken'];
    var state=document.getElementById("template-data").dataset.state;
    console.log(access_token)
    console.log('Welcome!  Fetching your information.... ');
    FB.api('/me', function(response) {
      console.log('Successful login for: ' + response.name);
     $.ajax({
      type: 'POST',
      url: '/fbconnect?state='+state,
      processData: false,
      data: access_token,
      contentType: 'application/octet-stream; charset=utf-8',
      success: function(result) {
        // Handle or verify the server response if necessary.
        if (result) {
          $('#login-modal').modal('hide');
          $('#login-status').html(result);
          $('#login-status').toggle('display');
          $('#opaque-layer').toggle('display');
         setTimeout(function() {
          window.location.href = "/";
         }, 4000);
          

      } else {
        $('#result').html('Failed to make a server-side call. Check your configuration and console.');
         }

      }
      
  });


    });
  }