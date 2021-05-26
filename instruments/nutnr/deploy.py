from common import common

def proc_deploy(instrument):
	# Specify a capture file...
	instrument.capfile = "save/NUTNR_SN_config_%s.txt" % common.formatdate(common.current_utc(), 'filename')

	# Open a serial (RS232) connection...
	instrument.init_connection()

	# List current configuration details...
	print(instrument.get_cfg())
	
	# Set the instrument clock to current time...
	print(instrument.set_clock())
	print(instrument.get_cmd('get clock'))
	
	# Send deployment configurations to instrument...
	print(instrument.get_cmd('set msglevel info'))
	print(instrument.get_cmd('set outfrtyp full_ascii'))
	print(instrument.get_cmd('set logfrtyp full_ascii'))
	print(instrument.get_cmd('set outdrkfr output'))
	print(instrument.get_cmd('set logdrkfr output'))
	print(instrument.get_cmd('set logftype daily'))
	print(instrument.get_cmd('set opermode continuous'))
	print(instrument.get_cmd('set operctrl samples'))
	print(instrument.get_cmd('set exdevtyp wiper'))
	print(instrument.get_cmd('set exdevrun on'))
	print(instrument.get_cmd('set countdwn 3'))
	print(instrument.get_cmd('set drkavers 100'))
	print(instrument.get_cmd('set lgtavers 3'))
	print(instrument.get_cmd('set drksmpls 1'))
	print(instrument.get_cmd('set lgtsmpls 1'))
	print(instrument.get_cmd('set intpradj off'))
	print(instrument.get_cmd('set intprfac 1'))

	# List updated configuration details...
	print(instrument.get_cfg())
	
	# End procedure...
	if not instrument.disconnect():
		print("Error closing serial port!")
	return True