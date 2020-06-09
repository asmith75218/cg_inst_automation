from common.seabird_common import Seabird_instrument
from . import retire, qct

class Ctdmo(Seabird_instrument):
	# class variables common to all CTDMO
	proctypes = ['qct', 'retire']
	name = "CTDMO"
	baudrate = 9600
	
	def __init__(self):
		# instance variables...
		self.timeout = 5
		self.imm_configtype = '1'

		# Initialize shared superclass attributes...
		super().__init__()
	
	# these first definitions are for launching available procedures and should
	# match the above proctypes
	def retire(self):
		retire.proc_retire(self)
		
	def qct(self):
		qct.init_qct(self)
	# --------------------------
	
	
