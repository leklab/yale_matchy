var auth2; // The Sign-In object.
var googleUser; // The current user.
var signInLink = document.getElementById('sign-in-link');

/**
* Calls startAuth after Sign in V2 finishes setting up.
*/

window.onload = function() {
    gapi.load('auth2', initSigninV2);
};

/**
 * Initializes Signin v2 and sets up listeners.
 */
var initSigninV2 = function() {
  auth2 = gapi.auth2.init({
      client_id: '443149971299-a4ube422g2jmp838t2vtq33ofmh3m9rr.apps.googleusercontent.com',
      scope: 'profile'
  });

  auth2.isSignedIn.listen(updateSigninStatus);       
  auth2.currentUser.listen(userChanged);

  updateSigninStatus(gapi.auth2.getAuthInstance().isSignedIn.get()); 


};


function handleAuthClick(event) {
  gapi.auth2.getAuthInstance().signIn();
}
function handleSignoutClick(event) {
  gapi.auth2.getAuthInstance().signOut();
  window.location.href = "/"
}

function updateSigninStatus(isSignedIn) {
  //console.log('Signin state changed to ', isSignedIn);

  if (isSignedIn) {
    document.getElementById('sign-in-link').innerText = "Sign Out";
    document.getElementById('account-profile').style.display = 'block';


    document.getElementById('submissions-div').style.display = 'block';
    document.getElementById('submissions-menu').style.display = 'block';
    document.getElementById('submissions-new').style.display = 'block';
    document.getElementById('submissions-history').style.display = 'block';

    signInLink.onclick = handleSignoutClick;
  
  } else {
    document.getElementById('sign-in-link').innerText = "Sign In";
    document.getElementById('account-name').innerText = "Account";

    document.getElementById('account-profile').style.display = 'none';

    document.getElementById('submissions-div').style.display = 'none';
    document.getElementById('submissions-menu').style.display = 'none';
    document.getElementById('submissions-new').style.display = 'none';
    document.getElementById('submissions-history').style.display = 'none';


    signInLink.onclick = handleAuthClick;
  }
}

/**
 * Listener method for sign-out live value.
 *
 * @param {boolean} val the updated signed out state.
 */
var signinChanged = function (val) {
    console.log('Signin state changed to ', val);
    //document.getElementById('signed-in-cell').innerText = val;
};


/**
 * Listener method for when the user changes.
 *
 * @param {GoogleUser} user the updated user.
 */
var userChanged = function (user) {
    //console.log('User now: ', user);
    //document.getElementById('content').innerText = user['w3']['ig'];
    if(typeof user['w3'] != 'undefined'){
        document.getElementById('account-name').innerText = user['w3']['ig'];
    }
    //googleUser = user;
    //updateGoogleUser();
};


/**
 * Updates the properties in the Google User table using the current user.
 */
var updateGoogleUser = function () {
  if (googleUser) {
    //document.getElementById('user-id').innerText = googleUser.getId();
    //document.getElementById('user-scopes').innerText = googleUser.getGrantedScopes();
    //document.getElementById('auth-response').innerText = JSON.stringify(googleUser.getAuthResponse(), undefined, 2);
  } else {
    //document.getElementById('user-id').innerText = '--';
    //document.getElementById('user-scopes').innerText = '--';
    //document.getElementById('auth-response').innerText = '--';
  }
};
