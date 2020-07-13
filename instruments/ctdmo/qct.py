from common import common
from common.qct_common import Qct


def init_qct(instrument):
	# COMMON VARIABLES
	USERNAME = common.set_username()        # Test conductor name (entered by user)
	FORMNUMBER = common.set_formnumber()    # QCT sequential form number (or starting number)
	DOCNUMBER = "3305-00101"                # QCT document number
	
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
	# class variables common to all CTDMO QCT
	ID = "01"   # Inductive ID will be reset to this for testing
	
	def __init__(self):
		# Initialize shared Qct superclass attributes...
		super().__init__()
		
		# Initialize or override ctdmo-specific attributes...
		
	def proc_qct(self, instrument):
		# Specify a capture file...
		instrument.capfile = "%s-A.txt" % self.header['docname']

		# Open a serial (RS232) connection...
		while not instrument.connected():
			if not instrument.connect():
	 			common.usercancelled()
	 			return True

		# Establish communication with the IMM...
		instrument.imm_poweron()
		instrument.imm_cmd("gethd")
		instrument.imm_setconfigtype(configtype='1', setenablebinarydata='0')
		
		# ---- 8.3.5 ----
		print("Waking the instrument...")
		instrument.imm_remote_wakeup()

		# ---- 8.3.6 ----
		print("Establishing communication...")
		# Set the instrument's IMM ID...
		if not instrument.imm_set_remote_id(self.ID):
			common.usercancelled()
			return True
		print("Remote id: %s" % instrument.remote_id)
		
		
		if not instrument.disconnect():
			print("Error closing serial port!")
		return True