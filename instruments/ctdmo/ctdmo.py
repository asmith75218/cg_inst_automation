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
			't_min':'17',
			't_max':'23',
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
		
	def clock_set_test(self, margin, conditions=['utc']):
		for condition in conditions:
			while True:
				if condition == 'noon':
					print("Setting clock to noon yesterday...")
					t1 = common.noon_yesterday()
				elif condition == 'utc':
					print("Setting clock to current time UTC...")
					t1 = common.current_utc()
				self.imm_set_datetime(common.formatdate(t1, 'sbe'))	
				t2 = self.get_time()
				if common.compare_times_ordered(t1, t2, margin):
					break
				else:
					if common.usertryagain("There was a problem setting the clock. The reported time is %s. The expected time is %s" % (common.formatdate(t2, 'us'), common.formatdate(t1, 'us'))):
						continue
					else:
						return False
		return True

	def take_sample(self):
		# Instruct a CTDMO to take a sample, parse the reply and return it as a dictionary
		sample = self.imm_remote_reply('ts').splitlines()[1]
		print(sample)
		sample = [s.strip() for s in sample.split(',')]
		return {'date':sample[4], 'time':sample[5], 'sn':sample[0], 't':sample[1], 'c':sample[2], 'p':sample[3]}
	
	def sample_range_test(self, sample):
		# Test sample values are within predefined min/max range...
		result = True
		params = {'t':'temperature', 'c':'conductivity', 'p':'pressure'}
		sample = {key:value for key, value in sample.items() if key in params.keys()}
		for item in sample.items():
			min, max = [self.sample_minmax[key] for key in ['%s_min' % item[0], '%s_max' % item[0]]]
			if not float(min) < float(item[1]) < float(max):
				print("The %s value '%s' appears to be out of range!" % (params[item[0]], item[1]))
				result = False
		return result	

	def sample_compare_increase(self, sample2, sample1, params):
		# Test sample values increased for specified parameters ...
		result = True
		param_names = {'t':'temperature', 'c':'conductivity', 'p':'pressure'}
		sample1 = {key:value for key, value in sample1.items() if key in params}
		sample2 = {key:value for key, value in sample2.items() if key in params}
		for item in sample2.items():
			print('Testing %s <= %s...' % (item[1], sample1[item[0]]))
			if not float(item[1]) >= float(sample1[item[0]]):
				print("The %s value did not increase as expected!" % param_names[item[0]])
				result = False
		return result