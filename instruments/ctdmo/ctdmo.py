from common import common
from common.seabird_common import Seabird_instrument
from . import retire, qct

class Ctdmo(Seabird_instrument):
	# class variables common to all CTDMO
	proctypes = ['qct', 'retire']
	name = "CTDMO"
	baudrate = 9600
	class_id = "1336-00001"
	
	def __init__(self):
		# instance variables...
		self.timeout = 5
		self.imm_configtype = '1'
		
		# default validation min/max values for a sample, in air, at normal indoor conditions
		self.sample_minmax = {
			'c_min':'-0.01',
			'c_max':'0.01',
			't_min':'15',
			't_max':'25',
			'p_min':'-0.5',
			'p_max':'0.5'
		}

		# Initialize shared superclass attributes...
		super().__init__()
	
	# these first definitions are for launching available procedures and should
	# match the above proctypes
	def retire(self):
		retire.proc_retire(self)
		
	def qct(self):
		qct.init_qct(self)
	# --------------------------
	
	
	def get_time(self):
		ds = self.imm_remote_reply('ds')
		ds_date = ' '.join(ds.split()[6:10])
		return common.formatdate(ds_date, '%d %b %Y %H:%M:%S')
		
	def clock_set_test(self, margin, setting='utc'):
		while True:
			if setting == 'noon':
				print("Setting clock to noon yesterday...")
				t1 = common.noon_yesterday()
			elif setting == 'utc':
				print("Setting clock to current time UTC...")
				t1 = common.current_utc()
			self.imm_set_datetime(common.formatdate(t1, 'sbe'))	
			t2 = self.get_time()
			if not common.compare_times_ordered(t1, t2, margin):
				if common.usertryagain("There was a problem setting the clock. The reported time is %s. The expected time is %s" % (common.formatdate(t2, 'us'), common.formatdate(t1, 'us'))):
					continue
				else:
					return False
			else:
				return True

	def take_sample(self):
		# Instruct a CTDMO to take a sample, parse the reply and return it as a dictionary
		sample = self.imm_remote_reply('ts')
		print(sample.splitlines()[1])
		sample = sample.split()
		return {'date':sample[4], 'time':sample[5], 'sn':sample[0], 't':sample[1], 'c':sample[2], 'p':sample[3]}
				