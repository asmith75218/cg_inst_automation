from workbench import Instrument
from . import retire, qct

class Ctdmo(Instrument):
	# class variables common to all DUMMY
	proctypes = ['qct', 'retire']
	
	# these first definitions are for launching available procedures and should
	# match the above proctypes
	def retire(self):
		retire.proc_retire(self)
		
	def qct(self):
		qct.proc_qct(self)
	# --------------------------
	
	
