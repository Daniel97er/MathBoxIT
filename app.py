import math
from random import randrange
from flask import Flask, render_template, request, redirect, flash

# Flask instance configuration
app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

app.secret_key = "super secret key"


# Homepage
@app.route("/")
def index():
    return render_template("index.html")

# Miller-Rabin-Test
@app.route("/miller_rabin_test", methods=["GET", "POST"])
def miller_rabin_test():

  if request.method == "POST":

    # Get data from registration.html
    number = int(request.form.get("prime"))
    
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

    # Check if user input is a prime number
    result = ""

    if miller_rabin_tester_test(number):
      result = 1
    else:
      result = 0

    # Render page with result
    print(result)
    return render_template("miller_rabin_test.html", result=result)

  else:
    # Render page without result
    return render_template("miller_rabin_test.html")

# Prime factors
@app.route("/prime_factors", methods=["GET", "POST"])
def prime_factors():

    def prime_factorization(number):
        # Return three lists with prime factorials, exponents and one index list for jinja 
  
        # Check zero and one by default
        if number == 0:
           return [0], [1]

        if number == 1:
  	       return [1], [1]

        # Create two lists for prime factors and exponents
        factor_list = []
        exponent_list = []

        # Get prime numbers up to number 
        prime_list = prime_test(number)
  
        # Go through primes and check if it is a prime factor and possibly add to prime factors list
        for i in prime_list:
          if number % i == 0:
            factor_list.append(i)

        # Calculate the number of exponent for the respective prime factor
        for i in factor_list:
          counter = 0
          temp_number = number 
          # Keep dividing the number until it no longer fits in
          while temp_number % i == 0:
            temp_number //= i
            counter += 1
          exponent_list.append(counter) 

        # Create index list for jinja template for loop
        index_list = [i for i in range(len(factor_list))]
  
        return factor_list,exponent_list, index_list


    def prime_test(number):
        # Return list of primes up to number (Sieve of Eratosthenes)

        prime_test_list = []

        # Go through all numbers 
        for i in range(2, number+1):

         # Set tester to false to check if current i is prime
         tester = False 
    
         # Go up to square root because of efficiency 
         for j in range(2,int(math.sqrt(i))+1):
             # If there is a dividend so i is not prime 
             if i % j == 0:
                 tester = True 
                 # Stop loop if i is not prime
                 break
    
         # If tester in the end of the loop is false so i is a prime
         if tester == False:
             prime_test_list.append(i)

  
        return prime_test_list
    
    p_factors, p_exponents, index_list = prime_factorization(2)
    return 

