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

        # When random_number power of prime_help  modulo number comes out equal to one, 
        # in the first try, it is most likely a prime number
        if (random_number ** prime_help) % number == 1:
          return True 

        # While counter greater zero test if result is -1 or 1 and decide then 
        while counter > 0:
          if (random_number ** prime_help) % number == number -1:
            return True

          if (random_number ** prime_help) % number == 1:
            return False 
    
          random_number **= 2
          counter -= 1

        # Return false if no 1 or -1 appears 
        return False


    def miller_rabin_tester_test(number):
        # Runs the miller-rabin-test 15 times to minimize 
        # the chance of false positive results

        # Return false if number is apparently not prime 
        if number < 2 or number % 2 == 0:
          return False 

       # Run Miller-Rabin-test 15 times to test 
        for i in range(15):
          if not miller_rabin_tester(number):
            # Return false if number not prime 
            return False 

       # Return true when most likely prime 
        return True  
