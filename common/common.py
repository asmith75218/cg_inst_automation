from . import userinput
from serial import Serial
from serial.tools import list_ports


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

# The following functions provide access to serial ports...
#
def set_serialport():
	ports = [port for port in list_ports.comports()]
	portmenu = ["%s - %s" % (port.device, port.description) for port in ports]
	try:
		port_id = int(dynamicmenu_get("Select an available port", portmenu))
	except TypeError:
		return None
	return ports[port_id]

def serialport_open(port, baudrate):
	"""Open connection to a serial port and start logging to a file."""
	print("Connecting to %s at %d baud..." % (port, baudrate))
	try:
		ser = Serial(port[0], baudrate, timeout=5)
		print("Connected to %s." % port)
		return ser
	except BaseException as msg:
		input("\nError! %s [Press ENTER to continue]..." % msg)
		return None
