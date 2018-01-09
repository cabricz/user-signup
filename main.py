from flask import Flask, request, redirect, render_template
import cgi
import os
import re

app = Flask(__name__)
app.config['DEBUG'] = True

def isempty(text):
    if len(text) == 0:
        return True
    else:
        return False

def isvalid(text):
    if len(text) < 3 or len(text) > 20:
        return False
    else:
        if not re.match("[\w-]+$", text):
            return False
        else:
            return True

def isemail(text):
    if len(text) < 3 or len(text) > 20:
        return False
    else:
        if not re.match("[^@]+@[^@]+\.[^@]+", text):
            return False
        else:
            return True

def ismatch(text1, text2):
    if not text1 == text2:
        return False
    else:
        return True

@app.route("/")
def display_signup_form():
    return render_template("form.html", title="User Signup")

@app.route("/", methods=["POST", "GET"])
def index():
    username = request.form["username"]
    password = request.form["password"]
    conf_password = request.form["conf_password"]
    email = request.form["email"]

    username_error = ""
    password_error = ""
    conf_password_error = ""
    email_error = ""

    if isempty(username):
        username_error = "Please enter username."
        username = ""
    else:
        if not isvalid(username):
            username_error = "Please enter valid username. 3-20 characters. No special characters or spaces."
            username = ""
    
    if isempty(password):
        password_error = "Please enter a password."
        password = ""
    else:
        if not isvalid(password):
            password_error = "Please enter valid password. 3-20 characters.  No special characters or spaces."
            password = ""
    
    if isempty(conf_password):
        conf_password_error = "Please confirm password."
        conf_password = ""
    else:
        if not ismatch(password, conf_password):
            conf_password_error = "Passwords must match."
            conf_password = ""

    if not isempty(email):
        if not isemail(email):
            email_error = "Please enter valid email."
            email = ""
    
    if not username_error and not password_error and not conf_password_error and not email_error:
        return redirect("/welcome?username={0}".format(username))
    else:
        return render_template("form.html", username=username, password=password, conf_password=conf_password, email=email, username_error=username_error, password_error=password_error, conf_password_error=conf_password_error, email_error=email_error)

@app.route("/welcome")
def welcome():
    username = request.args.get("username")
    return render_template("welcome.html", title="Welcome", username=username)
    
app.run()