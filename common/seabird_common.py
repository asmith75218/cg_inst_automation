from .serial_common import Serial_instrument

class Seabird_instrument(Serial_instrument):
	def __init__(self):
		# Initialize shared Instrument superclass attributes...
		super().__init__()

	def imm_timedout(self):
		if not self.buffer_empty():
			self.cap_buf()
			if "TIMEOUT" in self.buf:
				return True
		else:
			return False
	
	def imm_poweron(self):
		self.cap_cmd('')
		if "S>" in self.buf:
			self.configtype = "1"
			return True
		elif "IMM>" in self.buf:
			self.configtype = "2"
			return True
		else: return False
		
	def imm_cmd(self, cmd):
		if self.imm_timedout():
			self.imm_poweron()
		self.cap_cmd(cmd)
		
	def imm_remote_wakeup(self):
		pass
		
	def imm_remote_cmd(self, cmd):
		pass
