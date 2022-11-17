from flask import Flask, render_template, request, redirect, flash
from random import randrange 

# Flask instance configuration
app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

app.secret_key = "super secret key"


# Homepage
@app.route("/")
def index():

    # Get global data from database
    a = 5 
    b = 9
    return render_template("index.html")

# Miller-Rabin-Test 
# @app.route("/miller_rabin_test") 
def miller_rabin_test():
