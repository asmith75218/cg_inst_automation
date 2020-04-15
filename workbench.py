# Available instrument types...
import instruments
import pkgutil

known_inst = [name for finder, name, ispkg in pkgutil.iter_modules(instruments.__path__)]

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
				print("Spammit! Try again...")
				continue
			else:
				chosen_proc = self.proctypes[int(selection)-1]
				print("You have selected %s" % chosen_proc.upper())
				response = input("Is this correct? [y]/n ")
				if response.lower() == 'n':
					continue
				else:
					print("Spam!")
					getattr(self, chosen_proc)()




# def spam():
# 	while not time_to_quit:
# 		print("\r\nCG AUTO QCT")
# 		print("MAIN MENU")
# 		print("---------")
# 		print("1) Test an instrument")
# 		print("2) Configure serial port")
# 		print("3) Exit")
# 		selection = input("Enter your selection: ")
# 		if selection == '1':
# 			if not port:
# 				port = 'foo'
# 				#port = select_port()
# 				if not port:
# 					continue
# 			username = input("What is your name?: ")
# 			while True:
# 				formnumber = 'spam!'
# 				#formnumber = set_formnumber(formnumber)
# 				print("Voila! Test complete!")
# 				#print(ctdmo_qct_test(port, username, formnumber))
# 				again = input("Would you like to test another instrument? y/[n] ")
# 				if again != "y":
# 					formnumber = None
# 					break
# 				input("Type ENTER to begin the next test...")
# 		elif selection == '2':
# 			port = 'foo'
# 			#port = select_port()
# 			print("Selected port is %s." % port)
# 		elif selection == '3':
# 			time_to_quit = True
# 			print("Good bye!")
# 		else: print("Error! Invalid entry.\r\n")
