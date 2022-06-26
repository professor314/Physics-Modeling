# <---This is a comment character.  All text on a line
#     after a comment character is ignored by Python.

#define a function to add two numbers. This is only
#   a definition and does not actuall do anything until
#   the function is "called" somewhere later in the program
#   The x and y in parentheses is called the "parameter list".
#   The "return value" is the value of the expression in the "return" statement,
#   in this case, the sum of the two parameters that were "passed in" to the 
#   function.

def add(x,y):
     return x+y

# note the 'return' line must be indented to put it in the body of the function

#The next line is NOT indented so it is not part of the loop
#   It is a "function call" which actually executes the function
#   and substitutes the return value in place of the call.

sum = add(2,3)  # Call the function to use it.
print sum       # this should print a '5'
 
#Functions can have default values assigned to their parameters

def add(x=0,y=0):
     return x+y

#now call the new verion of add() with no arguments
#default values will be used for its parameters

print add()   # this should print a '0'

	
