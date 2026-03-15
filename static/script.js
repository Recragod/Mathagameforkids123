// This line writes the text "Login page loaded" to the browser's developer console.
// It is mainly used for debugging to check that the JavaScript file is connected properly
console.log ("Login page loaded");

//---------------------------------------------------------------
//Function to open the signup page in a popup window
//---------------------------------------------------------------
function openSignupWindow()
{
    window.open('/signup', 'Singup', 'width=400,height=400,top=200,left=500');
}
