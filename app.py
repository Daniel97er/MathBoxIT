import math
from random import randrange
from flask import Flask, render_template, request, flash

# Flask instance configuration
app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

app.secret_key = "super secret key"


# Homepage
@app.route("/", methods=["GET"])
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
            for _ in range(15):
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

    if request.method == "POST":

        entered_number = int(request.form.get("prime_factor"))
        
        def prime_factorization(number):
            # Return three lists with prime factorials, exponents and one index list for jinja 
      
            
            # Check zero and one by default
            if number == 0:
                # factor, exponent and index
                return [0], [1], [0]

            if number == 1:
                # factor, exponent and index
                return [1], [1], [0]

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
                if tester is False:
                    prime_test_list.append(i)

      
            return prime_test_list
        
        # Prime factor, prime exponent and index list
        p_factors, p_exponents, index_list = prime_factorization(entered_number)

        return render_template("prime_factors.html", p_factors=p_factors, p_exponents=p_exponents, index_list=index_list)

    else:
        return render_template("prime_factors.html")

# ISBN-10 TEST
@app.route("/isbn_test", methods=["GET", "POST"])
def isbn_test():
  
    if request.method == "POST":
        # Get user input
        number = request.form.get("isbn")

        # Check if it is a ten-digit number
        if len(number) != 10:

            # Flash message to help the user
            flash("Please enter a ten-digit ISBN-number without space or other signs")

            return render_template("isbn_test.html")

        for i in number:
            if not ((ord(i) >= 48 and ord(i) <= 57) or (ord(i) == 88) or (ord(i) == 120)):
                flash("Not valid sign was entered, please try again")

                return render_template("isbn_test.html")

        def isbn_test(isbn):
            # Check if there is a valid ISBN-10 number

            sum = 0
            counter = 1
            # Get isbn numbers without check digit
            isbn_list = isbn[:9]

            # Go through numbers and calculate the value
            for i in isbn_list:
                sum += counter*int(i)
                counter += 1

            # If sum modulo 11 is not equal to check digit it is a not correct isbn
            result = sum % 11

            temp = -1
            
            # Check if check-digit is not int
            if isbn[9] == "x" or isbn[9] == "X":
                temp = 10
            else:
                temp = int(isbn[9])

            # Return result
            if result == temp:
                return 1
            else:
                return 0

        result = isbn_test(number)

        return render_template("isbn_test.html", result=result)
      
    else:
        return render_template("isbn_test.html")


# Euclidean algorithm
@app.route("/euclidean_algorithm", methods=["GET", "POST"])
def euclidean_algorithm():

    if request.method == "POST":

        # Get user data from euclidean_algorithm page
        number1 = int(request.form.get("euclidean_number1"))
        number2 = int(request.form.get("euclidean_number2"))

        def euclidean_algorithm_func(number1, number2):
            # Return GCD from number1 and number2

            # Calculate with modulo while is possible
            while number2 != 0:
                temp = number1%number2
                # swap numbers 
                number1 = number2
                number2 = temp

            # Return GCD
            return number1

        result = euclidean_algorithm_func(number1, number2)
          
        return render_template("euclidean_algorithm.html", result=result)

    else:
        return render_template("euclidean_algorithm.html")


