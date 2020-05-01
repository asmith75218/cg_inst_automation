from . import userinput


# Dynamic menu
#
#
def dynamicmenu(msg, menuoptions, lastitem, header):
	"""
	Displays a dynamically generated menu and returns the letter or number used to
	index the menu option as a string. Called by dynamicmenu_get.
	"""
	if header: print(header)
	print("%s:" % msg)
	menuid = []   # Dynamic menu...
	for i, option in enumerate(menuoptions):
		menuid.append(str(i+1))
		print("%s) %s" % (menuid[i], option))
	print("%s) %s" % (lastitem[0].upper(), lastitem[1].title()))
	selection = input("Enter your selection: ")
	
	if selection.lower() == lastitem[0].lower():
		return None
	elif selection in menuid:
		return selection
	else:
		return 999

def dynamicmenu_get(msg, menuoptions, lastitem=('B', 'Go Back'), header=None):
	"""
	Executes a dynamically generated menu calling on dynamicmenu function to
	display the options and pass back a selection.
	
	Params:
	msg (string)		Required. Message or prompt to display above the menu
						options. Suggested message might be "Select an instrument"
						or similar. Do not include space, colon, dash, etc at
						the end.
	menuoptions (list)	Required. List of strings to display as menu options. Do
						not include index numbers or letters in the string, as
						these will be generated programmatically. Strings will
						appear in the order they occur in the list, so if this is
						important, sort the list before passing to this function.
	lastitem (tuple)	Two-item tuple or list of strings used to generate the
						last menu option. The first item shall be the letter or
						number used to index the option in the menu. The second
						item shall be the text to display. Capitalizes first
						letters. Defaults to ('B', 'Go Back') when not provided.
	header (string)		Optional. Text header to display before msg and all menu
						options. No formatting will be applied, so format the
						string before passing to this function if desired.
						
	Returns:
	(string)			As a string, the index value of the selection from
						menuoptions list.
	(None)				If lastitem is selected.
		
	"""
	while True:
		selection = dynamicmenu(msg, menuoptions, lastitem, header)
		if not selection:
			return None
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
		username = userinput.Userinput(input("\nEnter your name: "))
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
		formnumber = userinput.Userinput(input("\nEnter the five-digit form number (ex: 00123): "))
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

