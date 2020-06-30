from common import common

# Available instrument types... -------------------------------
import instruments
import pkgutil

known_inst = [name for finder, name, ispkg in pkgutil.iter_modules(instruments.__path__)]
# -------------------------------------------------------------

# High level instrument class for properties shared across instrument types
class Instrument:
	def __init__(self):
		pass
		
	def explode(self):
		print("Boom!")
			
	def select_proc(self):
		while True:
			header = ''.join(("\n", "-" * 17, "INSTRUMENT MENU: %s" % self.name.upper().ljust(7), "-" * 18))
			proclist = [proc.upper() for proc in self.proctypes]
			try:
				proc_id = int(common.dynamicmenu_get("Select a procedure", proclist, header=header))
			except TypeError:
				break
			else:
				getattr(self, self.proctypes[proc_id])()
	
	

