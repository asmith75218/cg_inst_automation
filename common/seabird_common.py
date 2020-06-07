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
		