from . import userinput


# Dynamic menu
#
#
def dynamicmenu(msg, menuoptions, lastitem, header):
	if header: print(header)
	print("%s:" % msg)
	menuid = []   # Dynamic menu...
	for i, option in enumerate(menuoptions):
		menuid.append(str(i+1))
		print("%s) %s" % (menuid[i], option))
	print("%s) %s" % (lastitem[0].upper(), lastitem[1].capitalize()))
	selection = input("Enter your selection: ")
	
	if selection.lower() == lastitem[0].lower():
		return None
	elif selection in menuid:
		return selection
	else:
		return 999

def dynamicmenu_get(msg, menuoptions, lastitem=('B', 'Go Back'), header=None):
	while True:
		selection = dynamicmenu(msg, menuoptions, lastitem, header)
		if not selection:
			break
		elif selection == 999:
			input("\nError! Unrecognized entry [Press ENTER to continue]...")
			continue
		else:
			print("\nYou have selected %s" % menuoptions[int(selection)-1])
			response = input("Is this correct? [y]/n ")
			if response.lower() == 'n':
				continue
			else:
				return str(int(selection) - 1)

	

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

# Common messages
#
#
usercancelled = "\nOperation cancelled by user. [Press ENTER to continue]..."

