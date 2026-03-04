#Importing Flask class & functions for HTML
#Flask create the web app

from flask import Flask, render_template,request
app = Flask(__name__)

#variables for login details
USERNAME = "admin"
PASSWORD = "1234"

#This route runs when the user goes to the login page
@app.route("/")

#name of function called home
def home():
#this shows the login.html page to the user
    return render_template("login.html")

#This route runs when the login form is submitted
#it only accepts POST requests - because the form uses POST in HTML
@app.route("/login", methods=["POST"])

#name of function called login to accept data the user types
def login():
    #Get the username typed in the form on the login screen
    username=request.form["username"]
    #Get the password typed in the form on the login screen
    password=request.form["password"]

    #Check if the username and password entered is a match to whats saved
    if username == USERNAME and password == PASSWORD:
        #if the correct details are entered, show success message
        return "Login successful"
    else:
        #if the incorrect details are entered, show invalid message
        return "Invalid username or password"

#This makes sure that the program runs only when this file is executed directly
if __name__ == "__main__":
    app.run(debug=True, port=8000)
