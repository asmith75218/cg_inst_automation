from common import common
from common.qct_common import Qct
from instruments.ctdmo import cal_ctdmo


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
	INVENTORYCSV = "instruments/ctdmo/ctdmo_inv.csv"
	
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
			self.results_text['8.3.5'] = "Failed to establish communication with instrument."
			self.results_pass['8.3.5'] = False
			return True
		print("Remote id: %s" % instrument.remote_id)
		
		# Add step results to test results dictionaries...
		self.results_text['8.3.5'] = "Established communication with instrument."
		self.results_pass['8.3.5'] = True

		# ---- 8.3.7 ----
		instrument.imm_cmd('#%soutputformat=1' % instrument.remote_id)
		ds = instrument.imm_remote_reply('ds').split()
		instrument.serialnumber = "37-%s" % ds[5]
		instrument.firmware = ds[2]
		print("Serial number: %s" % instrument.serialnumber)
		print("Firmware version: %s" % instrument.firmware)

		# Add step results to test results dictionaries...
		self.results_text['8.3.7a'] = "Serial number confirmed."
		self.results_pass['8.3.7a'] = True
		self.results_text['8.3.7b'] = "Firmware %s confirmed." % instrument.firmware
		self.results_pass['8.3.7b'] = True

		# Use serial number to look up series letter from a csv inventory file...
		inventory_dict = common.dict_from_csv(self.INVENTORYCSV)
		try:
			instrument.seriesletter = inventory_dict[instrument.serialnumber]
		except KeyError:
			instrument.seriesletter = common.usertextselection("Enter the instrument Series (G, H, Q or R): ", "GgHhQqRr").upper()
		print("Class/Series: CTDMO-%s" % instrument.seriesletter)
		
		# Use series letter to get part number...
		instrument.part_no = "%s-%s" % (instrument.class_id, common.partno_from_series(instrument.seriesletter))
		print("Part No.: %s" % instrument.part_no)
		
		# ---- 8.3.8 ----
		print("Retrieving calibration information...")
		cc = instrument.imm_remote_reply('getcc')

		# Generate the calibration CSV...
		print("Exporting calibration to CSV...")
		cc_xml = cc[8:-2]
		cal_ctdmo.export_csv(cc_xml, instrument.seriesletter, self.header['formnumber'])
		
		# ---- 8.3.9 ----
		print("Testing instrument clock...")
		for condition in ['noon', 'utc']:
			if not instrument.clock_set_test(15, condition):
				if not common.userpassanyway():
					common.usercancelled()
					return True
			
		# ---- 8.3.11 ----
		print("Testing configuration...")
		# change sample interval first to 120, then to 10...
		for interval in ['120', '10']:
			instrument.imm_remote_reply('sampleinterval=%s' % interval)
			ds = instrument.imm_remote_reply('ds').split()
			if ds[29] != interval:
				if not common.userpassanyway():
					common.usercancelled()
					return True


		if not instrument.disconnect():
			print("Error closing serial port!")
		return True