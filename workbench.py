# from common import 

# Available instrument types... -------------------------------
import instruments
import pkgutil

known_inst = [name for finder, name, ispkg in pkgutil.iter_modules(instruments.__path__)]
# -------------------------------------------------------------

# High level instrument class for properties shared across instrument types
class Instrument:
	def __init__(self, name):
		self.name = name
		
	def explode(self):
		print("Boom!")
		
	def mainmenu(self, proctypes):
		print("\n")
		print("-" * 17, "INSTRUMENT MENU: %s" % self.name.upper().ljust(7), "-" * 18)
		print("Select a procedure:")
		menuid = []
		for i, proc in enumerate(proctypes):
			menuid.append(str(i+1))
			print("%s) %s" % (menuid[i], proc.upper()))
		print("B) Go Back")
	
		selection = input("Enter your selection: ")
	
		if selection.lower() == 'b':
			return None
		elif selection in menuid:
			return selection
		else:
			return 999
	
	def select_proc(self):
		while True:
			selection = self.mainmenu(self.proctypes)
			
			if not selection:
				break
			elif selection == 999:
				input("\nError! Unrecognized entry [Press ENTER to continue]...")
				continue
			else:
				chosen_proc = self.proctypes[int(selection)-1]
				print("\nYou have selected %s" % chosen_proc.upper())
				response = input("Is this correct? [y]/n ")
				if response.lower() == 'n':
					continue
				else:
					getattr(self, chosen_proc)()
	
	

