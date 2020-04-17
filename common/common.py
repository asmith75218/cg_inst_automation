from . import userinput 

# Use this function to prompt the user for a name to use on forms and documents. It
# has built-in input validation (see common/userinput.py for validation details).
#
def set_username():
	"""
	Prompt the user for a name to use on forms and documents.
	"""
	while True:
		username = userinput.Userinput(input("Enter your name: "))
		if username.valid_name():
			return username.user_response
		else:
			print("Unknown error! Try again.")



# Use this function to increment or set the starting form number to use on forms and
# documents. It has built-in input validation (see common/userinput.py for
# validation details).
#
def set_formnumber(formnumber=None):
	"""Prompt the user for a form number, or increment it if it already exists."""
	while not formnumber:
		# Prompt user and test for valid input...
		formnumber = userinput.Userinput(input("Enter the five-digit form number (ex: 00123): "))
		if formnumber.valid_range(range(1, 100000)):
			return str(int(formnumber.user_response)).rjust(5, '0')
		else:
			formnumber = None
			input("\nError! Unrecognized entry [Press ENTER to continue]...")
	# increment the form number...
	return str(int(formnumber)+1).rjust(5, '0')
