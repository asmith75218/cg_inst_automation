from . import userinput 
from serial.tools import list_ports

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


# The following functions provide access to serial ports...
#
def serialport_menu(ports):
	print("Select an available port:")
	menuid = []   # Dynamic menu...
	for i, port in enumerate(ports):
		menuid.append(str(i+1))
		print("%s) %s - %s" % (menuid[i], port.device, port.description))
	print("X) Cancel")
	selection = input("Enter your selection: ")
	
	if selection.lower() == 'x':
		return None
	elif selection in menuid:
		return selection
	else:
		return 999

def set_serialport():
	ports = [port for port in list_ports.comports()]
	
	while True:
		selection = serialport_menu(ports)
		if not selection:
			break
		elif selection == 999:
			input("\nError! Unrecognized entry [Press ENTER to continue]...")
			continue
		else:
			chosen_port = ports[int(selection)-1]
			print("\nYou have selected %s - %s" % (chosen_port.device, chosen_port.description))
			response = input("Is this correct? [y]/n ")
			if response.lower() == 'n':
				continue
			else:
				return chosen_port
