import instrumentbase
from rma import rma
from importlib import import_module

def mainmenu():
	"""
	Displays the main menu for the program with header and list of instruments.
	The instrument list is generated dynamically from a list of instruments that
	are known to the instrumentbase.py module.
	"""
	print("\n")
	print("-" * 20, "OOI CGSN INSTRUMENT", "-" * 20)
	print(" " * 14, "AUTOMATED INSTRUMENT PROCEDURES")
	print(" " * 23, "Version 1.0a")
	print("-" * 61)
	print("Select an instrument:")
	menuid = []   # Dynamic menu. See instrumentbase module...
	for i, inst in enumerate(instrumentbase.known_inst):
		menuid.append(str(i+1))
		print("%s) %s" % (menuid[i], inst.upper()))
	print("R) RMA and SHIPPING")
	print("Q) Quit")
	selection = input("Enter your selection: ")
	
	if selection.lower() == 'q':
		return None
	elif selection.lower() == 'r':
		return 'rma'
	elif selection in menuid:
		return selection
	else:
		return 999
		
def main():
	while True:
		selection = mainmenu()
		if not selection:
			break
		elif selection == 999:
			input("\nError! Unrecognized entry [Press ENTER to continue]...")
			continue
		elif selection == 'rma':
			rma.main()
		else:
			chosen_instrument = instrumentbase.known_inst[int(selection)-1]
			print("\nYou have selected %s" % chosen_instrument.upper())
			response = input("Is this correct? [y]/n ")
			if response.lower() == 'n':
				continue
			else:
				# Dynamic loading of the module for the selected instrument, then
				# defining 'instrument' as an instance of instrument Class
				# from that module. The Class name must be the Capitalized
				# module name. This must be defined in the relevant module.
				instrmod = import_module('instruments.%s' % chosen_instrument)
				instrclass = getattr(instrmod, chosen_instrument.capitalize())
# 				instrument = instrclass(chosen_instrument)
				instrument = instrclass()
				
				# With an instrument defined, the available procedures will be
				# presented dynamically by the instrumentbase module, where one will
				# be chosen by the user and further actions will happen...
				instrument.select_proc()
			
			
			
main()
print("Good bye!\n")