# Extended Euclidean algorithm
@app.route("/extended_euclidean_algorithm", methods=["GET", "POST"])
def extended_euclidean_algorithm():

    if request.method == "POST":

      # Because of user data
        try:
            # Get user data from extended_euclidean_algorithm page
            number1 = int(request.form.get("extended_euclidean_number1"))
            number2 = int(request.form.get("extended_euclidean_number2"))

            def extended_euclidean_algorithm(number1, number2):
                # Extended euclidean algorithm return in this function GCD and linear combination 

                # Avoid error
                if number2 == 0:
                    return(number1, 1, 0)

                # Quotient list 
                q_list = []
                # Counter for calculation
                counter1 = 0

                # GCD calculation and documentation
                while number2 != 0:
                    q_list.append(number1 // number2)
                    number3 = number2
                    number2 = number1 % number2
                    number1 = number3
                    counter1 += 1

                # Variable for the backward algorithm
                x = 0
                y = 1
                # List of y
                y_list_temp = [1]
                # counter2 to get the right index from list
                counter2 = 0

                # Go backward through list and calculate the linear combinations
                while counter1 > 1:
                    # Calculate y and add in the list then calculate x
                    y = x - q_list[counter1 - 2] * y_list_temp[counter2]
                    y_list_temp.append(y)
                    x = y_list_temp[counter2]
                    # Update counters
                    counter2 += 1
                    counter1 -= 1
        

                return(number1, x, y)

            result, result_number1, result_number2 = extended_euclidean_algorithm(number1, number2)

            return render_template("extended_euclidean_algorithm.html", number1=number1, number2=number2, result=result, result_number1=result_number1, result_number2=result_number2)
        
        except:
            flash("Please enter number in the number fields")
          
            return render_template("extended_euclidean_algorithm.html")
    else:
        return render_template("extended_euclidean_algorithm.html")

# Decimal to numerial system
@app.route("/decimal_to_numeral_system", methods=["GET", "POST"])
def decimal_to_numeral_system():
  
    if request.method == "POST":

        # Get user data from decimal_to_numeral_system page
        decimal_number = int(request.form.get("decimal_number"))
        numeral_system = int(request.form.get("numeral_system"))

        def decimal_to_numeral_system_func(decimal_number, numeral_system):
            # Function converts decimal number into another numeral system

            # Standard cases and error checking
            if decimal_number == 0:
                return [0]

            if decimal_number < 0:
                flash("Please enter a decimal number higher zero")
                return render_template("decimal_to_numeral_system.html")

            if numeral_system <= 1:
                flash("Please enter a numeral system higher one")
                return render_template("decimal_to_numeral_system.html")

            # Empty list for result
            list1 = []

            # Modulo calculating while decimal_number greater zero
            # and then check if zero or result from modulo calculating in list
            while decimal_number >= 1:
                if decimal_number % numeral_system == 0:
                    list1.append(0)
                else:
                    list1.append(decimal_number % numeral_system)
   
                # Integer division
                decimal_number //= numeral_system

            # Return the flipped list for right result
            return list1[::-1]

        # Get list with decimal to numerial system result
        result_list = decimal_to_numeral_system_func(decimal_number, numeral_system)

        # Create a integer from the result list
        string_result = ""

        for index in result_list:
            string_result += str(index)
   
        result = int(string_result)


        return render_template("decimal_to_numeral_system.html", result=result, decimal_number=decimal_number, numeral_system=numeral_system)

    else:

        return render_template("decimal_to_numeral_system.html")


# Numeral system to decimal
@app.route("/numeral_system_to_decimal", methods=["GET", "POST"])
def numeral_system_to_decimal():

    if request.method == "POST":

        # Get user data from numeral system to decimal page
        numeral_system = int(request.form.get("num_system"))
        number = int(request.form.get("number"))

        def numeral_system_to_decimal(number, numeral_system):
            # Function converts number from a numeral system into decimal
    
            # Check if user input number higher than numeral system
            for i in str(number):
                if numeral_system <= int(i):
                    flash("Some digits from number higher than numeral system ")
                    return render_template("numeral_system_to_decimal.html")
            
            counter = 0
            sum = 0
    
            # Get string backward list of number
            number_backward = str(number)[::-1]
    
            # Calculate the decimal value
            for index in number_backward:
                sum += int(index) * (numeral_system**counter)
                counter += 1
        
            # Return decimal value
            return sum

        result = numeral_system_to_decimal(number, numeral_system)

        return render_template("numeral_system_to_decimal.html", result=result)

    else:
        return render_template("numeral_system_to_decimal.html")


# Decimal to binary
app.route("/decimal_to_binary", methods=["GET", "POST"])
def decimal_to_binary():
    
    if request.method == "POST":

        def decimal_to_binary(decimal_num):
            # Funktion converts decimal number to binary number
  
            # Standard cases 
            if decimal_num <= 0:
                flash("Please enter a decimal number higher than zero")
  	            return render_template("decimal_to_binary.html")
  	
            binary_list = []

            # Calculate with modulo the binary values and append to list
            while decimal_num != 0:
                binary_list.append(decimal_num % 2)
                decimal_num //= 2
  
            # List backwards is the right order
            binary_list = binary_list[::-1] 
  
            # Convert int list into string 
            binary_string_list = [str(x) for x in binary_list]
  
            # Convert string list into a string
            binary_string = "".join(binary_string_list)
  
            # Convert string into integer
            binary_num = int(binary_string)
  
            return binary_num
        
        result = decimal_to_binary(decimal_num)
        
        return render_template("decimal_to_binary.html", result=result)

    else:
        return render_template("decimal_to_binary.html")

  

