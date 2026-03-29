#Programmer: Joe Shikagishi
#Importing Flask class & functions for HTML
#FLASK LOGIN AND SIGNUP APPLICAION (NO PASSWORD CHECK)
#------------------------------------------------------------------------

from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3  # Allows you to use the SQL commands on Python
import os       # Module that creates a connection between your operating system & Python

#CREATE THE FLASK APPLICATION
#------------------------------------------------------------------------

app = Flask(__name__)
app.secret_key = "math_masters_secret_123"  # signs and secures session cookies so no one can hack and bypass

# DATABASE SETUP
#------------------------------------------------------------------------
DB_NAME = "users.db" # stores the name of the database file

# function that sets up the database when the app first runs
def init_db(): #Creates the take for us in the database
    """
    Initialise the database and create the users table if it doesn't exist
    """ # only creates the database if it doesn't already exist
    if not os.path.exists(DB_NAME): 
        conn = sqlite3.connect(DB_NAME) # connects to the database file
        cursor = conn.cursor() # creates a cursor to run SQL commands
        cursor.execute(""" 
            CREATE TABLE users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL   
            )             
        """)  # creates the users table with id, username and password columns
        conn.commit()  # saves the changes to the database
        conn.close()  # closes the database connection

#Initialise the database
init_db()  #Use this function everytime we recall the table

#HOME PAGE ROUTE
#------------------------------------------------------------------------

#variables for login details
#USERNAME = "admin"
#PASSWORD = "1234"

#This route runs when the user goes to the login page
@app.route("/")

#name of function called home
def home():
#this shows the login.html page to the user
    return render_template("login.html")

@app.route("/addition") #This is the route for the addition learning page
def addition(): #creates the function called addition
    return render_template("addition.html")

@app.route("/subtraction") # This is the route for the subtraction learning page
def subtraction(): #creates the function called subtraction
    return render_template("subtraction.html")

@app.route("/division") # This is the route for the division learning page
def division(): #creates the function called division
    return render_template("division.html")

@app.route("/multiplication") # route for the multiplication learning page
def multiplication(): #creates the function called multiplication
    return render_template("multiplication.html")

@app.route("/home") # This is the route for the main homepage after login
def homepage(): #creates the function called homepage
    username = session.get("username", "Fellow Mathmathician") # gets the username from the session but show "Fellow Mathematician" if not found
    return render_template("home.html", username=username) # passes the username to the template so it can be displayed

@app.route("/practice") # This is the route for the practice mode selection page
def practice(): #creates the function called practice
    return render_template("practice.html")

@app.route("/learn") # This is the route for the learning topic selection page
def learn(): #creates the function called learn
    return render_template("learn.html")

@app.route("/logout", methods=["GET", "POST"]) # This is the route for logging out which accepts both GET and POST
def logout(): #creates the function called logout
    session.clear() # clears all session cookie data so the user is fully logged out
    return redirect(url_for("login"))  # sends them back to the login page
    
#This route runs when the login form is submitted
#it only accepts POST requests - because the form uses POST in HTML
@app.route("/login", methods=["GET", "POST"]) # route for the login page - handles both showing the form and processing it
def login(): #creates the function called login
    # check if the user is submitting the form (POST) or just visiting the page (GET)
    if request.method == "POST":
        # get the username and password typed in the form
        username = request.form["username"] # gets the username typed in the form
        password = request.form["password"] # gets the password typed in the form

        # connect to the database and search for a matching user
        conn = sqlite3.connect(DB_NAME)  # connects to the database
        cursor = conn.cursor()  # creates a cursor to run SQL commands
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))  # searches for a user that matches the entered username and password
        user = cursor.fetchone() # fetches the result - returns the user row if found, or None if not found
        conn.close() # closes the database connection

        # if a matching user was found, go to homepage
        if user:
            session["username"] = username #defines the username variable
            return redirect(url_for("homepage")) # redirects to the homepage
        # otherwise tell them the details were wrong
        else:
            return render_template("login.html", error="Invalid username or password")  #shows Invalid username or password if and error is sent from the login page
    
    else:
        # GET request - just show the login page
        return render_template("login.html", error=None)

@app.route("/success") # This is a simple route to confirm login was successful
def success(): #creates the function called success
    return "Login Successful!"

