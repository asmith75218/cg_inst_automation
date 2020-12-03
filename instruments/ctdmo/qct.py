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
		
		# call test procedure...
		qct.proc_qct(instrument)
		
		# test complete, generate results doc...
		# TODO write function to generate the doc and replace below sreendump code
		for key in qct.results_pass:
			b = 'Pass' if qct.results_pass[key] else 'Fail'
			print("%s %s: %s" % (key, b, qct.results_text[key]))
		
		# Prompt to test another instrument, which will incrememt tjhe form number
		# and run the loop again...
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
		self.test_step('8.3.5',
						instrument.imm_set_remote_id(self.ID),
						'Established communication with instrument.',
						'Failed to establish communication with instrument.')
		print("Remote id: %s" % instrument.remote_id)
		
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
		self.test_step('8.3.9',
						instrument.clock_set_test(5, ['noon', 'utc']),
						'The clock was set successfully.',
						'The clock was not set successfully.',
						'The instrument clock was not set to the expected time.')
			
		# ---- 8.3.11 - 8.3.12 ----
		print("Testing configuration...")
		current_steps = ['8.3.11', '8.3.12']
		# change sample interval first to 120, then to 10...
		for i, interval in enumerate(['120', '10']):
			instrument.imm_remote_reply('sampleinterval=%s' % interval)
			ds = instrument.imm_remote_reply('ds').split()
			self.test_step( current_steps[i],
							ds[29] == interval,
							'The sample interval was set successfully.',
							'The sample interval was not set successfully.',
							'The sample interval was not set to the expected value!')

		# ---- 8.3.13 ----
		print("Acquiring a sample...") #TODO complete this step... make loop for try again, etc
		sample_in_air = instrument.take_sample()
		# Test for a valid sample date i.e. today...
		self.test_step('8.3.13a',
						common.compare_date_now(', '.join([sample_in_air[k] for k in ['date','time']]), '%d %b %Y, %H:%M:%S'),
						'The sample contains a vaild timestamp.',
						'The sample does not contain a vaild timestamp.',
						'The sample date is not today!')
		# Overly simple sample range test...
		self.test_step('8.3.13b',
						instrument.sample_range_test(sample_in_air),
						'The sample data appear to be valid.',
						'The sample data appear invalid.')
			
		# ---- 8.3.16 ----
		print("Place the instrument in a container of warm water now.")
		input("Press ENTER to continue...")
		print("Acquiring a sample...")
		sample_in_bucket = instrument.take_sample()
		self.test_step('8.3.16',
						instrument.sample_compare_increase(sample_in_bucket, sample_in_air, 'tp'),
						'The sample data appear to be valid.',
						'The sample data appear invalid.')

		if not instrument.disconnect():
			print("Error closing serial port!")
		return True