from common import common
from common.serial_common import Serial_instrument
from . import deploy

class Nutnr(Serial_instrument):
	# class variables common to all nutnr
	proctypes = ['deploy']
	name = "NUTNR"
	baudrate = 57600
	# TODO part no. for nutnr: class_id = "1336-00001"
	
	def __init__(self):
		# instance variables...
		self.timeout = 1

		# Initialize shared superclass attributes...
		super().__init__()
	
	# these first definitions are for launching available procedures and should
	# match the above proctypes
	def deploy(self):
		deploy.proc_deploy(self)
		
	# --------------------------

	def init_connection(self):		
		self.connect()

		while not instrument.get_prompt():
			if common.usertryagain("Failed to communicate with instrument."):
				continue
			else:
				common.usercancelled()
				return True

	def get_prompt(self):
		self.cap_cmd('$')
		if "SUNA>" in self.buf:
			return True
		else: return False

	def get_cfg(self):
		return self.get_cmd('get cfg')

	def set_clock(self):
		return self.get_cmd('set clock %s' % common.formatdate(common.current_utc(), 'suna'))