@app.route("/signup", methods=["GET", "POST"]) # This is the route for the signup page which handles both showing the form and processing it
def signup(): #creates the function called signup
    if request.method == "POST": # if the signup form was submitted
        username=request.form["username"] # gets the username typed in the signup form
        password=request.form["password"] # gets the password typed in the signup form

        conn = sqlite3.connect(DB_NAME) # connects to the database
        cursor = conn.cursor() # creates a cursor to run SQL commands
        cursor.execute(  # inserts the new user into the database
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit() # saves the new user to the database
        conn.close() # closes the database connection
        # returns a success message with a button to close the popup window
        return """ 
        <h3>User created successfully!</h3>
        <button onclick='window.close()'>Close Window</button>
        """

    # GET request: show signup form
    return """
    <html>
    <head><title>Sign Up</title></head>
    <body>
        <h2>Create New User</h2>
        <form method='POST'>
            <input type='text' name='username' placeholder='Username' required><br><br>
            <input type='password' name='password' placeholder='Password' required><br><br>
            <button type='submit'>Sign Up</button>
        </form>
    </body>
    </html>
    """
import random # imports the random module which is able to generate random numbers and operations

def generate_easy_question(): # function that generates a random addition or subtraction question with 2 digit numbers
    num1 = random.randint(1, 99)   # generates a random number from 1 to 99
    num2 = random.randint(1, 99)   # generates a random number from 1 to 99
    operation = random.choice(["+", "-"])   # randomly picks addition or subtraction

    # makes sure subtraction never goes negative
    if operation == "-" and num2 > num1:  # swaps the numbers if subtraction would give a negative answer
        num1, num2 = num2, num1

    question = f"{num1} {operation} {num2}"  # builds the question string
    answer = eval(question) # eval calculates the randomly generated question and saves it as the answer
    return question, answer # returns both the question and the answer

def generate_medium_question():  # function that generates a random question with all 4 operations and 2 digit numbers
    mediumnum1 = random.randint(1, 99)   # generates a random number from 1 to 99
    mediumnum2 = random.randint(1, 99)   # generates a random number from 1 to 99
    mediumoperation = random.choice(["+", "-", "/", "*"])   # randomly picks the operation

    if mediumoperation == "/":  # this code makes sure division gives whole numbers
        mediumnum2 = random.randint(1, 9) # generates a random number from 1 to 9
        mediumnum1 = mediumnum2 * random.randint(1, 9) # generates a random number from 1 to 9

    if mediumoperation == "-" and mediumnum2 > mediumnum1: mediumnum1, mediumnum2 = mediumnum2, mediumnum1 # swaps the numbers if subtraction would give a negative answer

    question = f"{mediumnum1} {mediumoperation} {mediumnum2}"  # builds the question string
    answer = int(eval(question)) # eval calculates the randomly generated question and saves it as the answer
    return question, answer # returns both the question and the answer

def generate_hard_question(): # function that generates a random question with all 4 operations and 3 digit numbers
    hardnum1 = random.randint(100, 999)   # generates a random number from 100 to 999
    hardnum2 = random.randint(100, 999)   # generates a random number from 100 to 999
    hardoperation = random.choice(["+", "-", "/", "*"])   # randomly picks the operation

    if hardoperation == "/": # This code makes sure division gives whole numbers
        hardnum2 = random.randint(10, 99) # This picks a 2 digit divisor
        hardnum1 = hardnum2 * random.randint(10, 99)  # This makes num1 a multiple of num2 so there's no remainder

    question = f"{hardnum1} {hardoperation} {hardnum2}" # builds the question string
    answer = int(eval(question)) # eval calculates the randomly generated question and saves it as the answer
    return question, answer # returns both the question and the answer

def generate_timeattack_question(): # function that generates a random question with all 4 operations and a 1 digit number
    timeattacknum1 = random.randint(1, 9)   # generates a random number from 1 to 9
    timeattacknum2 = random.randint(1, 9)   # generates a random number from 1 to 9
    timeattackoperation = random.choice(["+", "-", "/", "*"])   # randomly picks the operation

    if timeattackoperation == "/": # this code makes sure division gives whole numbers
        timeattacknum2 = random.randint(1, 9)  # picks a divisor
        timeattacknum1 = timeattacknum2 * random.randint(1, 9) # makes num1 a multiple of num2 so there's no remainder

    question = f"{timeattacknum1} {timeattackoperation} {timeattacknum2}" # builds the question string
    answer = int(eval(question)) # eval calculates the randomly generated question and saves it as the answer
    return question, answer # returns both the question and the answer

@app.route("/practice/easy", methods=["GET", "POST"]) # route for easy mode
def practice_easy(): # creates a function called practice_easy
    if request.method == "GET": # reset game when user first visits the page
        session["easy_score"] = 0  # resets the score to 0
        session["easy_question_number"] = 1 # resets the question number to 1
        question, answer = generate_easy_question()  # generates the first question
        session["easy_answer"] = answer # stores the correct answer in the session
        return render_template("easy.html", # renders the easy mode page with the first question
            question=question,
            question_number=1,
            score=0,
            feedback=None)

    if request.method == "POST": # handle answer when user submits
        user_answer = int(request.form["answer"]) # gets the answer the user typed in
        correct_answer = session.get("easy_answer") # gets the correct answer from the session
        score = session.get("easy_score", 0) # gets the current score from the session
        question_number = session.get("easy_question_number", 1) # gets the current question number from the session

        if user_answer == correct_answer: # check if answer is correct and update score
            score += 1  # adds 1 to the score for a correct answer
            feedback = "Correct!"
            feedback_type = "correct"
        else:  # score stays the same for an incorrect answer
            feedback = "Incorrect!"
            feedback_type = "incorrect"

        session["easy_score"] = score # saves the updated score to the session
        question_number += 1 # moves to the next question
        session["easy_question_number"] = question_number  # saves the updated question number to the session

        if question_number > 10: # if all 10 questions are done it shows game over screen
            return render_template("easy.html",
                question=None,
                question_number=10,
                score=score,
                feedback=None)
        
        question, answer = generate_easy_question()  # generate next question
        session["easy_answer"] = answer # stores the new correct answer in the session

        return render_template("easy.html",  # renders the page with the next question and feedback
            question=question,
            question_number=question_number,
            score=score,
            feedback=feedback,
            feedback_type=feedback_type)
    
@app.route("/practice/medium", methods=["GET", "POST"]) # route for medium mode 
def practice_medium(): # creates a function called practice_medium
    if request.method == "GET": # reset game when user first visits the page
        session["medium_score"] = 0 # resets the score to 0
        session["medium_question_number"] = 1 # resets the question number to 1
        question, answer = generate_medium_question() # generates the first question
        session["medium_answer"] = answer # stores the correct answer in the session
        return render_template("medium.html",  # renders the medium mode page with the first question
            question=question,
            question_number=1,
            score=0,
            feedback=None)

    if request.method == "POST": # handle answer when user submits
        user_answer = int(request.form["answer"]) # gets the answer the user typed in
        correct_answer = session.get("medium_answer") # gets the correct answer from the session
        score = session.get("medium_score", 0) # gets the current score from the session
        question_number = session.get("medium_question_number", 1) # gets the current question number from the session

        if user_answer == correct_answer: # check if answer is correct and update score
            score += 1 # adds 1 to the score for a correct answer
            feedback = "Correct!"
            feedback_type = "correct"
        else: # score stays the same for an incorrect answer
            feedback = "Incorrect!"
            feedback_type = "incorrect"

        session["medium_score"] = score # saves the updated score to the session
        question_number += 1 # moves to the next question
        session["medium_question_number"] = question_number # saves the updated question number to the session

        if question_number > 15: # if all 15 questions are done, show game over screen
            return render_template("medium.html",
                question=None,
                question_number=15,
                score=score,
                feedback=None)

        question, medanswer = generate_medium_question() # generate next question
        session["medium_answer"] = medanswer # stores the new correct answer in the session

        return render_template("medium.html",  # renders the page with the next question and feedback 
            question=question,
            question_number=question_number,
            score=score,
            feedback=feedback,
            feedback_type=feedback_type)

@app.route("/practice/hard", methods=["GET", "POST"]) # This is the route for hard mode
def practice_hard(): # creates a function called practice_hard
    if request.method == "GET": # reset game when user first visits the page
        session["hard_score"] = 0 # resets the score to 0
        session["hard_question_number"] = 1 # resets the question number to 1
        question, answer = generate_hard_question() # generates the first question
        session["hard_answer"] = answer  # stores the correct answer in the session
        return render_template("hard.html", # renders the hard mode page with the first question
            question=question,
            question_number=1,
            score=0,
            feedback=None)

    if request.method == "POST": # handle answer when user submits
        user_answer = int(request.form["answer"]) # gets the answer the user typed in 
        correct_answer = session.get("hard_answer")  # gets the correct answer from the session
        score = session.get("hard_score", 0)  # gets the current score from the session
        question_number = session.get("hard_question_number", 1) # gets the current question number from the session

        if user_answer == correct_answer: # check if answer is correct and update score
            score += 1 # adds 1 to the score for a correct answer
            feedback = "Correct!"
            feedback_type = "correct"
        else: # score stays the same for an incorrect answer
            feedback = "Incorrect!"
            feedback_type = "incorrect"

        session["hard_score"] = score # saves the updated score to the session
        question_number += 1 # moves to the next question
        session["hard_question_number"] = question_number  # saves the updated question number to the session

        if question_number > 20: # if all 20 questions are done, show game over screen
            return render_template("hard.html",
                question=None,
                question_number=20,
                score=score,
                feedback=None)

        question, hardanswer = generate_hard_question() # generate next question
        session["hard_answer"] = hardanswer # generate next question

        return render_template("hard.html", # renders the page with the next question and feedback
            question=question,
            question_number=question_number,
            score=score,
            feedback=feedback,
            feedback_type=feedback_type)
    
@app.route("/practice/timeattack", methods=["GET", "POST"]) # This is a route for time attack mode
def practice_timeattack(): # creates a function called practice_timeattack
    if request.method == "GET":  # resets the game when the user first visits the page
        session["timeattack_score"] = 0 # resets the score to 0
        session["timeattack_question_number"] = 1  # resets the question number to 1
        session["timeattack_start"] = __import__('time').time()  # store start time
        question, answer = generate_timeattack_question()  # generates the first question
        session["timeattack_answer"] = answer  # stores the correct answer in the session
        return render_template("timeattack.html",  # renders the time attack page with 60 seconds on the timer
            question=question,
            question_number=1,
            score=0,
            feedback=None,
            time_left=60)

    if request.method == "POST": # handles the answer when the user submits
        import time # imports the time module

        start_time = session.get("timeattack_start", time.time())  # check if timer has run out
        elapsed = time.time() - start_time  # calculates how many seconds have passed since the game started
        time_left = max(0, int(60 - elapsed))   # calculates how many seconds are left

        if request.form.get("timeout") == "true" or time_left <= 0:  # if timeout form submitted or time is up
            score = session.get("timeattack_score", 0) # gets the final score from the session
            return render_template("timeattack.html",  # renders the game over screen with the final score
                question=None,
                question_number=0,
                score=score,
                feedback=None,
                time_left=0)

        user_answer = int(request.form["answer"]) # gets the answer the user typed in
        correct_answer = session.get("timeattack_answer") # gets the correct answer from the session
        score = session.get("timeattack_score", 0) # gets the current score from the session
        question_number = session.get("timeattack_question_number", 1) # gets the current question number from the session

        if user_answer == correct_answer: # checks if the user's answer matches the correct answer
            score += 1 # adds 1 to the score for a correct answer
            feedback = "Correct!"
            feedback_type = "correct"
        else:  # score stays the same for an incorrect answer
            feedback = "Incorrect!"
            feedback_type = "incorrect"

        session["timeattack_score"] = score # saves the updated score to the session
        question_number += 1 # moves to the next question
        session["timeattack_question_number"] = question_number # saves the updated question number to the session

        question, answer = generate_timeattack_question()  # generates the next question
        session["timeattack_answer"] = answer # stores the new correct answer in the session

        return render_template("timeattack.html",  # renders the page with the next question and feedback
            question=question,
            question_number=question_number,
            score=score,
            feedback=feedback,
            feedback_type=feedback_type,
            time_left=time_left)
    
if __name__ == "__main__":  # makes sure the server only runs when this file is executed directly
    app.run(debug=True, port=4000)
