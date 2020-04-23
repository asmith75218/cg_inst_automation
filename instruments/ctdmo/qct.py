from common import common
from common.qct_common import Qct

def proc_qct(instrument):
	qct = Qct_ctdmo()
		
	print("For the %sth time %s, you better flunk this %s!" % (qct.formnumber, qct.username, instrument.name.upper()))
	


class Qct_ctdmo(Qct):
	def __init__(self):
		# Initialize shared Qct superclass attributes...
		super().__init__()
		
		# Initialize or override ctdmo-specific attributes...
		self.formnumber = "3305-00101-%s" % self.formnumber
	pass