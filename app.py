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
@app.route("/miller_rabin_test") 
def miller_rabin_test(): 

  # Miller-Rabin primality test (probabilistic primality test)
  # Based on the principle of prime modulo and that X*X=1 has maximum only
  # two solutions one and minus one 

  def miller_rabin_tester(number):
    # Miller-Rabin-Test 
    # If the result is negative then it is definitely not a prime number. 
    # If the result is positive then possibly a false positive result 

    prime_help = number - 1
    counter = 0

    # Divide prime_help by two, while it is even
    # and increase the counter each time
    while prime_help % 2 == 0:
      prime_help //= 2
      counter += 1

    # Get random number between 2 and number 
    random_number = randrange(2, number)
