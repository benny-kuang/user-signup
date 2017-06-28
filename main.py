# Create user form submission
# Following should trigger an error:
# User leaves any of the following field empty: username, pw, verify pw
# Username or pw is not valid (ex:contains space character or consists of less than 3 chars or 20+ chars)
# User pw and pw confirmaiton do not match
# User provides email but not valid (note: email field may be empty, but if content, content must be validated.)
#     Criteria for valid email is single @, single ., no spaces and between 3 and 20 char long
# Each feedback should be next to the field that it refers to.
# For the username and email fields, you should clear them, for security reasons
# If all input is valid, you should show the user a welcome page that uses the username input to display welcome message of: "Welcome, {username}"
# Use the templates to render the HTML for your web app

from flask import Flask, request, render_template, redirect
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def index():
    return render_template("index.html", username='', username_error='' )

@app.route('/', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        username = request.form['username']
        # password = request.form['password']
        # verify_pass = request.form['verify_password']
        # email = request.form['email']
        username_valid = True
        # password = True
        # verify_password_valid = True
        # email_valid = True

        username_error = ''

        if len(username) < 3:
            username_error = "plz use more than 3 chars"
            username = ""
            username_valid = False            
        if len(username) > 20:
            username_error = "plz use less than 20 chars"
            username_valid = False
        for char in username:
            if char == " ":
                username_error = "plz no spaces"
                username_valid = False

        if username_valid == False:
            return render_template("index.html", username='', username_error = username_error)
        
        return redirect('/welcome?username={}'.format(username) )

@app.route('/welcome', methods=['GET'])
def welcome():
    username = request.args.get('username')
    return render_template('welcome.html')

app.run()