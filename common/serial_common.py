from serial import Serial
from serial.tools import list_ports
from workbench import Instrument
from . import common

class Serial_instrument(Instrument):
	def __init__(self):
		# Initialize shared Instrument superclass attributes...
		super().__init__()


	def set_serialport(self):
		ports = [port for port in list_ports.comports()]
		portmenu = ["%s - %s" % (port.device, port.description) for port in ports]
		try:
			port_id = int(common.dynamicmenu_get("Select an available port", portmenu, lastitem=('C', 'Cancel')))
		except TypeError:
			print("TypeError in set_serialport()")
			return None
		return ports[port_id]

	def serialport_open(self, baudrate, timeout=5):
		"""Open connection to a serial port and start logging to a file."""
		while True:
			try:
				print("Connecting to %s at %d baud..." % (self.port, baudrate))
			except AttributeError:
				self.port = self.set_serialport()
				continue
			break
		try:
			self.ser = Serial(self.port[0], baudrate, timeout)
		except BaseException as msg:
			input("\nError! %s [Press ENTER to continue]..." % msg)
			return None
		print("Connected to %s." % self.port)
