from workbench import Instrument
from . import retire

class Dummy(Instrument):
	# class variables common to all DUMMY
	proctypes = ['qct', 'retire']
	
	def retire(self):
		retire.proc_retire(self)
		
	def qct(self):
		qct.proc_qct(self)