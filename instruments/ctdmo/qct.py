from common import common
from common.qct_common import Qct


def init_qct(instrument):
	# COMMON VARIABLES
	USERNAME = common.set_username()        # Test conductor name (entered by user)
	FORMNUMBER = common.set_formnumber()    # QCT sequential form number (or starting number)
	DOCNUMBER = "3305-00101"                # QCT document number
	ID = "01"                               # Inductive ID will be reset to this for testing
	
	# Main test loop...
	while True:
		qct = Qct_ctdmo()
		qct.init_header(FORMNUMBER, DOCNUMBER, USERNAME)
		qct.proc_qct(instrument)
		again = input("Would you like to test another instrument? y/[n] ")
		if again.lower() != "y":
			return
		input("Type ENTER to begin the next test...")
		FORMNUMBER = common.set_formnumber(FORMNUMBER)
		
class Qct_ctdmo(Qct):
	def __init__(self):
		# Initialize shared Qct superclass attributes...
		super().__init__()
		
		# Initialize or override ctdmo-specific attributes...
		
	def proc_qct(self, instrument):
		instrument.connect()
		if not instrument.port:
			common.usercancelled()
			return
		print("%s! We are the knights who say %s on %s!" % (self.header['username'], self.header['formnumber'], self.header['testdate']))
	