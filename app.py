from flask import Flask, render_template, request, redirect, flash, session
from flask_session import Session
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

# Flask instance configuration
app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

app.secret_key = "super secret key"

# Database started
#db = SQL("sqlite:///database.db")


# Homepage / Purchase documentation
@app.route("/")
def index():

    # Get global data from database
    a = 5 
    b = 9
    return render_template("index.html")