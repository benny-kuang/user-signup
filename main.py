# Create user form submission
# Following should trigger an error:
# User leaves any of the following field empty: username, pw, verify pw
# Username or pw is not valid (ex:contains space character or consists of less than 3 chars or 20+ chars)
# User pw and pw confirmation do not match
# User provides email but not valid (note: email field may be empty, but if content, content must be validated.)
#     Criteria for valid email is single @, single ., no spaces and between 3 and 20 char long
# Each feedback should be next to the field that it refers to.
# For the username and email fields, you should clear them, for security reasons
# If all input is valid, you should show the user a welcome page that uses the username input to display welcome message of: "Welcome, {username}"
# Use the templates to render the HTML for your web app

from flask import Flask, request, render_template, redirect
import cgi
import os

app = Flask(__name__)
app.config['DEBUG'] = True

def validate_username(username):
    username, username_error = username, ""
    if len(username) < 3:
        username_error = "plz use 3 or more chars"
        username = "" 
    if len(username) > 20:
        username_error = "plz use less than 20 chars"
        username = ""
    for char in username:
        if char == " ":
            username_error = "plz no spaces"
            username = ""
    return username, username_error
def validate_password(password, password_verify):
    password, password_error = password, ""
    password_verify, password_verify_error = password_verify, ""
    if len(password) < 3:
                password_error = "plz use 3 or more chars"
                password = ""
    if len(password) > 20:
        password_error = "plz use less than 20 chars"
        password = ""
    for char in password:
        if char == " ":
            password_error = "plz no spaces"
            password = ""
    if password_verify != password:
        password_verify_error = "Password does not match"
        password_verify = ""
    return password, password_error, password_verify, password_verify_error
def validate_email(email):
    email, email_error = email, ""
    at = 0
    dot = 0
    if len(email) != 0:
        if len(email) < 3:
            email_error = "plz use 3 or more chars"
            email = ""
        if len(email) > 20:
            email_error = "plz use less than 20 chars"
            email = ""
        for char in email:
            if char == "@":
                at += 1
                if at > 1:
                    email_error = "plz only use 1 @ symbol!"
                    email = ""
            if char == ".":
                dot += 1
                if dot > 1:
                    email_error = "plz only use 1 period!"
                    dot = ""
            if char == " ":
                email_error = "plz no spaces!"
                email = ""
        if at == 0:
            email_error = "plz use 1 @ symbol!"
            email = ""
        if dot == 0:
            email_error = "plz use a period!"
            email = ""
    return email, email_error

@app.route('/', methods=["POST", "GET"])
def sign_up():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        username, username_error = validate_username(request.form["username"])
        email, email_error = validate_email(request.form["email"])
        password, password_error, password_verify, password_verify_error = validate_password(request.form["password"], request.form["password_verify"])
        if not username_error and not password_error and not password_verify_error and not email_error:
            return redirect("/welcome?username={0}".format(username))
        else:
            return render_template("index.html",
            username = username, username_error = username_error,
            password = password, password_error = password_error,
            password_verify = password_verify, password_verify_error = password_verify_error,
            email = email, email_error = email_error)

@app.route('/welcome', methods=['GET'])
def welcome():
    username = request.args.get('username')
    return render_template('welcome.html', username = username)

app.run()