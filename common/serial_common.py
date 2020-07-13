from datetime import datetime as dt
from serial import Serial
from serial.tools import list_ports
from instrumentbase import Instrument
from . import common

## This module is for functions/methods etc shared by all serial instruments to
## access the serial driver. Most if not everything in this module will include
## calls to the serial driver module. NO FUNCTIONS IN ANY OTHER MODULE SHALL MAKE
## CALLS TO THE SERIAL DRIVER MODULE. In this way, should the serial driver module
## change in the future, only this common serial library will need to be updated.
##
## Serial driver module at time of writing is: pyserial 3.4

class Serial_instrument(Instrument):
	def __init__(self):
		# Initialize shared Instrument superclass attributes...
		super().__init__()

		self.ser = Serial()
		self.ser.baudrate = self.baudrate
		self.ser.timeout = self.timeout
		self.port = None
		self.capfile = "Serial_instrument.log"	# Default should be overridden in instrument-specific module


	def set_serialport(self):
		ports = [port for port in list_ports.comports()]
		portmenu = ["%s - %s" % (port.device, port.description) for port in ports]

		# Present port selection menu to user...
		userselection = common.dynamicmenu_get("Select an available port", portmenu, lastitem=('C', 'Cancel'))
		if not userselection:
			# Cancelled by user...
			return False
		
		port_id = int(userselection)
		self.port = ports[port_id]
		self.ser.port = self.port[0]
		return True

	def serialport_open(self):
		"""Open connection to a serial port and initialize a log file."""
		while not self.port:
			# No port chosen, try to choose one...
			if not self.set_serialport():
				again = input("Would you like to try to connect again? y/[n] ")
				if again.lower() != "y":
					# Cancelled by user...
					return False
		try:
			self.ser.open()
		except BaseException as msg:
			input("\nError! %s [Press ENTER to continue]..." % msg)
			return False
		print("Connected to %s." % self.port)
		with open(self.capfile, "w") as capfile:
			self.capfileheader = " ".join(("=" * 22, "Session log - %s" % dt.now().strftime("%Y/%m/%d %H:%M:%S"), "=" * 22, "\r\n"))
			capfile.write(self.capfileheader)
		return True

	def cap_cmd(self, cmd):
		"""
		Send a single commmand cmd to an instrument. Write the reply to the
		capture file. If instrument echoes the command, the command will also
		be captured.
		"""
		self.ser.reset_input_buffer()
		self.send_cmd(cmd)
		self.cap_buf()
		return True

	def send_cmd(self, cmd):
		return self.ser.write((cmd + '\r\n').encode('ascii'))
		
	def read_reply(self):
		# Read incoming serial input and store in a buffer until no new bytes are
		# received for duration of the timeout.
		self.buf = self.ser.read(self.ser.in_waiting).decode('ascii')
		while True:
			cur = self.buf
			self.buf += self.ser.read(1).decode('ascii')
			if cur == self.buf:
				return True
		
	def cap_buf(self):
		# Read serial input and append to the capture file.
		self.read_reply()
		self.capfile_append(self.buf)
		return True

	def connect(self):
		# Wrapper to open a serial connection. Returns True or False.
		return self.serialport_open()
	
	def connected(self):
		# Wrapper to test for open serial port. Returns True of False.
		return self.ser.is_open
	
	def disconnect(self):
		# Wrapper to close a serial connection. Returns True or False.
		self.ser.close()
		return not self.ser.is_open
		
	def capfile_append(self, lines):
		# Append text to a capture file. Pass text to append as lines.
		with open(self.capfile, 'a') as capfile:
			capfile.write(lines)
	
	def buffer_empty(self):
		# Check for unread bytes in serial input buffer. Returns True of False.
		if not self.ser.in_waiting:
			return True
		else:
			return False
	
