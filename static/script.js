// This line writes the text "Login page loaded" to the browser's developer console.
// It is mainly used for debugging to check that the JavaScript file is connected properly
console.log("Login page loaded");

//---------------------------------------------------------------
//Function to open the signup page in a popup window
//---------------------------------------------------------------
function openSignupWindow()
{
    window.open('/signup', 'Signup', 'width=400,height=400,top=200,left=500');
}

    var count = 6000; // Sets the starting value for the countdown (6000 units of 10ms = 60 seconds)
    var counter = setInterval(timer, 10); // Starts a repeating timer that runs the function every 10 milliseconds
    
    function timer() // Creates a function called timer
    {
        if (count <= 0) // This checks if the countdown has reached zero or less
        {
            clearInterval(counter); // This stops the interval from running further
            return; // Exits the function
         }
         count--; // Subtracts 1 from the 'count' variable
         document.getElementById("Timer").innerHTML = (count / 100).toFixed(2); // Calculates the seconds, formats it to 2 decimal places
     }